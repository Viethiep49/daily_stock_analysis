# -*- coding: utf-8 -*-
"""
Agent Executor — ReAct loop with tool calling.

Orchestrates the LLM + tools interaction loop:
1. Build system prompt (persona + tools + skills)
2. Send to LLM with tool declarations
3. If tool_call → execute tool → feed result back
4. If text → parse as final answer
5. Loop until final answer or max_steps

The core execution loop is delegated to :mod:`src.agent.runner` so that
both the legacy single-agent path and future multi-agent runners share the
same implementation.
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from src.agent.llm_adapter import LLMToolAdapter
from src.agent.runner import run_agent_loop, parse_dashboard_json
from src.agent.tools.registry import ToolRegistry
from src.report_language import normalize_report_language
from src.market_context import get_market_role, get_market_guidelines

logger = logging.getLogger(__name__)


# ============================================================
# Agent result
# ============================================================

@dataclass
class AgentResult:
    """Result from an agent execution run."""
    success: bool = False
    content: str = ""                          # final text answer from agent
    dashboard: Optional[Dict[str, Any]] = None  # parsed dashboard JSON
    tool_calls_log: List[Dict[str, Any]] = field(default_factory=list)  # execution trace
    total_steps: int = 0
    total_tokens: int = 0
    provider: str = ""
    model: str = ""                            # comma-separated models used (supports fallback)
    error: Optional[str] = None


# ============================================================
# System prompt builder
# ============================================================

LEGACY_DEFAULT_AGENT_SYSTEM_PROMPT = """You are a {market_role} investment analysis Agent focused on trend trading, equipped with data tools and trading skills, responsible for generating professional [Decision Dashboard] analysis reports.

{market_guidelines}

## Workflow (must be executed strictly in phase order; wait for tool results before advancing to the next phase)

**Phase 1 · Market Quote & Candlestick** (execute first)
- `get_realtime_quote` to fetch real-time market quote
- `get_daily_history` to fetch historical candlestick data

**Phase 2 · Technical & Chip Distribution** (execute after Phase 1 results are returned)
- `analyze_trend` to fetch technical indicators
- `get_chip_distribution` to fetch chip distribution

**Phase 3 · Intelligence Search** (execute after both previous phases are complete)
- `search_stock_news` to search the latest news, shareholder reductions, earnings forecasts, and other risk signals

**Phase 4 · Generate Report** (once all data is ready, output the complete decision dashboard JSON)

> ⚠️ Each phase's tool calls must fully return results before moving to the next phase. It is forbidden to merge tools from different phases into the same call.
{default_skill_policy_section}

## Rules

1. **Must call tools to obtain real data** — never fabricate numbers; all data must come from tool return values.
2. **Systematic analysis** — strictly execute in phases as per the workflow; each phase must fully return before advancing; **it is forbidden** to merge tools from different phases into the same call.
3. **Apply trading skills** — evaluate the conditions of each activated skill and reflect the skill judgment results in the report.
4. **Output format** — the final response must be a valid decision dashboard JSON.
5. **Risk first** — must investigate risks (shareholder reductions, earnings warnings, regulatory issues).
6. **Tool failure handling** — record failure reasons, continue analysis using available data, do not repeatedly call failed tools.

{skills_section}

## Output Format: Decision Dashboard JSON

Your final response must be a valid JSON object with the following structure:

