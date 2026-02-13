# AutoShot API 说明文档

## 概述
本文档详细介绍了AutoShot项目的API接口，包括各模块的功能、方法和使用方法。

## 模块结构

### 1. window_manager.py

#### WindowManager 类

##### 构造函数
```python
wm = WindowManager()
```
创建一个新的WindowManager实例。

##### 方法

**find_window(class_name=None, window_name=None)**
- 功能：通过类名或窗口标题查找窗口
- 参数：
  - class_name (str, optional): 窗口类名
  - window_name (str, optional): 窗口标题
- 返回：窗口句柄(int) 或 None

**resize_window(hwnd, width, height)**
- 功能：调整窗口尺寸
- 参数：
  - hwnd (int): 窗口句柄
  - width (int): 目标宽度
  - height (int): 目标高度
- 返回：成功返回True，否则返回False

**get_window_rect(hwnd)**
- 功能：获取窗口矩形坐标
- 参数：hwnd (int): 窗口句柄
- 返回：元组(left, top, right, bottom) 或 None

**get_client_rect(hwnd)**
- 功能：获取客户区矩形坐标（不含边框和标题栏）
- 参数：hwnd (int): 窗口句柄
- 返回：元组(left, top, right, bottom) 或 None

**get_pixel_color(x, y)**
- 功能：获取屏幕上指定坐标的RGB颜色值
- 参数：
  - x (int): 屏幕X坐标
  - y (int): 屏幕Y坐标
- 返回：元组(R, G, B) 或 None

**convert_screenshot_coords_to_screen(hwnd, screenshot_x, screenshot_y, use_client_area=True)**
- 功能：将截图坐标转换为屏幕坐标
- 参数：
  - hwnd (int): 窗口句柄
  - screenshot_x (int): 截图中的X坐标
  - screenshot_y (int): 截图中的Y坐标
  - use_client_area (bool): 是否使用客户区坐标
- 返回：元组(screen_x, screen_y) 或 None

**get_pixel_from_screenshot_coords(hwnd, screenshot_x, screenshot_y, use_client_area=True)**
- 功能：根据截图坐标获取屏幕上的像素颜色
- 参数：
  - hwnd (int): 窗口句柄
  - screenshot_x (int): 截图中的X坐标
  - screenshot_y (int): 截图中的Y坐标
  - use_client_area (bool): 是否使用客户区坐标
- 返回：元组(R, G, B) 或 None

### 2. image_processor.py

#### ImageProcessor 类

##### 构造函数
```python
ip = ImageProcessor(output_dir="chat_shot")
```
- 参数：output_dir (str): 输出目录路径

##### 方法

**crop_top_half(image)**
- 功能：裁剪图片的上半部分
- 参数：image (PIL.Image): 输入图片
- 返回：裁剪后的PIL.Image对象

**save_image(image, filename)**
- 功能：保存图片到输出目录
- 参数：
  - image (PIL.Image): 要保存的图片
  - filename (str): 文件名
- 返回：保存的完整路径

**create_unique_filename(prefix="screenshot", extension=".png")**
- 功能：创建带时间戳的唯一文件名
- 参数：
  - prefix (str): 文件名前缀
  - extension (str): 文件扩展名
- 返回：唯一文件名字符串

### 3. similarity_detector.py

#### SimilarityDetector 类

##### 构造函数
```python
sd = SimilarityDetector(threshold=0.9)
```
- 参数：threshold (float): 相似度阈值（0-1之间）

##### 方法

**calculate_phash(image)**
- 功能：计算图片的感知哈希
- 参数：image (PIL.Image): 输入图片
- 返回：感知哈希值

**compare_images(hash1, hash2)**
- 功能：比较两个图片哈希的相似度
- 参数：
  - hash1: 第一个图片哈希
  - hash2: 第二个图片哈希
- 返回：相似度比例（0-1之间）

**find_similar_images(image_path, comparison_dir)**
- 功能：查找相似图片（仅与最近的一张图片比较）
- 参数：
  - image_path (str): 参考图片路径
  - comparison_dir (str): 比较目录路径
- 返回：相似图片路径列表

