# -*- coding: utf-8 -*-
"""
===================================
Market Review — Vietnam Market (VNINDEX + VN30)
===================================

Runs the daily market review for Vietnam's HOSE/HNX exchanges.
Fetches VNINDEX and VN30 data, calls the AI analyzer,
saves the report, and sends notifications.
"""

import logging
from datetime import datetime
from typing import Optional

from src.config import get_config
from src.notification import NotificationService
from src.market_analyzer import MarketAnalyzer
from src.search_service import SearchService
from src.analyzer import GeminiAnalyzer

logger = logging.getLogger(__name__)


def run_market_review(
    notifier: NotificationService,
    analyzer: Optional[GeminiAnalyzer] = None,
    search_service: Optional[SearchService] = None,
    send_notification: bool = True,
    merge_notification: bool = False,
    override_region: Optional[str] = None,
) -> Optional[str]:
    """
    Run the Vietnam daily market review (VNINDEX + VN30).

    Args:
        notifier:           Notification service instance.
        analyzer:           AI analyzer (optional).
        search_service:     Search/news service (optional).
        send_notification:  Whether to push the report.
        merge_notification: When True, skip standalone push; let the caller
                            combine individual-stock + market results (Issue #190).
        override_region:    Effective region after trading-day filter (Issue #373).
                            Ignored if not 'vn' or None — always runs VN review.

    Returns:
        Report text string, or None on failure.
    """
    logger.info("[MarketReview] Starting Vietnam market review (VNINDEX + VN30)...")
    config = get_config()

    # Respect trading-day filter: empty string means market is closed today
    effective_region = override_region if override_region is not None else "vn"
    if effective_region == "":
        logger.info("[MarketReview] Vietnam market is closed today — skipping review.")
        return None

    try:
        vn_analyzer = MarketAnalyzer(
            search_service=search_service,
            analyzer=analyzer,
            region="vn",
        )
        review_report = vn_analyzer.run_daily_review()

        if review_report:
            # Save report to file
            date_str = datetime.now().strftime("%Y%m%d")
            report_filename = f"market_review_vn_{date_str}.md"
            filepath = notifier.save_report_to_file(
                f"# 📊 Thị Trường Việt Nam — Tổng Kết Ngày\n\n{review_report}",
                report_filename,
            )
            logger.info("[MarketReview] Report saved: %s", filepath)

            if merge_notification and send_notification:
                logger.info(
                    "[MarketReview] Merge mode: skipping standalone push; "
                    "will be combined with individual-stock report."
                )
            elif send_notification and notifier.is_available():
                report_content = f"📊 Thị Trường VN hôm nay\n\n{review_report}"
                if notifier.send(report_content, email_send_to_all=True):
                    logger.info("[MarketReview] Notification sent successfully.")
                else:
                    logger.warning("[MarketReview] Notification send failed.")
            elif not send_notification:
                logger.info("[MarketReview] Notification skipped (--no-notify).")

            return review_report

    except Exception as exc:
        logger.error("[MarketReview] Failed: %s", exc)

    return None
