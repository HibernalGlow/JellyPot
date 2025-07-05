#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JellyPot 命令行入口
"""

import sys
from jellypot.core.launcher import main as launcher_main


def main():
    """主入口函数"""
    launcher_main()


if __name__ == "__main__":
    main()
