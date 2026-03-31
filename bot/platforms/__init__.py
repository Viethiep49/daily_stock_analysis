# -*- coding: utf-8 -*-
"""
===================================
Bot Platform Adapters
===================================

Supported platforms (Vietnam market):
  - Discord: Primary bot platform
  - (Future) Zalo OA: when Zalo bot API is approved

Removed: DingTalk, DingTalk Stream, Feishu/Lark Stream
"""

from bot.platforms.base import BotPlatform
from bot.platforms.discord import DiscordPlatform

# Available platforms (webhook mode)
ALL_PLATFORMS = {
    "discord": DiscordPlatform,
}

__all__ = [
    "BotPlatform",
    "DiscordPlatform",
    "ALL_PLATFORMS",
]