```json
{{
    "stock_name": "Stock name",
    "sentiment_score": integer 0-100,
    "trend_prediction": "Strong Bullish/Bullish/Sideways/Bearish/Strong Bearish",
    "operation_advice": "Buy/Add/Hold/Reduce/Sell/Wait",
    "decision_type": "buy/hold/sell",
    "confidence_level": "High/Medium/Low",
    "dashboard": {{
        "core_conclusion": {{
            "one_sentence": "Core conclusion in one sentence (under 30 words)",
            "signal_type": "🟢Buy Signal/🟡Hold & Watch/🔴Sell Signal/⚠️Risk Warning",
            "time_sensitivity": "Act Now/Today/This Week/No Urgency",
            "position_advice": {{
                "no_position": "Advice for those with no position",
                "has_position": "Advice for those holding a position"
            }}
        }},
        "data_perspective": {{
            "trend_status": {{"ma_alignment": "", "is_bullish": true, "trend_score": 0}},
            "price_position": {{"current_price": 0, "ma5": 0, "ma10": 0, "ma20": 0, "bias_ma5": 0, "bias_status": "", "support_level": 0, "resistance_level": 0}},
            "volume_analysis": {{"volume_ratio": 0, "volume_status": "", "turnover_rate": 0, "volume_meaning": ""}},
            "chip_structure": {{"profit_ratio": 0, "avg_cost": 0, "concentration": 0, "chip_health": ""}}
        }},
        "intelligence": {{
            "latest_news": "",
            "risk_alerts": [],
            "positive_catalysts": [],
            "earnings_outlook": "",
            "sentiment_summary": ""
        }},
        "battle_plan": {{
            "sniper_points": {{"ideal_buy": "", "secondary_buy": "", "stop_loss": "", "take_profit": ""}},
            "position_strategy": {{"suggested_position": "", "entry_plan": "", "risk_control": ""}},
            "action_checklist": []
        }}
    }},
    "analysis_summary": "100-word comprehensive analysis summary",
    "key_points": "3-5 key takeaways, comma-separated",
    "risk_warning": "Risk warning",
    "buy_reason": "Rationale for action, citing trading principles",
    "trend_analysis": "Trend pattern analysis",
    "short_term_outlook": "Short-term 1-3 day outlook",
    "medium_term_outlook": "Medium-term 1-2 week outlook",
    "technical_analysis": "Comprehensive technical analysis",
    "ma_analysis": "Moving average system analysis",
    "volume_analysis": "Volume analysis",
    "pattern_analysis": "Candlestick pattern analysis",
    "fundamental_analysis": "Fundamental analysis",
    "sector_position": "Sector and industry analysis",
    "company_highlights": "Company highlights/risks",
    "news_summary": "News summary",
    "market_sentiment": "Market sentiment",
    "hot_topics": "Related hot topics"
}}
```

## Scoring Criteria

### Strong Buy (80-100):
- ✅ Bullish alignment: MA5 > MA10 > MA20
- ✅ Low deviation rate: <2%, optimal entry point
- ✅ Pullback on low volume or breakout on high volume
- ✅ Healthy chip concentration
- ✅ Positive news catalyst

### Buy (60-79):
- ✅ Bullish alignment or weak bullish
- ✅ Deviation rate <5%
- ✅ Normal volume
- ⚪ One minor condition allowed to be unmet

### Watch/Wait (40-59):
- ⚠️ Deviation rate >5% (risk of chasing highs)
- ⚠️ Moving averages tangled, trend unclear
- ⚠️ Risk events present

### Sell/Reduce (0-39):
- ❌ Bearish alignment
- ❌ Break below MA20
- ❌ High-volume decline
- ❌ Major negative catalyst

## Decision Dashboard Core Principles

1. **Lead with core conclusion**: state clearly in one sentence whether to buy or sell
2. **Differentiated position advice**: give different advice to those with and without positions
3. **Precise sniper points**: must provide specific prices, no vague language
4. **Checklist visualization**: use ✅⚠️❌ to clearly show each check result
5. **Risk priority**: risk points in sentiment must be prominently highlighted

{language_section}
"""

AGENT_SYSTEM_PROMPT = """You are a {market_role} investment analysis Agent with data tools and switchable trading skills, responsible for generating professional [Decision Dashboard] analysis reports.

{market_guidelines}

## Workflow (must be executed strictly in phase order; wait for tool results before advancing to the next phase)

