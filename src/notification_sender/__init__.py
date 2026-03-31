# -*- coding: utf-8 -*-
"""
===================================
Notification Sender Layer
===================================

Primary channels (Vietnam market):
  - Telegram (primary)
  - Discord  (primary)
  - Email/SMTP (optional)
  - Slack (optional)
  - Custom Webhook (optional)
  - Zalo (optional — requires Zalo OA approval)

Removed: WeChat Work, Feishu/Lark, DingTalk, PushPlus, Server酱3, AstrBot, Pushover
"""

from .custom_webhook_sender import CustomWebhookSender
from .discord_sender import DiscordSender
from .email_sender import EmailSender
from .slack_sender import SlackSender
from .telegram_sender import TelegramSender

# Zalo: optional — only import if available
try:
    from .zalo_sender import ZaloSender
    _ZALO_AVAILABLE = True
except ImportError:
    ZaloSender = None
    _ZALO_AVAILABLE = False

__all__ = [
    "CustomWebhookSender",
    "DiscordSender",
    "EmailSender",
    "SlackSender",
    "TelegramSender",
    "ZaloSender",
    "_ZALO_AVAILABLE",
]
