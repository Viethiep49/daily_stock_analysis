# -*- coding: utf-8 -*-
"""
===================================
History record endpoints
===================================

Responsibilities:
1. Provide GET /api/v1/history for history list queries
2. Provide GET /api/v1/history/{query_id} for history detail queries
"""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Depends, Body

from api.deps import get_database_manager
from api.v1.schemas.history import (
    HistoryListResponse,
    HistoryItem,
    DeleteHistoryRequest,
    DeleteHistoryResponse,
    NewsIntelItem,
    NewsIntelResponse,
    AnalysisReport,
    ReportMeta,
    ReportSummary,
    ReportStrategy,
    ReportDetails,
    MarkdownReportResponse,
)
from api.v1.schemas.common import ErrorResponse
from src.storage import DatabaseManager
from src.report_language import (
    get_sentiment_label,
    get_localized_stock_name,
    localize_operation_advice,
    localize_trend_prediction,
    normalize_report_language,
)
from src.services.history_service import HistoryService, MarkdownReportGenerationError
from src.utils.data_processing import (
    normalize_model_used,
    extract_fundamental_detail_fields,
    extract_board_detail_fields,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "",
    response_model=HistoryListResponse,
    responses={
        200: {"description": "History record list"},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Get history analysis list",
    description="Paginated retrieval of history analysis record summaries, filterable by stock code and date range"
)
def get_history_list(
    stock_code: Optional[str] = Query(None, description="Stock code filter"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db_manager: DatabaseManager = Depends(get_database_manager)
) -> HistoryListResponse:
    """
    Get history analysis list

    Paginated retrieval of history analysis record summaries, filterable by stock code and date range.

    Args:
        stock_code: Stock code filter
        start_date: Start date
        end_date: End date
        page: Page number
        limit: Items per page
        db_manager: Database manager dependency

    Returns:
        HistoryListResponse: History record list
    """
    try:
        service = HistoryService(db_manager)

        # Uses def rather than async def; FastAPI automatically runs this in a thread pool
        result = service.get_history_list(
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            page=page,
            limit=limit
        )

        # Convert to response model
        items = [
            HistoryItem(
                id=item.get("id"),
                query_id=item.get("query_id", ""),
                stock_code=item.get("stock_code", ""),
                stock_name=item.get("stock_name"),
                report_type=item.get("report_type"),
                sentiment_score=item.get("sentiment_score"),
                operation_advice=item.get("operation_advice"),
                created_at=item.get("created_at")
            )
            for item in result.get("items", [])
        ]

        return HistoryListResponse(
            total=result.get("total", 0),
            page=page,
            limit=limit,
            items=items
        )

    except Exception as e:
        logger.error(f"Failed to query history list: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": f"Failed to query history list: {str(e)}"
            }
        )


@router.delete(
    "",
    response_model=DeleteHistoryResponse,
    responses={
        200: {"description": "Deletion successful"},
        400: {"description": "Invalid request parameters", "model": ErrorResponse},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Delete history analysis records",
    description="Batch delete analysis history records by primary key ID"
)
def delete_history_records(
    request: DeleteHistoryRequest = Body(...),
    db_manager: DatabaseManager = Depends(get_database_manager)
) -> DeleteHistoryResponse:
    """
    Batch delete history analysis records by primary key ID.
    """
    record_ids = sorted({record_id for record_id in request.record_ids if record_id is not None})
    if not record_ids:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_request",
                "message": "record_ids cannot be empty"
            }
        )

    try:
        service = HistoryService(db_manager)
        deleted = service.delete_history_records(record_ids)
        return DeleteHistoryResponse(deleted=deleted)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete history records: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": f"Failed to delete history records: {str(e)}"
            }
        )