**has_similar_image(image_path, comparison_dir)**
- 功能：检查是否存在相似图片
- 参数：
  - image_path (str): 参考图片路径
  - comparison_dir (str): 比较目录路径
- 返回：存在相似图片返回True，否则返回False

### 4. main.py

#### AutoShot 类

##### 构造函数
```python
autoshot = AutoShot(window_title, width, height, interval=2)
```
- 参数：
  - window_title (str): 窗口标题
  - width (int): 窗口宽度
  - height (int): 窗口高度
  - interval (int): 截图间隔（秒）

##### 方法

**setup_window()**
- 功能：查找并调整窗口尺寸
- 返回：成功返回True，否则返回False

**capture_screenshot(hwnd)**
- 功能：对指定窗口截图
- 参数：hwnd (int): 窗口句柄
- 返回：保存的图片路径或None

**get_pixel_at_screenshot_coords(hwnd, screenshot_x, screenshot_y)**
- 功能：获取截图中指定坐标的屏幕像素值
- 参数：
  - hwnd (int): 窗口句柄
  - screenshot_x (int): 截图中的X坐标
  - screenshot_y (int): 截图中的Y坐标
- 返回：元组(R, G, B) 或 None

**single_capture_cycle()**
- 功能：执行单次截图循环
- 返回：成功返回True，否则返回False

**start_capture_loop()**
- 功能：开始连续截图循环

**stop_capture_loop()**
- 功能：停止连续截图循环

**run_once()**
- 功能：执行单次截图并退出

## 命令行接口

### 基本用法
```bash
python -m autoshot.main [OPTIONS]
```

### 选项
- `--title TITLE` (必需): 目标窗口标题
- `--width WIDTH` (必需): 目标窗口宽度
- `--height HEIGHT` (必需): 目标窗口高度
- `--interval INTERVAL` (可选): 截图间隔（默认2秒）
- `--once` (可选): 单次模式
- `--query-pixel X Y` (可选): 查询截图中指定坐标的像素值

### 示例
```bash
# 连续截图
python -m autoshot.main --title "记事本" --width 800 --height 600

# 单次截图
python -m autoshot.main --title "记事本" --width 800 --height 600 --once

# 查询像素值
python -m autoshot.main --title "记事本" --width 800 --height 600 --query-pixel 100 50
```

## 使用示例

### 基本截图功能
```python
from autoshot.main import AutoShot

# 创建实例
autoshot = AutoShot("记事本", 800, 600)

# 单次截图
autoshot.run_once()

# 连续截图
autoshot.start_capture_loop()
# ... 一段时间后 ...
autoshot.stop_capture_loop()
```

### 像素查询功能
```python
from autoshot.main import AutoShot

autoshot = AutoShot("记事本", 800, 600)
hwnd = autoshot.window_manager.find_window(window_name="记事本")

# 查询截图中坐标(100, 50)对应的屏幕像素
rgb_value = autoshot.get_pixel_at_screenshot_coords(hwnd, 100, 50)
if rgb_value:
    r, g, b = rgb_value
    print(f"屏幕像素RGB值: ({r}, {g}, {b})")
```

### 高级用法
```python
from autoshot.window_manager import WindowManager
from autoshot.image_processor import ImageProcessor
from autoshot.similarity_detector import SimilarityDetector

# 分别使用各个组件
wm = WindowManager()
ip = ImageProcessor()
sd = SimilarityDetector(threshold=0.85)

# 查找窗口
hwnd = wm.find_window(window_name="记事本")
if hwnd:
    # 获取窗口坐标
    rect = wm.get_client_rect(hwnd)
    print(f"窗口坐标: {rect}")
    
    # 进行截图（需要使用PIL的ImageGrab）
    from PIL import ImageGrab
    if rect:
        left, top, right, bottom = rect
        bbox = (left, top, right, bottom)
        screenshot = ImageGrab.grab(bbox=bbox)
        
        # 裁剪上半部分
        cropped = ip.crop_top_half(screenshot)
        
        # 保存图片
        filepath = ip.save_image(cropped, ip.create_unique_filename())
        
        print(f"截图已保存: {filepath}")
```