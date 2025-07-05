#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序入口
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from jellypot.config.configurator import PPJFConfigurator


def main():
    """主函数"""
    try:
        configurator = PPJFConfigurator()
        success = configurator.run()
        
        if success:
            print()
            print("✅ 配置完成!")
            input("按回车键退出...")
        else:
            print("❌ 配置失败!")
            input("按回车键退出...")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print()
        print("❌ 用户取消操作")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        input("按回车键退出...")
        sys.exit(1)


if __name__ == "__main__":
    main()