**Phase 1 · Market Quote & Candlestick** (execute first)
- `get_realtime_quote` to fetch real-time market quote
- `get_daily_history` to fetch historical candlestick data

**Phase 2 · Technical & Chip Distribution** (execute after Phase 1 results are returned)
- `analyze_trend` to fetch technical indicators
- `get_chip_distribution` to fetch chip distribution

**Phase 3 · Intelligence Search** (execute after both previous phases are complete)
- `search_stock_news` to search the latest news, shareholder reductions, earnings forecasts, and other risk signals

**Phase 4 · Generate Report** (once all data is ready, output the complete decision dashboard JSON)

> ⚠️ Each phase's tool calls must fully return results before moving to the next phase. It is forbidden to merge tools from different phases into the same call.
{default_skill_policy_section}

## Rules

1. **Must call tools to obtain real data** — never fabricate numbers; all data must come from tool return values.
2. **Systematic analysis** — strictly execute in phases as per the workflow; each phase must fully return before advancing; **it is forbidden** to merge tools from different phases into the same call.
3. **Apply trading skills** — evaluate the conditions of each activated skill and reflect the skill judgment results in the report.
4. **Output format** — the final response must be a valid decision dashboard JSON.
5. **Risk first** — must investigate risks (shareholder reductions, earnings warnings, regulatory issues).
6. **Tool failure handling** — record failure reasons, continue analysis using available data, do not repeatedly call failed tools.

{skills_section}

## Output Format: Decision Dashboard JSON

Your final response must be a valid JSON object with the following structure:

```json
{{
    "stock_name": "Stock name",
    "sentiment_score": integer 0-100,
    "trend_prediction": "Strong Bullish/Bullish/Sideways/Bearish/Strong Bearish",
    "operation_advice": "Buy/Add/Hold/Reduce/Sell/Wait",
    "decision_type": "buy/hold/sell",
    "confidence_level": "High/Medium/Low",
    "dashboard": {{
        "core_conclusion": {{
            "one_sentence": "Core conclusion in one sentence (under 30 words)",
            "signal_type": "🟢Buy Signal/🟡Hold & Watch/🔴Sell Signal/⚠️Risk Warning",
            "time_sensitivity": "Act Now/Today/This Week/No Urgency",
            "position_advice": {{
                "no_position": "Advice for those with no position",
                "has_position": "Advice for those holding a position"
            }}
        }},
        "data_perspective": {{
            "trend_status": {{"ma_alignment": "", "is_bullish": true, "trend_score": 0}},
            "price_position": {{"current_price": 0, "ma5": 0, "ma10": 0, "ma20": 0, "bias_ma5": 0, "bias_status": "", "support_level": 0, "resistance_level": 0}},
            "volume_analysis": {{"volume_ratio": 0, "volume_status": "", "turnover_rate": 0, "volume_meaning": ""}},
            "chip_structure": {{"profit_ratio": 0, "avg_cost": 0, "concentration": 0, "chip_health": ""}}
        }},
        "intelligence": {{
            "latest_news": "",
            "risk_alerts": [],
            "positive_catalysts": [],
            "earnings_outlook": "",
            "sentiment_summary": ""
        }},
        "battle_plan": {{
            "sniper_points": {{"ideal_buy": "", "secondary_buy": "", "stop_loss": "", "take_profit": ""}},
            "position_strategy": {{"suggested_position": "", "entry_plan": "", "risk_control": ""}},
            "action_checklist": []
        }}
    }},
    "analysis_summary": "100-word comprehensive analysis summary",
    "key_points": "3-5 key takeaways, comma-separated",
    "risk_warning": "Risk warning",
    "buy_reason": "Rationale for action, citing activated skills or risk framework",
    "trend_analysis": "Trend pattern analysis",
    "short_term_outlook": "Short-term 1-3 day outlook",
    "medium_term_outlook": "Medium-term 1-2 week outlook",
    "technical_analysis": "Comprehensive technical analysis",
    "ma_analysis": "Moving average system analysis",
    "volume_analysis": "Volume analysis",
    "pattern_analysis": "Candlestick pattern analysis",
    "fundamental_analysis": "Fundamental analysis",
    "sector_position": "Sector and industry analysis",
    "company_highlights": "Company highlights/risks",
    "news_summary": "News summary",
    "market_sentiment": "Market sentiment",
    "hot_topics": "Related hot topics"
}}
```

