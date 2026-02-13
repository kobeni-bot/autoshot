# AutoShot 项目详细文档

## 项目概述
AutoShot 是一个自动窗口截图工具，能够定时对指定窗口进行截图，裁剪图片上半部分，并使用感知哈希算法检测和删除相似图片。此外，它还具备坐标转换功能，可以将截图中的像素坐标映射到屏幕上的实际坐标。

## 核心功能

### 1. 窗口管理
- 通过Windows API查找和定位目标窗口
- 调整窗口至指定尺寸
- 获取窗口在屏幕上的确切坐标（包括窗口矩形和客户区矩形）

### 2. 定时截图
- 每2秒对指定窗口进行截图
- 使用PIL的ImageGrab进行精确截图
- 支持连续截图模式和单次截图模式

### 3. 图像处理
- 自动裁剪截图的上半部分
- 将裁剪后的图片保存到chat_shot目录
- 生成带时间戳的唯一文件名

### 4. 相似度检测
- 使用感知哈希算法检测图片相似度
- 仅与最近的一张图片进行比较以提高性能
- 删除相似度大于0.9的重复图片

### 5. 坐标转换与像素查询（新增功能）
- 将截图坐标转换为屏幕坐标
- 获取屏幕上任意点的RGB颜色值
- 根据截图坐标查询屏幕上的实际像素值

## 技术架构

### 核心模块

#### 1. window_manager.py
负责窗口操作和坐标转换：

- `find_window()` - 通过窗口标题查找窗口句柄
- `resize_window()` - 调整窗口尺寸
- `get_window_rect()` - 获取窗口矩形坐标
- `get_client_rect()` - 获取客户区矩形坐标（不含边框和标题栏）
- `get_pixel_color()` - 获取屏幕上指定坐标的RGB颜色值
- `convert_screenshot_coords_to_screen()` - 将截图坐标转换为屏幕坐标
- `get_pixel_from_screenshot_coords()` - 根据截图坐标获取屏幕像素值

#### 2. image_processor.py
负责图像处理操作：

- `crop_top_half()` - 裁剪图片上半部分
- `save_image()` - 保存图片到输出目录
- `create_unique_filename()` - 生成带时间戳的唯一文件名

#### 3. similarity_detector.py
负责相似度检测：

- `calculate_phash()` - 计算图像的感知哈希
- `compare_images()` - 比较两张图片的相似度
- `find_similar_images()` - 查找相似图片（仅与最近的一张图片比较）

#### 4. main.py
主程序模块，协调所有功能：

- `AutoShot` 类 - 主要业务逻辑
- `capture_screenshot()` - 截图功能
- `get_pixel_at_screenshot_coords()` - 像素查询功能
- 命令行接口

## 关键实现细节

### 坐标转换机制
1. 通过`GetClientRect`获取窗口客户区相对于屏幕的坐标
2. 将截图中的相对坐标(x,y)转换为屏幕绝对坐标(left+x, top+y)
3. 使用`GetPixel` API获取屏幕指定坐标的RGB值

### 性能优化
- 相似度检测仅与最近的一张图片比较，避免与所有历史图片比较
- 使用客户区坐标进行截图，避免捕获窗口边框和标题栏
- 设备上下文的正确获取和释放

### 错误处理
- 窗口不存在时的处理
- 截图失败时的异常处理
- 图片无法打开时的容错机制

## 使用方法

### 命令行使用
```bash
# 连续模式：每2秒截图一次
python -m autoshot.main --title "窗口标题" --width 800 --height 600

# 单次模式：只截图一次
python -m autoshot.main --title "窗口标题" --width 800 --height 600 --once

# 查询像素值：获取截图中指定坐标的屏幕像素值
python -m autoshot.main --title "窗口标题" --width 800 --height 600 --query-pixel 100 50
```

### 编程接口使用
```python
from autoshot.main import AutoShot

# 创建实例
autoshot = AutoShot(window_title="窗口标题", width=800, height=600, interval=2)

# 运行一次
autoshot.run_once()

# 或启动连续截图
autoshot.start_capture_loop()

# 停止连续截图
autoshot.stop_capture_loop()

# 查询像素值
hwnd = autoshot.window_manager.find_window(window_name="窗口标题")
rgb_color = autoshot.get_pixel_at_screenshot_coords(hwnd, 100, 50)
```

## 依赖项
- pywin32: Windows API访问
- Pillow: 图像处理
- imagehash: 感知哈希计算
- numpy, scipy, pywavelets: 支持imagehash

## 文件结构
```
autoshot/
├── __init__.py
├── main.py          # 主程序模块
├── window_manager.py # 窗口管理模块
├── image_processor.py # 图像处理模块
└── similarity_detector.py # 相似度检测模块
chat_shot/           # 截图存储目录
pyproject.toml       # 项目配置文件
README.md           # 项目说明
```

## 工作流程
1. 查找指定标题的窗口
2. 将窗口调整为指定大小
3. 每隔指定时间截取窗口客户区图片
4. 对截图进行上半部分裁剪
5. 计算新图片与最近图片的感知哈希相似度
6. 如果相似度超过0.9，则删除旧的相似图片
7. 保存新的裁剪图片到chat_shot目录
8. 支持根据截图坐标查询屏幕实际像素值

## 注意事项
- 需要在Windows环境下运行
- 需要目标窗口在截图过程中保持可见
- 程序需要足够的权限访问目标窗口
- 像素查询功能基于截图坐标到屏幕坐标的转换