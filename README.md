# EmbodiedPlatform

基于 MuJoCo 物理引擎的履带机器人仿真平台，支持键盘控制移动、鼠标调整视角。

## 功能

- MuJoCo 物理仿真：履带机器人 + 围墙场地
- WASD 控制：W/S 前进后退，A/D 转向
- 鼠标视角：左键旋转、右键平移、滚轮缩放
- ESC 退出

## 环境要求

- Python 3.9+
- 依赖见 `requirements.txt`

推荐用 conda 创建独立环境：

```bash
conda create -n embodied python=3.11 -y
conda activate embodied
pip install -r requirements.txt
```

## 运行

在仓库根目录（即包含 `world.xml` 的目录）下执行：

```bash
python qt_run.py
```

> `qt_run.py` 是主推入口。它基于 PyQt6 封装的 viewer，能可靠跟踪按键按下/释放，实现"按住即动、松开即停"。
> `main.py` 是早期入口，用 MuJoCo 原生 viewer + GLFW 的 REPEAT 事件轮询键盘，存在无法准确检测松键的问题，仅作参考。

## 操作说明

| 按键 / 操作 | 功能 |
|---|---|
| W / S | 前进 / 后退 |
| A / D | 左转 / 右转 |
| 鼠标左键拖动 | 旋转视角 |
| 鼠标右键拖动 | 平移视角 |
| 鼠标滚轮 | 缩放 |
| ESC | 退出 |

## 文件结构

| 文件 | 说明 |
|---|---|
| `qt_run.py` | 运行入口（Qt viewer，主推） |
| `main.py` | 早期入口（原生 MuJoCo viewer，保留参考） |
| `viewer_widget.py` | PyQt6 封装的 MuJoCo 离屏渲染 viewer |
| `world.xml` | 仿真场景：地面、围墙、灯光、履带机器人 |
| `robot_model.xml` | 早期机器人本体模型定义，当前入口未加载 |
| `make_intro_ppt.py` | 生成项目介绍 PPT |
| `make_comparison_ppt.py` | 生成 main.py 与 qt_run.py 对比 PPT |

## 已知限制

- `viewer_widget.py` 的 `paintGL` 每帧重建 `mujoco.Renderer`，CPU 占用偏高，GL 资源未显式释放；后续可改为复用 Renderer 并正确处理 FBO 状态失效。
- 物理场景仅施加推力/扭矩到 base body，未实现真实履带/轮子驱动，仅供演示。