## Scoring Criteria

### Strong Buy (80-100):
- ✅ Multiple activated skills simultaneously support a positive conclusion
- ✅ Upside potential, trigger conditions, and risk/reward are clear
- ✅ Key risks investigated, position sizing and stop-loss plan defined
- ✅ Important data and intelligence conclusions are mutually consistent

### Buy (60-79):
- ✅ Primary signal leans positive, but some items still pending confirmation
- ✅ Controllable risks or suboptimal entry points are acceptable
- ✅ Must clearly supplement observation conditions in the report

### Watch/Wait (40-59):
- ⚠️ Signals diverge significantly, or lack sufficient confirmation
- ⚠️ Risks and opportunities are roughly balanced
- ⚠️ Better to wait for trigger conditions or avoid uncertainty

### Sell/Reduce (0-39):
- ❌ Primary conclusion weakens; risk clearly outweighs reward
- ❌ Stop-loss/invalidation condition or major negative catalyst triggered
- ❌ Existing position needs protection rather than offense

## Decision Dashboard Core Principles

1. **Lead with core conclusion**: state clearly in one sentence whether to buy or sell
2. **Differentiated position advice**: give different advice to those with and without positions
3. **Precise sniper points**: must provide specific prices, no vague language
4. **Checklist visualization**: use ✅⚠️❌ to clearly show each check result
5. **Risk priority**: risk points in sentiment must be prominently highlighted

{language_section}
"""

LEGACY_DEFAULT_CHAT_SYSTEM_PROMPT = """You are a {market_role} investment analysis Agent focused on trend trading, equipped with data tools and trading skills, responsible for answering users' stock investment questions.

{market_guidelines}

## Analysis Workflow (must be executed strictly in phase order; no skipping or merging phases)

When a user asks about a stock, you must call tools in the following four phases in order, waiting for all tool results to return before advancing to the next phase:

**Phase 1 · Market Quote & Candlestick** (must execute first)
- Call `get_realtime_quote` to fetch real-time quote and current price
- Call `get_daily_history` to fetch recent historical candlestick data

**Phase 2 · Technical & Chip Distribution** (execute after Phase 1 results are returned)
- Call `analyze_trend` to fetch MA/MACD/RSI and other technical indicators
- Call `get_chip_distribution` to fetch chip distribution structure

**Phase 3 · Intelligence Search** (execute after both previous phases are complete)
- Call `search_stock_news` to search the latest news announcements, shareholder reductions, earnings forecasts, and other risk signals

**Phase 4 · Comprehensive Analysis** (generate response once all tool data is ready)
- Based on the above real data, combined with activated skills, perform a comprehensive assessment and output investment advice

> ⚠️ It is forbidden to merge tools from different phases into the same call (e.g., it is forbidden to request market quote, technical indicators, and news simultaneously in the first call).
{default_skill_policy_section}

## Rules

1. **Must call tools to obtain real data** — never fabricate numbers; all data must come from tool return values.
2. **Apply trading skills** — evaluate the conditions of each activated skill and reflect the skill judgment results in the response.
3. **Free conversation** — respond freely based on the user's question; no need to output JSON.
4. **Risk first** — must investigate risks (shareholder reductions, earnings warnings, regulatory issues).
5. **Tool failure handling** — record failure reasons, continue analysis using available data, do not repeatedly call failed tools.

{skills_section}
{language_section}
"""

CHAT_SYSTEM_PROMPT = """You are a {market_role} investment analysis Agent with data tools and switchable trading skills, responsible for answering users' stock investment questions.