@router.get(
    "/{record_id}",
    response_model=AnalysisReport,
    responses={
        200: {"description": "Report details"},
        404: {"description": "Report not found", "model": ErrorResponse},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Get history report details",
    description="Get the complete history analysis report by analysis history record ID or query_id"
)
def get_history_detail(
    record_id: str,
    db_manager: DatabaseManager = Depends(get_database_manager)
) -> AnalysisReport:
    """
    Get history report details

    Retrieves the complete history analysis report by analysis history record primary key ID or query_id.
    Tries integer primary key ID first; falls back to query_id lookup if the parameter is not a valid integer.

    Args:
        record_id: Analysis history record primary key ID (integer) or query_id (string)
        db_manager: Database manager dependency

    Returns:
        AnalysisReport: Complete analysis report

    Raises:
        HTTPException: 404 - Report not found
    """
    try:
        service = HistoryService(db_manager)

        # Try integer ID first, fall back to query_id string lookup
        result = service.resolve_and_get_detail(record_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "not_found",
                    "message": f"No analysis record found for id/query_id={record_id}"
                }
            )

        # Extract price information from context_snapshot
        current_price = None
        change_pct = None
        context_snapshot = result.get("context_snapshot")
        if context_snapshot and isinstance(context_snapshot, dict):
            # Try to get from enhanced_context.realtime
            enhanced_context = context_snapshot.get("enhanced_context") or {}
            realtime = enhanced_context.get("realtime") or {}
            current_price = realtime.get("price")
            change_pct = realtime.get("change_pct") or realtime.get("change_60d")

            # Also try to get from realtime_quote_raw
            if current_price is None:
                realtime_quote_raw = context_snapshot.get("realtime_quote_raw") or {}
                current_price = realtime_quote_raw.get("price")
                change_pct = change_pct or realtime_quote_raw.get("change_pct") or realtime_quote_raw.get("pct_chg")

        raw_result = result.get("raw_result")
        if not isinstance(raw_result, dict):
            raw_result = {}
        report_language = normalize_report_language(
            result.get("report_language")
            or raw_result.get("report_language")
            or (
                context_snapshot.get("report_language")
                if isinstance(context_snapshot, dict)
                else None
            )
        )
        stock_name = get_localized_stock_name(
            result.get("stock_name"),
            result.get("stock_code", ""),
            report_language,
        )

        # Build response model
        meta = ReportMeta(
            id=result.get("id"),
            query_id=result.get("query_id", ""),
            stock_code=result.get("stock_code", ""),
            stock_name=stock_name,
            report_type=result.get("report_type"),
            report_language=report_language,
            created_at=result.get("created_at"),
            current_price=current_price,
            change_pct=change_pct,
            model_used=normalize_model_used(result.get("model_used"))
        )

        summary = ReportSummary(
            analysis_summary=result.get("analysis_summary"),
            operation_advice=localize_operation_advice(
                result.get("operation_advice"),
                report_language,
            ),
            trend_prediction=localize_trend_prediction(
                result.get("trend_prediction"),
                report_language,
            ),
            sentiment_score=result.get("sentiment_score"),
            sentiment_label=(
                get_sentiment_label(result.get("sentiment_score"), report_language)
                if result.get("sentiment_score") is not None
                else result.get("sentiment_label")
            )
        )

        strategy = ReportStrategy(
            ideal_buy=result.get("ideal_buy"),
            secondary_buy=result.get("secondary_buy"),
            stop_loss=result.get("stop_loss"),
            take_profit=result.get("take_profit")
        )

        fallback_fundamental = db_manager.get_latest_fundamental_snapshot(
            query_id=result.get("query_id", ""),
            code=result.get("stock_code", ""),
        )
        extracted_fundamental = extract_fundamental_detail_fields(
            context_snapshot=result.get("context_snapshot"),
            fallback_fundamental_payload=fallback_fundamental,
        )
        extracted_boards = extract_board_detail_fields(
            context_snapshot=result.get("context_snapshot"),
            fallback_fundamental_payload=fallback_fundamental,
        )

        details = ReportDetails(
            news_content=result.get("news_content"),
            raw_result=result.get("raw_result"),
            context_snapshot=result.get("context_snapshot"),
            financial_report=extracted_fundamental.get("financial_report"),
            dividend_metrics=extracted_fundamental.get("dividend_metrics"),
            belong_boards=extracted_boards.get("belong_boards"),
            sector_rankings=extracted_boards.get("sector_rankings"),
        )

        return AnalysisReport(
            meta=meta,
            summary=summary,
            strategy=strategy,
            details=details
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to query history detail: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": f"Failed to query history detail: {str(e)}"
            }
        )


@router.get(
    "/{record_id}/news",
    response_model=NewsIntelResponse,
    responses={
        200: {"description": "News intelligence list"},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Get news associated with a history report",
    description="Get the list of news intelligence associated with a history record ID (returns 200 even if empty)"
)
def get_history_news(
    record_id: str,
    limit: int = Query(20, ge=1, le=100, description="Return count limit"),
    db_manager: DatabaseManager = Depends(get_database_manager)
) -> NewsIntelResponse:
    """
    Get news associated with a history report

    Retrieves the list of news intelligence associated with an analysis history record ID or query_id.
    Resolves record_id to query_id internally.

    Args:
        record_id: Analysis history record primary key ID (integer) or query_id (string)
        limit: Return count limit
        db_manager: Database manager dependency

    Returns:
        NewsIntelResponse: News intelligence list
    """
    try:
        service = HistoryService(db_manager)
        items = service.resolve_and_get_news(record_id=record_id, limit=limit)

        response_items = [
            NewsIntelItem(
                title=item.get("title", ""),
                snippet=item.get("snippet"),
                url=item.get("url", "")
            )
            for item in items
        ]

        return NewsIntelResponse(
            total=len(response_items),
            items=response_items
        )

    except Exception as e:
        logger.error(f"Failed to query news intelligence: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": f"Failed to query news intelligence: {str(e)}"
            }
        )


@router.get(
    "/{record_id}/markdown",
    response_model=MarkdownReportResponse,
    responses={
        200: {"description": "Markdown format report"},
        404: {"description": "Report not found", "model": ErrorResponse},
        500: {"description": "Server error", "model": ErrorResponse},
    },
    summary="Get history report in Markdown format",
    description="Get the complete analysis report in Markdown format by analysis history record ID"
)
def get_history_markdown(
    record_id: str,
    db_manager: DatabaseManager = Depends(get_database_manager)
) -> MarkdownReportResponse:
    """
    Get the Markdown format content of a history report

    Generates a Markdown report consistent with the push notification format,
    identified by analysis history record ID or query_id.

    Args:
        record_id: Analysis history record primary key ID (integer) or query_id (string)
        db_manager: Database manager dependency

    Returns:
        MarkdownReportResponse: Complete report in Markdown format

    Raises:
        HTTPException: 404 - Report not found
        HTTPException: 500 - Report generation failed (internal server error)
    """
    service = HistoryService(db_manager)

    try:
        markdown_content = service.get_markdown_report(record_id)
    except MarkdownReportGenerationError as e:
        logger.error(f"Markdown report generation failed for {record_id}: {e.message}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "generation_failed",
                "message": f"Failed to generate Markdown report: {e.message}"
            }
        )
    except Exception as e:
        logger.error(f"Failed to get Markdown report: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": f"Failed to get Markdown report: {str(e)}"
            }
        )

    if markdown_content is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"No analysis record found for id/query_id={record_id}"
            }
        )

    return MarkdownReportResponse(content=markdown_content)
