# AutoShot C++ Version

AutoShot是一个自动窗口截图工具，能够定时对指定窗口进行截图，裁剪图片上半部分，并使用感知哈希算法检测和删除相似图片。

## 特性

- 通过Windows API调整目标窗口为指定大小
- 每2秒对指定窗口进行定时截图
- 使用OpenCV进行图像处理和感知哈希计算
- 将裁剪后的图片保存到chat_shot目录
- 使用感知哈希算法比较图片相似度
- 删除相似度大于0.9的重复图片
- 支持根据截图坐标查询屏幕像素值
- 更低的资源占用和更高的性能（相比Python版本）

## 系统要求

- Windows操作系统
- C++17兼容编译器 (MSVC, GCC, or Clang)
- CMake 3.10或更高版本
- OpenCV库

## 构建说明

### 安装依赖

1. 安装CMake (https://cmake.org/)
2. 安装OpenCV库：
   - 使用vcpkg: `vcpkg install opencv4`
   - 或从官网下载并配置

### 构建项目

```bash
# 创建构建目录
mkdir build
cd build

# 配置项目
cmake ..

# 构建项目
cmake --build . --config Release
```

## 使用方法

### 命令行使用

```bash
# 连续模式：每2秒截图一次
autoshot_cpp.exe --title "窗口标题" --width 800 --height 600

# 单次模式：只截图一次
autoshot_cpp.exe --title "窗口标题" --width 800 --height 600 --once

# 查询像素值：获取截图中指定坐标的屏幕像素值
autoshot_cpp.exe --title "窗口标题" --width 800 --height 600 --query-pixel 100 50
```

参数说明：
- `--title`: 要截图的窗口标题（必需）
- `--width`: 窗口宽度（必需）
- `--height`: 窗口高度（必需）
- `--interval`: 截图间隔时间（秒，默认为2）
- `--once`: 仅截图一次后退出
- `--query-pixel`: 查询截图中指定坐标的像素值

## 工作流程

1. 查找指定标题的窗口
2. 将窗口调整为指定大小
3. 每隔指定时间截取窗口图片
4. 对截图进行上半部分裁剪
5. 计算新图片与其他已保存图片的感知哈希相似度
6. 如果相似度超过0.9，则删除旧的相似图片
7. 保存新的裁剪图片到chat_shot目录

## 技术细节

- 窗口管理：使用Windows API进行窗口操作
- 图像处理：使用OpenCV进行图像处理和保存
- 相似度检测：使用离散余弦变换(DCT)实现感知哈希算法
- 多线程：使用std::thread实现后台截图功能
- 跨平台准备：代码结构便于未来移植到其他平台

## 性能优势

相比Python版本，C++版本具有以下优势：
- 更低的内存占用
- 更快的执行速度
- 更少的系统资源消耗
- 更稳定的长时间运行性能