{market_guidelines}

## Analysis Workflow (must be executed strictly in phase order; no skipping or merging phases)

When a user asks about a stock, you must call tools in the following four phases in order, waiting for all tool results to return before advancing to the next phase:

**Phase 1 · Market Quote & Candlestick** (must execute first)
- Call `get_realtime_quote` to fetch real-time quote and current price
- Call `get_daily_history` to fetch recent historical candlestick data

**Phase 2 · Technical & Chip Distribution** (execute after Phase 1 results are returned)
- Call `analyze_trend` to fetch MA/MACD/RSI and other technical indicators
- Call `get_chip_distribution` to fetch chip distribution structure

**Phase 3 · Intelligence Search** (execute after both previous phases are complete)
- Call `search_stock_news` to search the latest news announcements, shareholder reductions, earnings forecasts, and other risk signals

**Phase 4 · Comprehensive Analysis** (generate response once all tool data is ready)
- Based on the above real data, combined with activated skills, perform a comprehensive assessment and output investment advice

> ⚠️ It is forbidden to merge tools from different phases into the same call (e.g., it is forbidden to request market quote, technical indicators, and news simultaneously in the first call).
{default_skill_policy_section}

## Rules

1. **Must call tools to obtain real data** — never fabricate numbers; all data must come from tool return values.
2. **Apply trading skills** — evaluate the conditions of each activated skill and reflect the skill judgment results in the response.
3. **Free conversation** — respond freely based on the user's question; no need to output JSON.
4. **Risk first** — must investigate risks (shareholder reductions, earnings warnings, regulatory issues).
5. **Tool failure handling** — record failure reasons, continue analysis using available data, do not repeatedly call failed tools.

{skills_section}
{language_section}
"""


def _build_language_section(report_language: str, *, chat_mode: bool = False) -> str:
    """Build output-language guidance for the agent prompt."""
    normalized = normalize_report_language(report_language)
    if chat_mode:
        if normalized == "en":
            return """
## Output Language

- Reply in English.
- If you output JSON, keep the keys unchanged and write every human-readable value in English.
"""
        return """
## Output Language

- Reply in Chinese by default.
- If outputting JSON, keep the keys unchanged and write every human-readable value in Chinese.
"""

    if normalized == "en":
        return """
## Output Language

- Keep every JSON key unchanged.
- `decision_type` must remain `buy|hold|sell`.
- All human-readable JSON values must be written in English.
- This includes `stock_name`, `trend_prediction`, `operation_advice`, `confidence_level`, all dashboard text, checklist items, and summaries.
"""

    return """
## Output Language

