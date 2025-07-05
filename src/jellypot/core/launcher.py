#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PotPlayer 启动器模块
"""

import sys
import subprocess
import urllib.parse
import re
from pathlib import Path
from typing import Optional


class PotPlayerLauncher:
    """PotPlayer 启动器类"""
    
    def __init__(self, potplayer_path: Optional[str] = None):
        """初始化启动器
        
        Args:
            potplayer_path: PotPlayer 可执行文件路径，如果为 None 则自动检测
        """
        self.potplayer_path = potplayer_path or self._detect_potplayer()
    
    def _detect_potplayer(self) -> str:
        """自动检测 PotPlayer 路径"""
        common_paths = [
            r"D:\scoop\apps\potplayer\current\PotPlayerMini64.exe",
            r"C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe",
            r"C:\Program Files (x86)\DAUM\PotPlayer\PotPlayerMini64.exe",
            r"C:\Program Files\PotPlayer\PotPlayerMini64.exe",
            r"C:\Program Files (x86)\PotPlayer\PotPlayerMini64.exe"
        ]
        
        for path in common_paths:
            if Path(path).exists():
                return path
        
        # 默认路径
        return r"C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe"
    
    @staticmethod
    def normalize_path(path_str: str) -> str:
        """标准化路径
        
        Args:
            path_str: 原始路径字符串
            
        Returns:
            标准化后的路径
        """
        if not path_str:
            return ""
        
        # 移除 potplayer:// 协议前缀
        path = path_str.replace("potplayer://", "")
        
        # URL 解码
        path = urllib.parse.unquote(path)
        
        # 清理斜杠和反斜杠
        path = path.replace("///", "\\")
        path = path.replace("\\\\\\\\", "\\")
        path = path.replace("\\\\", "\\")
        path = path.replace("//", "\\")
        
        # 修正磁盘驱动器路径
        path = re.sub(r"^([A-Z]):\\\\", r"\1:\\", path)
        path = re.sub(r"^([A-Z])/", r"\1:\\", path)
        path = re.sub(r"^([A-Z]):", r"\1:\\", path)
        
        # 替换特定的 \\?\\ 路径格式
        path = re.sub(r"([A-Z]):\\\\\\\\\\?\\\\", r"\1:\\", path)
        path = re.sub(r"\\\\\\\\\\?\\\\", "\\", path)
        
        # 将所有剩余的斜杠规范化为反斜杠
        path = path.replace("/", "\\")
        
        return path
    
    def launch(self, media_path: str, silent: bool = True) -> bool:
        """启动 PotPlayer
        
        Args:
            media_path: 媒体文件路径
            silent: 是否静默启动（无控制台窗口）
            
        Returns:
            启动是否成功
        """
        try:
            # 检查 PotPlayer 是否存在
            if not Path(self.potplayer_path).exists():
                if not silent:
                    print(f"错误: PotPlayer 未找到: {self.potplayer_path}")
                return False
            
            # 标准化路径
            normalized_path = self.normalize_path(media_path)
            if not silent:
                print(f"标准化路径: {normalized_path}")
            
            # 构建启动参数
            creation_flags = subprocess.CREATE_NO_WINDOW if silent else 0
            
            # 启动 PotPlayer
            subprocess.Popen(
                [self.potplayer_path, normalized_path],
                creationflags=creation_flags
            )
            
            if not silent:
                print(f"PotPlayer 已启动: {normalized_path}")
            return True
            
        except Exception as e:
            if not silent:
                print(f"启动 PotPlayer 失败: {e}")
            return False


def main():
    """命令行入口函数"""
    if len(sys.argv) < 2:
        print("用法: python -m jellypot.launcher <媒体路径>")
        sys.exit(1)
    
    media_path = sys.argv[1]
    launcher = PotPlayerLauncher()
    success = launcher.launch(media_path, silent=False)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
