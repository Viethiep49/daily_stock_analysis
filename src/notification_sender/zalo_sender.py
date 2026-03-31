# -*- coding: utf-8 -*-
"""
===================================
ZaloSender — Zalo OA Notification (Stub)
===================================

Placeholder for future Zalo Official Account integration.

Status: NOT YET ACTIVE
  - Zalo OA requires an approved business account (paid tier)
  - Webhook / bot API availability depends on Zalo's approval process
  - Until approved, Telegram + Discord are the primary channels

To activate:
  1. Register a Zalo Official Account at: https://oa.zalo.me/
  2. Obtain ZALO_OA_TOKEN from the OA admin panel
  3. Set ZALO_WEBHOOK_URL and ZALO_OA_TOKEN in .env
  4. Implement send() below using the Zalo Notification Service (ZNS) API
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ZaloSender:
    """
    Stub sender for Zalo OA notifications.

    No-op until Zalo OA is approved and configured.
    """

    def __init__(
        self,
        webhook_url: Optional[str] = None,
        oa_token: Optional[str] = None,
    ) -> None:
        self._webhook_url = (webhook_url or "").strip()
        self._oa_token = (oa_token or "").strip()
        if not self.is_configured():
            logger.debug(
                "[ZaloSender] Not configured — ZALO_WEBHOOK_URL / ZALO_OA_TOKEN missing. "
                "Zalo notifications disabled."
            )

    def is_configured(self) -> bool:
        """Return True only when both webhook URL and OA token are provided."""
        return bool(self._webhook_url and self._oa_token)

    def send(self, content: str) -> bool:
        """
        Send a text notification via Zalo OA.

        Args:
            content: Markdown or plain-text message body.

        Returns:
            True on success, False otherwise.
            Currently always returns False (stub — not implemented).
        """
        if not self.is_configured():
            logger.warning("[ZaloSender] send() called but sender is not configured.")
            return False

        # TODO: Implement ZNS API call once Zalo OA is approved
        # POST https://openapi.zalo.me/v2.0/oa/message
        # Headers: {"access_token": self._oa_token}
        # Body: {"recipient": {...}, "message": {"text": content}}
        logger.warning(
            "[ZaloSender] ZNS API integration not yet implemented. "
            "Message NOT sent."
        )
        return False
