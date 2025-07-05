#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JellyPot 快速测试脚本
"""

import sys
from pathlib import Path

# 添加 src 到路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_launcher():
    """测试启动器"""
    print("🔬 测试 PotPlayer 启动器...")
    try:
        from jellypot.core.launcher import PotPlayerLauncher
        
        launcher = PotPlayerLauncher()
        print(f"✅ 启动器初始化成功")
        print(f"📍 PotPlayer 路径: {launcher.potplayer_path}")
        
        # 测试路径标准化
        test_path = "potplayer://d:/test.mp4"
        normalized = launcher.normalize_path(test_path)
        print(f"🔄 路径标准化测试: {test_path} -> {normalized}")
        
        return True
    except Exception as e:
        print(f"❌ 启动器测试失败: {e}")
        return False

def test_configurator():
    """测试配置器"""
    print("🔬 测试配置器...")
    try:
        from jellypot.config.configurator import PPJFConfigurator
        
        configurator = PPJFConfigurator()
        print(f"✅ 配置器初始化成功")
        print(f"📁 配置目录: {configurator.config_dir}")
        print(f"📁 脚本目录: {configurator.scripts_dir}")
        
        # 测试软件检测
        detected = configurator.detect_software_paths()
        print(f"🔍 检测到的软件: {list(detected.keys())}")
        
        return True
    except Exception as e:
        print(f"❌ 配置器测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 JellyPot 功能测试")
    print("=" * 50)
    
    success = True
    
    # 测试启动器
    success &= test_launcher()
    print()
    
    # 测试配置器
    success &= test_configurator()
    print()
    
    if success:
        print("🎉 所有测试通过!")
        print("✅ 项目结构正确，功能正常")
    else:
        print("❌ 部分测试失败!")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