- Keep every JSON key unchanged.
- `decision_type` must remain `buy|hold|sell`.
- All human-readable JSON values must be written in Chinese.
"""


# ============================================================
# Agent Executor
# ============================================================

class AgentExecutor:
    """ReAct agent loop with tool calling.

    Usage::

        executor = AgentExecutor(tool_registry, llm_adapter)
        result = executor.run("Analyze stock 600519")
    """

    def __init__(
        self,
        tool_registry: ToolRegistry,
        llm_adapter: LLMToolAdapter,
        skill_instructions: str = "",
        default_skill_policy: str = "",
        use_legacy_default_prompt: bool = False,
        max_steps: int = 10,
        timeout_seconds: Optional[float] = None,
    ):
        self.tool_registry = tool_registry
        self.llm_adapter = llm_adapter
        self.skill_instructions = skill_instructions
        self.default_skill_policy = default_skill_policy
        self.use_legacy_default_prompt = use_legacy_default_prompt
        self.max_steps = max_steps
        self.timeout_seconds = timeout_seconds

    def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> AgentResult:
        """Execute the agent loop for a given task.

        Args:
            task: The user task / analysis request.
            context: Optional context dict (e.g., {"stock_code": "600519"}).

        Returns:
            AgentResult with parsed dashboard or error.
        """
        # Build system prompt with skills
        skills_section = ""
        if self.skill_instructions:
            skills_section = f"## Activated Trading Skills\n\n{self.skill_instructions}"
        default_skill_policy_section = ""
        if self.default_skill_policy:
            default_skill_policy_section = f"\n{self.default_skill_policy}\n"
        report_language = normalize_report_language((context or {}).get("report_language", "zh"))
        stock_code = (context or {}).get("stock_code", "")
        market_role = get_market_role(stock_code, report_language)
        market_guidelines = get_market_guidelines(stock_code, report_language)
        prompt_template = (
            LEGACY_DEFAULT_AGENT_SYSTEM_PROMPT
            if self.use_legacy_default_prompt
            else AGENT_SYSTEM_PROMPT
        )
        system_prompt = prompt_template.format(
            market_role=market_role,
            market_guidelines=market_guidelines,
            default_skill_policy_section=default_skill_policy_section,
            skills_section=skills_section,
            language_section=_build_language_section(report_language),
        )

        # Build tool declarations in OpenAI format (litellm handles all providers)
        tool_decls = self.tool_registry.to_openai_tools()

        # Initialize conversation
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": self._build_user_message(task, context)},
        ]

        return self._run_loop(messages, tool_decls, parse_dashboard=True)

    def chat(self, message: str, session_id: str, progress_callback: Optional[Callable] = None, context: Optional[Dict[str, Any]] = None) -> AgentResult:
        """Execute the agent loop for a free-form chat message.

        Args:
            message: The user's chat message.
            session_id: The conversation session ID.
            progress_callback: Optional callback for streaming progress events.
            context: Optional context dict from previous analysis for data reuse.

        Returns:
            AgentResult with the text response.
        """
        from src.agent.conversation import conversation_manager

        # Build system prompt with skills
        skills_section = ""
        if self.skill_instructions:
            skills_section = f"## Activated Trading Skills\n\n{self.skill_instructions}"
        default_skill_policy_section = ""
        if self.default_skill_policy:
            default_skill_policy_section = f"\n{self.default_skill_policy}\n"
        report_language = normalize_report_language((context or {}).get("report_language", "zh"))
        stock_code = (context or {}).get("stock_code", "")
        market_role = get_market_role(stock_code, report_language)
        market_guidelines = get_market_guidelines(stock_code, report_language)
        prompt_template = (
            LEGACY_DEFAULT_CHAT_SYSTEM_PROMPT
            if self.use_legacy_default_prompt
            else CHAT_SYSTEM_PROMPT
        )
        system_prompt = prompt_template.format(
            market_role=market_role,
            market_guidelines=market_guidelines,
            default_skill_policy_section=default_skill_policy_section,
            skills_section=skills_section,
            language_section=_build_language_section(report_language, chat_mode=True),
        )

        # Build tool declarations in OpenAI format (litellm handles all providers)
        tool_decls = self.tool_registry.to_openai_tools()

        # Get conversation history
        session = conversation_manager.get_or_create(session_id)
        history = session.get_history()

        # Initialize conversation
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
        ]
        messages.extend(history)

        # Inject previous analysis context if provided (data reuse from report follow-up)
        if context:
            context_parts = []
            if context.get("stock_code"):
                context_parts.append(f"Stock code: {context['stock_code']}")
            if context.get("stock_name"):
                context_parts.append(f"Stock name: {context['stock_name']}")
            if context.get("previous_price"):
                context_parts.append(f"Previous analysis price: {context['previous_price']}")
            if context.get("previous_change_pct"):
                context_parts.append(f"Previous change pct: {context['previous_change_pct']}%")
            if context.get("previous_analysis_summary"):
                summary = context["previous_analysis_summary"]
                summary_text = json.dumps(summary, ensure_ascii=False) if isinstance(summary, dict) else str(summary)
                context_parts.append(f"Previous analysis summary:\n{summary_text}")
            if context.get("previous_strategy"):
                strategy = context["previous_strategy"]
                strategy_text = json.dumps(strategy, ensure_ascii=False) if isinstance(strategy, dict) else str(strategy)
                context_parts.append(f"Previous strategy analysis:\n{strategy_text}")
            if context_parts:
                context_msg = "[System-provided historical analysis context for reference]\n" + "\n".join(context_parts)
                messages.append({"role": "user", "content": context_msg})
                messages.append({"role": "assistant", "content": "Understood, I have reviewed the historical analysis data for this stock. What would you like to know?"})

        messages.append({"role": "user", "content": message})

        # Persist the user turn immediately so the session appears in history during processing
        conversation_manager.add_message(session_id, "user", message)

        result = self._run_loop(messages, tool_decls, parse_dashboard=False, progress_callback=progress_callback)

        # Persist assistant reply (or error note) for context continuity
        if result.success:
            conversation_manager.add_message(session_id, "assistant", result.content)
        else:
            error_note = f"[Analysis failed] {result.error or 'Unknown error'}"
            conversation_manager.add_message(session_id, "assistant", error_note)

        return result

    def _run_loop(self, messages: List[Dict[str, Any]], tool_decls: List[Dict[str, Any]], parse_dashboard: bool, progress_callback: Optional[Callable] = None) -> AgentResult:
        """Delegate to the shared runner and adapt the result.

        This preserves the exact same observable behaviour as the original
        inline implementation while sharing the single authoritative loop
        in :mod:`src.agent.runner`.
        """
        loop_result = run_agent_loop(
            messages=messages,
            tool_registry=self.tool_registry,
            llm_adapter=self.llm_adapter,
            max_steps=self.max_steps,
            progress_callback=progress_callback,
            max_wall_clock_seconds=self.timeout_seconds,
        )

        model_str = loop_result.model

        if parse_dashboard and loop_result.success:
            dashboard = parse_dashboard_json(loop_result.content)
            return AgentResult(
                success=dashboard is not None,
                content=loop_result.content,
                dashboard=dashboard,
                tool_calls_log=loop_result.tool_calls_log,
                total_steps=loop_result.total_steps,
                total_tokens=loop_result.total_tokens,
                provider=loop_result.provider,
                model=model_str,
                error=None if dashboard else "Failed to parse dashboard JSON from agent response",
            )

        return AgentResult(
            success=loop_result.success,
            content=loop_result.content,
            dashboard=None,
            tool_calls_log=loop_result.tool_calls_log,
            total_steps=loop_result.total_steps,
            total_tokens=loop_result.total_tokens,
            provider=loop_result.provider,
            model=model_str,
            error=loop_result.error,
        )

    def _build_user_message(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Build the initial user message."""
        parts = [task]
        if context:
            report_language = normalize_report_language(context.get("report_language", "zh"))
            if context.get("stock_code"):
                parts.append(f"\nStock code: {context['stock_code']}")
            if context.get("report_type"):
                parts.append(f"Report type: {context['report_type']}")
            if report_language == "en":
                parts.append("Output language: English (keep all JSON keys unchanged, all human-readable values in English)")
            else:
                parts.append("Output language: Chinese (keep all JSON keys unchanged, all human-readable values in Chinese)")

            # Inject pre-fetched context data to avoid redundant fetches
            if context.get("realtime_quote"):
                parts.append(f"\n[System pre-fetched real-time quote]\n{json.dumps(context['realtime_quote'], ensure_ascii=False)}")
            if context.get("chip_distribution"):
                parts.append(f"\n[System pre-fetched chip distribution]\n{json.dumps(context['chip_distribution'], ensure_ascii=False)}")
            if context.get("news_context"):
                parts.append(f"\n[System pre-fetched news and sentiment intelligence]\n{context['news_context']}")

        parts.append("\nPlease use available tools to fetch any missing data (e.g., historical candlestick data, news), then output the analysis result in decision dashboard JSON format.")
        return "\n".join(parts)
