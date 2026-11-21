# -*- coding: utf-8 -*-
"""生成 EmbodiedPlatform 项目功能介绍 PPT。"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------- 配色 ----------
PRIMARY = RGBColor(0x1F, 0x3A, 0x5F)   # 深蓝
ACCENT  = RGBColor(0xE8, 0x7A, 0x33)   # 橙
TEAL    = RGBColor(0x2A, 0x9D, 0x8F)   # 青
LIGHT   = RGBColor(0xF4, 0xF6, 0xFA)   # 浅底
CARD    = RGBColor(0xFF, 0xFF, 0xFF)   # 卡片白
DARK    = RGBColor(0x22, 0x2B, 0x3A)   # 深字
GRAY    = RGBColor(0x6B, 0x72, 0x80)   # 灰字
LINE    = RGBColor(0xD8, 0xDE, 0xE6)   # 分割线
FONT    = "微软雅黑"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = prs.slide_width, prs.slide_height


def slide():
    return prs.slides.add_slide(BLANK)


def _set_font(run, size, color, bold=False, name=FONT):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color


def rect(s, l, t, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
    sp = s.shapes.add_shape(shape, l, t, w, h)
    sp.fill.solid()
    sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(0.75)
    sp.shadow.inherit = False
    return sp


def text(s, l, t, w, h, lines, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """lines: list of (text, size, color, bold) 或 ((text, ...), level)"""
    tb = s.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Pt(2); tf.margin_right = Pt(2)
    tf.margin_top = Pt(1); tf.margin_bottom = Pt(1)
    first = True
    for item in lines:
        t_, sz, col, bold = item[:4]
        lvl = item[4] if len(item) > 4 else 0
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        p.level = lvl
        r = p.add_run()
        r.text = t_
        _set_font(r, sz, col, bold)
    return tb


def header(s, title, page):
    rect(s, 0, 0, SW, Inches(1.05), PRIMARY)
    rect(s, 0, Inches(1.05), SW, Inches(0.06), ACCENT)
    text(s, Inches(0.6), Inches(0.12), Inches(10), Inches(0.8),
         [(title, 26, RGBColor(0xFF, 0xFF, 0xFF), True)],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, SW - Inches(1.1), Inches(0.12), Inches(0.7), Inches(0.8),
         [(str(page), 14, RGBColor(0xCF, 0xDB, 0xEA), False)],
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def footer(s):
    text(s, Inches(0.6), SH - Inches(0.45), Inches(6), Inches(0.3),
         [("EmbodiedPlatform · 履带机器人仿真平台", 9, GRAY, False)])


def card(s, l, t, w, h, title, lines, accent=ACCENT, body_size=14):
    rect(s, l, t, w, h, CARD, line=LINE)
    rect(s, l, t, Inches(0.08), h, accent)  # 左色条
    inner_l = l + Inches(0.22)
    text(s, inner_l, t + Inches(0.14), w - Inches(0.4), Inches(0.4),
         [(title, 15, PRIMARY, True)])
    rows = [(ln, body_size, DARK, False) for ln in lines]
    text(s, inner_l, t + Inches(0.6), w - Inches(0.4), h - Inches(0.7), rows)


def bullets(s, l, t, w, h, items, size=14, color=DARK, gap=6):
    tb = s.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for it in items:
        if isinstance(it, str):
            t_, lvl = it, 0
        else:
            t_ = it[0]
            lvl = it[1] if len(it) > 1 else 0
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.level = lvl
        p.space_after = Pt(gap)
        r = p.add_run()
        bullet = "● " if lvl == 0 else "– "
        r.text = bullet + t_
        _set_font(r, size if lvl == 0 else size - 1,
                  color if lvl == 0 else GRAY, lvl == 0)
    return tb


# ============================================================
# Slide 1 — 封面
# ============================================================
s = slide()
rect(s, 0, 0, SW, SH, PRIMARY)
rect(s, 0, Inches(4.55), SW, Inches(0.10), ACCENT)
rect(s, Inches(0.9), Inches(3.7), Inches(0.9), Inches(0.10), TEAL)
text(s, Inches(0.9), Inches(2.0), Inches(11.5), Inches(1.3),
     [("EmbodiedPlatform", 52, RGBColor(0xFF, 0xFF, 0xFF), True)])
text(s, Inches(0.9), Inches(3.95), Inches(11.5), Inches(0.6),
     [("基于 MuJoCo 的履带机器人仿真平台", 24, RGBColor(0xCF, 0xDB, 0xEA), False)])
text(s, Inches(0.9), Inches(4.8), Inches(11.5), Inches(0.5),
     [("物理仿真 · 键盘遥操 · 3D 相机交互 · 可扩展场景", 15, RGBColor(0x9F, 0xB3, 0xCC), False)])
text(s, Inches(0.9), Inches(6.7), Inches(11.5), Inches(0.4),
     [("功能介绍文档", 12, RGBColor(0x8A, 0x9D, 0xB8), False)])


# ============================================================
# Slide 2 — 项目概览
# ============================================================
s = slide()
header(s, "项目概览", 2)
footer(s)
text(s, Inches(0.6), Inches(1.4), Inches(6.6), Inches(1.6),
     [("一个轻量级的履带机器人 (tracked robot) 物理仿真演示，", 16, DARK, False),
      ("基于 MuJoCo 引擎，Python 实现，支持键盘遥操与 3D 相机交互。", 16, DARK, False),
      ("项目结构清晰，核心仅 4 个文件，便于学习与二次开发。", 16, DARK, False)])
# 右侧文件卡片
files = [
    ("main.py", "主程序入口；启动 MuJoCo 原生 viewer，键盘控制机器人"),
    ("viewer_widget.py", "自研 PyQt6+OpenGL 嵌入式 viewer 组件（备用方案）"),
    ("robot_model.xml", "机器人本体模型定义（含 motor / 触碰传感器）"),
    ("world.xml", "完整场景：地面+墙+灯+机器人（main.py 实际加载）"),
]
for i, (fn, desc) in enumerate(files):
    y = Inches(1.4 + i * 1.35)
    rect(s, Inches(7.5), y, Inches(5.3), Inches(1.2), CARD, line=LINE)
    rect(s, Inches(7.5), y, Inches(0.08), Inches(1.2), TEAL)
    text(s, Inches(7.75), y + Inches(0.12), Inches(5), Inches(0.4),
         [(fn, 15, PRIMARY, True)])
    text(s, Inches(7.75), y + Inches(0.55), Inches(5), Inches(0.6),
         [(desc, 12, GRAY, False)])
text(s, Inches(0.6), Inches(3.4), Inches(6.6), Inches(0.5),
     [("运行方式", 15, PRIMARY, True)])
bullets(s, Inches(0.6), Inches(3.85), Inches(6.6), Inches(2.8), [
    "在项目目录下执行 python main.py",
    "加载 world.xml → 初始化物理 → 弹出 3D viewer",
    "键盘 WASD 控制移动，鼠标控制相机视角",
], size=13, gap=8)


# ============================================================
# Slide 3 — 技术栈
# ============================================================
s = slide()
header(s, "技术栈", 3)
footer(s)
stack = [
    ("MuJoCo", "物理仿真引擎：刚体动力学、碰撞、摩擦", PRIMARY),
    ("Python 3", "主开发语言，3.12 运行环境", TEAL),
    ("PyQt6", "嵌入式 viewer 的 GUI 框架（备用方案）", ACCENT),
    ("PyOpenGL", "将 MuJoCo 渲染结果贴到 Qt 画布", PRIMARY),
    ("NumPy", "向量/矩阵运算，力与坐标变换", TEAL),
    ("glfw", "原生 viewer 的窗口与键盘事件处理", ACCENT),
]
cw, ch = Inches(3.9), Inches(2.5)
gx, gy = Inches(0.4), Inches(0.35)
ox, oy = Inches(0.6), Inches(1.5)
for i, (name, desc, col) in enumerate(stack):
    r, c = divmod(i, 3)
    x = ox + c * (cw + gx)
    y = oy + r * (ch + gy)
    rect(s, x, y, cw, ch, CARD, line=LINE)
    rect(s, x, y, cw, Inches(0.12), col)
    text(s, x + Inches(0.3), y + Inches(0.35), cw - Inches(0.6), Inches(0.7),
         [(name, 22, col, True)])
    text(s, x + Inches(0.3), y + Inches(1.15), cw - Inches(0.6), Inches(1.2),
         [(desc, 13, DARK, False)])


# ============================================================
# Slide 4 — 系统架构
# ============================================================
s = slide()
header(s, "系统架构：两条渲染路线", 4)
footer(s)
text(s, Inches(0.6), Inches(1.3), Inches(12), Inches(0.5),
     [("项目提供两种 viewer 方案：主程序使用原生被动 viewer，另保留一套可嵌入 Qt 应用的自研组件。", 14, GRAY, False)])
# 左卡
card(s, Inches(0.6), Inches(2.0), Inches(6.0), Inches(4.8),
     "路线一：原生被动 Viewer（main.py 在用）", [
         "launch_passive 启动 MuJoCo 自带 viewer",
         "主循环手动 mj_step + viewer.sync()",
         "键盘事件经 glfw 回调收集",
         "鼠标交互由引擎自带处理",
         "独立窗口，开箱即用",
     ], accent=ACCENT, body_size=14)
# 右卡
card(s, Inches(6.85), Inches(2.0), Inches(6.0), Inches(4.8),
     "路线二：PyQt6 嵌入式 Viewer（备用）", [
         "MuJoCoViewer 继承 QOpenGLWidget",
         "Renderer 离屏渲染 → 上传 GL 纹理 → 贴图",
         "QTimer 每 16ms 驱动 (~60fps)",
         "自实现相机：左键转/右键平移/滚轮缩放",
         "可集成进更大的 Qt 应用",
     ], accent=TEAL, body_size=14)


# ============================================================
# Slide 5 — 机器人模型
# ============================================================
s = slide()
header(s, "机器人模型", 5)
footer(s)
text(s, Inches(0.6), Inches(1.3), Inches(12), Inches(0.5),
     [("由 XML 描述的履带机器人，含飘浮基座、履带、四轮与传感器塔。", 14, GRAY, False)])
bullets(s, Inches(0.6), Inches(2.0), Inches(6.6), Inches(4.5), [
    "base 本体：box 几何，质量 5kg，freejoint 六自由度飘浮",
    "左右两条履带 track：box 表示，质量各 1kg",
    "四个轮子 lf/lr/rf/rr：cylinder，质量各 0.3kg",
    "传感器塔 tower：cylinder 立柱 + 红色 sensor_ball",
    "robot_model.xml 另含 motor 执行器与 touch 触碰传感器",
], size=14, gap=10)
# 右侧参数表
tx, ty = Inches(7.6), Inches(2.0)
rows = [
    ("部件", "类型", "质量"),
    ("车身 base", "box", "5 kg"),
    ("履带 track ×2", "box", "1 kg"),
    ("轮子 ×4", "cylinder", "0.3 kg"),
    ("传感器塔", "cylinder", "0.3 kg"),
    ("传感器球", "sphere", "—"),
]
from pptx.util import Emu
tbl_h = Inches(0.42)
gtbl = s.shapes.add_table(len(rows), 3, tx, ty, Inches(5.2), Inches(len(rows)*0.42)).table
gtbl.columns[0].width = Inches(2.0)
gtbl.columns[1].width = Inches(1.7)
gtbl.columns[2].width = Inches(1.5)
for ri, row in enumerate(rows):
    for ci, val in enumerate(row):
        cell = gtbl.cell(ri, ci)
        cell.margin_left = Pt(6); cell.margin_right = Pt(4)
        cell.margin_top = Pt(2); cell.margin_bottom = Pt(2)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.text = val
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = val
        if ri == 0:
            cell.fill.solid(); cell.fill.fore_color.rgb = PRIMARY
            _set_font(r, 12, RGBColor(0xFF, 0xFF, 0xFF), True)
        else:
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT if ri % 2 else CARD
            _set_font(r, 12, DARK, False)


# ============================================================
# Slide 6 — 仿真场景
# ============================================================
s = slide()
header(s, "仿真场景 (world.xml)", 6)
footer(s)
text(s, Inches(0.6), Inches(1.3), Inches(12), Inches(0.5),
     [("一个 20×20 的封闭场地，带地面、围墙与灯光，构成完整仿真世界。", 14, GRAY, False)])
scene = [
    ("棋盘格地面", "plane 类型，20×20，checker 纹理", PRIMARY),
    ("四面围墙", "box 墙体，限定活动范围，质量 100kg", TEAL),
    ("两盏灯光", "顶光 + 侧光，diffuse+ambient 环境光", ACCENT),
    ("物理参数", "重力 9.81，timestep 0.002，Euler 积分", PRIMARY),
]
for i, (t_, d, col) in enumerate(scene):
    y = Inches(2.0 + i * 1.25)
    rect(s, Inches(0.6), y, Inches(12.1), Inches(1.1), CARD, line=LINE)
    rect(s, Inches(0.6), y, Inches(0.1), Inches(1.1), col)
    text(s, Inches(0.95), y + Inches(0.14), Inches(3.5), Inches(0.8),
         [(t_, 17, col, True)], anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(4.6), y + Inches(0.14), Inches(8), Inches(0.8),
         [(d, 14, DARK, False)], anchor=MSO_ANCHOR.MIDDLE)


# ============================================================
# Slide 7 — 工作原理：仿真循环
# ============================================================
s = slide()
header(s, "工作原理：仿真主循环", 7)
footer(s)
steps = [
    ("加载 XML", "from_xml_path"),
    ("建状态", "MjData"),
    ("前向计算", "mj_forward"),
    ("读键盘", "keys_pressed"),
    ("施加力", "qfrc_applied"),
    ("步进物理", "mj_step"),
    ("刷新画面", "viewer.sync"),
]
n = len(steps)
bw, bh = Inches(1.55), Inches(1.4)
total_w = n * bw + (n - 1) * Inches(0.15)
start_x = (SW - total_w) / 2
y = Inches(2.4)
for i, (t_, d) in enumerate(steps):
    x = start_x + i * (bw + Inches(0.15))
    rect(s, x, y, bw, bh, PRIMARY if i % 2 == 0 else TEAL,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x, y + Inches(0.22), bw, Inches(0.5),
         [(t_, 14, RGBColor(0xFF, 0xFF, 0xFF), True)], align=PP_ALIGN.CENTER)
    text(s, x, y + Inches(0.75), bw, Inches(0.4),
         [(d, 10, RGBColor(0xE6, 0xED, 0xF6), False)], align=PP_ALIGN.CENTER)
    if i < n - 1:
        ar = rect(s, x + bw - Inches(0.02), y + Inches(0.5), Inches(0.18), Inches(0.4),
                  ACCENT, shape=MSO_SHAPE.RIGHT_ARROW)
text(s, Inches(0.6), Inches(4.2), Inches(12.1), Inches(0.5),
     [("关键设计：控制不依赖 actuator/motor，而是直接对 base body 施加力与力矩。", 14, DARK, True)])
bullets(s, Inches(0.6), Inches(4.8), Inches(12.1), Inches(2.0), [
    "W/S 沿机体局部 Y 轴施力 (forward_speed=8) → 前进/后退",
    "A/D 绕 Z 轴施力矩 (turn_torque=6) → 左转/右转",
    "力经 base 旋转矩阵转到世界系，mj_applyFT 转为广义力 qfrc",
    "累加到 qfrc_applied 后 mj_step 推进物理 —— 等价于整体推着机器人走",
], size=13, gap=7)


# ============================================================
# Slide 8 — 交互控制
# ============================================================
s = slide()
header(s, "交互控制", 8)
footer(s)
# 左：键盘
rect(s, Inches(0.6), Inches(1.5), Inches(6.0), Inches(5.3), CARD, line=LINE)
rect(s, Inches(0.6), Inches(1.5), Inches(6.0), Inches(0.6), PRIMARY)
text(s, Inches(0.6), Inches(1.5), Inches(6.0), Inches(0.6),
     [("  键盘控制 (WASD)", 16, RGBColor(0xFF, 0xFF, 0xFF), True)],
     anchor=MSO_ANCHOR.MIDDLE)
keys = [("W", "前进 Forward"), ("S", "后退 Backward"),
        ("A", "左转 Turn Left"), ("D", "右转 Turn Right"),
        ("ESC", "退出 Quit")]
for i, (k, d) in enumerate(keys):
    y = Inches(2.4 + i * 0.78)
    rect(s, Inches(1.0), y, Inches(1.2), Inches(0.6), ACCENT,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, Inches(1.0), y, Inches(1.2), Inches(0.6),
         [(k, 16, RGBColor(0xFF, 0xFF, 0xFF), True)],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(2.5), y, Inches(3.8), Inches(0.6),
         [(d, 14, DARK, False)], anchor=MSO_ANCHOR.MIDDLE)
# 右：鼠标
rect(s, Inches(6.85), Inches(1.5), Inches(6.0), Inches(5.3), CARD, line=LINE)
rect(s, Inches(6.85), Inches(1.5), Inches(6.0), Inches(0.6), TEAL)
text(s, Inches(6.85), Inches(1.5), Inches(6.0), Inches(0.6),
     [("  鼠标相机控制", 16, RGBColor(0xFF, 0xFF, 0xFF), True)],
     anchor=MSO_ANCHOR.MIDDLE)
ms = [("左键拖拽", "旋转相机方位 / 俯仰"),
      ("右键拖拽", "平移相机视角中心"),
      ("滚轮", "缩放相机距离"),
      ("组合", "自由观察机器人各角度")]
for i, (k, d) in enumerate(ms):
    y = Inches(2.7 + i * 0.95)
    rect(s, Inches(7.3), y, Inches(1.9), Inches(0.6), PRIMARY,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, Inches(7.3), y, Inches(1.9), Inches(0.6),
         [(k, 14, RGBColor(0xFF, 0xFF, 0xFF), True)],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(9.5), y, Inches(3.2), Inches(0.6),
         [(d, 14, DARK, False)], anchor=MSO_ANCHOR.MIDDLE)


# ============================================================
# Slide 9 — 两种 Viewer 对比
# ============================================================
s = slide()
header(s, "两种 Viewer 对比", 9)
footer(s)
cmp_rows = [
    ("维度", "原生 passive viewer", "PyQt6 嵌入式 viewer"),
    ("实现者", "MuJoCo 引擎自带", "项目自研 (viewer_widget.py)"),
    ("集成方式", "独立窗口，开箱即用", "Qt 组件，可嵌入更大应用"),
    ("渲染机制", "引擎内部直接渲染", "Renderer 离屏 → GL 纹理 → 贴图"),
    ("帧驱动", "主循环手动 sync", "QTimer 每 16ms (~60fps)"),
    ("相机交互", "引擎自带处理", "自实现：左转/右平/滚缩"),
    ("当前状态", "✅ main.py 在用", "⏸ 备用，主程序未调用"),
]
gt = s.shapes.add_table(len(cmp_rows), 3, Inches(0.8), Inches(1.5),
                        Inches(11.7), Inches(5.2)).table
gt.columns[0].width = Inches(2.3)
gt.columns[1].width = Inches(4.7)
gt.columns[2].width = Inches(4.7)
for ri, row in enumerate(cmp_rows):
    for ci, val in enumerate(row):
        cell = gt.cell(ri, ci)
        cell.margin_left = Pt(8); cell.margin_right = Pt(6)
        cell.margin_top = Pt(3); cell.margin_bottom = Pt(3)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        r = cell.text_frame.paragraphs[0].add_run(); r.text = val
        if ri == 0:
            cell.fill.solid(); cell.fill.fore_color.rgb = PRIMARY
            _set_font(r, 13, RGBColor(0xFF, 0xFF, 0xFF), True)
        else:
            cell.fill.solid()
            cell.fill.fore_color.rgb = LIGHT if ri % 2 else CARD
            col = PRIMARY if ci == 0 else DARK
            _set_font(r, 13, col, ci == 0)


# ============================================================
# Slide 10 — 功能特性与扩展
# ============================================================
s = slide()
header(s, "功能特性与扩展性", 10)
footer(s)
feats = [
    ("物理仿真", "MuJoCo 真实刚体动力学：重力、摩擦、碰撞、自由度", PRIMARY),
    ("履带机器人", "车身+履带+四轮+传感器塔，XML 描述易修改", TEAL),
    ("键盘遥操", "WASD 实时控制前进/后退/转向，响应即时", ACCENT),
    ("3D 相机交互", "鼠标自由旋转/平移/缩放，多角度观察", PRIMARY),
    ("双 Viewer 方案", "原生 viewer 即用 + Qt 嵌入式可扩展", TEAL),
    ("XML 可扩展", "改模型/加墙/换灯光/增传感器，无需改代码", ACCENT),
]
cw, ch = Inches(3.95), Inches(2.4)
for i, (t_, d, col) in enumerate(feats):
    r, c = divmod(i, 3)
    x = Inches(0.6) + c * (cw + Inches(0.3))
    y = Inches(1.5) + r * (ch + Inches(0.3))
    rect(s, x, y, cw, ch, CARD, line=LINE)
    rect(s, x, y, Inches(0.1), ch, col)
    text(s, x + Inches(0.3), y + Inches(0.25), cw - Inches(0.5), Inches(0.6),
         [(t_, 18, col, True)])
    text(s, x + Inches(0.3), y + Inches(0.95), cw - Inches(0.5), Inches(1.3),
         [(d, 12.5, DARK, False)])
text(s, Inches(0.6), Inches(6.75), Inches(12), Inches(0.5),
     [("→ 一个轻量、可读、易扩展的机器人仿真起点，适合学习、原型验证与二次开发。", 13, PRIMARY, True)])


# ---------- 保存 ----------
out = "EmbodiedPlatform_功能介绍.pptx"
prs.save(out)
print("已生成:", out, "共", len(prs.slides._sldIdLst), "页")
