"""
AutoShot 10秒截图测试
此脚本将启动AutoShot进行10秒的截图测试
"""
import time
from autoshot.main import AutoShot
import threading


def screenshot_test():
    print("开始AutoShot 10秒截图测试...")
    print("请注意：此测试需要一个有效的窗口标题才能正常运行")
    print("示例窗口标题可能包括：'记事本'、'计算器'、'任务管理器'等")
    print("-" * 50)
    
    # 这里我们使用一个示例窗口标题，但在实际运行时您需要替换为存在的窗口标题
    window_title = input("请输入要截图的窗口标题（例如：记事本）: ").strip()
    
    if not window_title:
        print("未提供窗口标题，使用默认值 '无标题 - 记事本' 作为示例")
        window_title = "无标题 - 记事本"
    
    # 创建AutoShot实例
    autoshot = AutoShot(window_title, 400, 1600, 2)  # 每2秒截图一次
    
    print(f"正在查找窗口: {window_title}")
    
    # 设置窗口大小
    if not autoshot.setup_window():
        print(f"错误：无法找到或设置窗口 '{window_title}'")
        print("请确保窗口存在且可见")
        return
    
    print("窗口设置成功，开始10秒截图测试...")
    
    # 启动连续截图
    autoshot.start_capture_loop()
    
    # 运行10秒
    time.sleep(150)
    
    # 停止截图
    autoshot.stop_capture_loop()
    
    print("10秒截图测试完成！")
    print("截图已保存到 chat_shot 目录中")
    print("相似度高于0.9的重复图片已被自动删除")


if __name__ == "__main__":
    screenshot_test()