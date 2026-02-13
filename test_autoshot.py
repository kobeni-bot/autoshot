"""
Test script for AutoShot
This script demonstrates how to use the AutoShot functionality
"""
import sys
import time
from autoshot.main import AutoShot


def test_autoshot():
    print("AutoShot 测试脚本")
    print("=" * 40)
    
    # 提供一些使用示例
    print("使用示例:")
    print("1. 命令行使用:")
    print("   python -m autoshot.main --title \"记事本\" --width 800 --height 600")
    print("")
    print("2. 编程方式使用:")
    print("   autoshot = AutoShot('记事本', 800, 600, 2)")
    print("   autoshot.run_once()")
    print("")
    print("3. 连续截图模式:")
    print("   autoshot.start_capture_loop()")
    print("   # 运行一段时间后停止")
    print("   autoshot.stop_capture_loop()")
    print("")
    print("注意事项:")
    print("- 请确保提供正确的窗口标题")
    print("- 确保目标窗口在截图期间保持可见")
    print("- 图片将保存在 chat_shot 目录中")


if __name__ == "__main__":
    test_autoshot()