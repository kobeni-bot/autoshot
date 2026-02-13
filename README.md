# AutoShot

AutoShot是一个自动窗口截图工具，能够定时对指定窗口进行截图，裁剪图片上半部分，并使用感知哈希算法检测和删除相似图片。

## 功能特性

- 通过Windows API调整目标窗口为指定大小
- 每2秒对指定窗口进行定时截图
- 使用Pillow对截图进行预定义裁剪（保留上半部分）
- 将裁剪后的图片保存到chat_shot目录
- 使用感知哈希算法比较图片相似度
- 删除相似度大于0.9的重复图片

## 系统要求

- Windows操作系统
- Python 3.8 或更高版本
- uv 包管理器

## 安装

1. 克隆或下载项目
2. 在项目根目录下运行以下命令创建虚拟环境并安装依赖：

```bash
uv venv
uv sync
```

## 使用方法

### 命令行使用

```bash
# 连续模式：每2秒截图一次
python -m autoshot.main --title "窗口标题" --width 800 --height 600

# 单次模式：只截图一次
python -m autoshot.main --title "窗口标题" --width 800 --height 600 --once
```

参数说明：
- `--title`：要截图的窗口标题（必需）
- `--width`：窗口宽度（必需）
- `--height`：窗口高度（必需）
- `--interval`：截图间隔时间（秒，默认为2）
- `--once`：仅截图一次后退出

### 作为模块使用

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
```

## 工作流程

1. 查找指定标题的窗口
2. 将窗口调整为指定大小
3. 每隔指定时间截取窗口图片
4. 对截图进行上半部分裁剪
5. 计算新图片与其他已保存图片的感知哈希相似度
6. 如果相似度超过0.9，则删除旧的相似图片
7. 保存新的裁剪图片到chat_shot目录

## 目录结构

- `autoshot/` - 主要源代码目录
- `chat_shot/` - 截图保存目录（自动生成）
- `pyproject.toml` - 项目依赖配置
- `.gitignore` - Git忽略文件配置

## 注意事项

- 请确保目标窗口在截图过程中保持可见
- 程序需要足够的权限来访问目标窗口
- 保存的截图将位于项目根目录下的chat_shot文件夹中