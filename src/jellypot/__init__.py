#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JellyPot - Jellyfin + PotPlayer 整合工具包
"""

__version__ = "0.1.0"
__author__ = "JellyPot Team"
__description__ = "Jellyfin + PotPlayer 整合配置工具"

from .core.launcher import PotPlayerLauncher
from .config.configurator import PPJFConfigurator
from .config.runner import PPJFRunner

__all__ = ["PotPlayerLauncher", "PPJFConfigurator", "PPJFRunner"]
