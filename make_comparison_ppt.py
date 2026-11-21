# -*- coding: utf-8 -*-
"""生成 main.py vs qt_run.py 对比 PPT"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── 颜色常量 ──
BG_DARK   = RGBColor(0x1A, 0x1A, 0x2E)
BG_MID    = RGBColor(0x16, 0x21, 0x3E)
ACCENT    = RGBColor(0x00, 0xD2, 0xFF)
ACCENT2   = RGBColor(0xFF, 0x6B, 0x6B)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
GRAY      = RGBColor(0xAA, 0xAA, 0xBB)
GREEN     = RGBColor(0x4E, 0xC9, 0xB0)
ORANGE    = RGBColor(0xFF, 0xA5, 0x00)
CODE_BG   = RGBColor(0x0D, 0x11, 0x17)


def set_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text(slide, left, top, width, height, text, size=18, color=WHITE,
             bold=False, align=PP_ALIGN.LEFT, font_name="Microsoft YaHei"):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top),
                                     Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = align
    return txBox


def add_code_box(slide, left, top, width, height, code, font_size=13):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = CODE_BG
    shape.line.fill.background()
    shape.shadow.inherit = False

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.15)
    tf.margin_bottom = Inches(0.15)

    for i, line in enumerate(code.split("\n")):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(font_size)
        p.font.color.rgb = GREEN
        p.font.name = "Consolas"
        p.space_after = Pt(1)
    return shape


def add_badge(slide, left, top, text, color=ACCENT):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(1.8), Inches(0.4)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(12)
    p.font.color.rgb = WHITE
    p.font.bold = True
    p.font.name = "Microsoft YaHei"
    p.alignment = PP_ALIGN.CENTER
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.03)
    tf.margin_bottom = Inches(0.03)


# ════════════════════════════════════════════
# Slide 1: 封面
# ════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)

add_text(slide, 1.5, 1.8, 10, 1.2,
         "main.py  vs  qt_run.py", 48, ACCENT, bold=True, align=PP_ALIGN.CENTER)
add_text(slide, 1.5, 3.2, 10, 0.8,
         "EmbodiedPlatform 仿真查看器方案对比", 28, WHITE, align=PP_ALIGN.CENTER)
add_text(slide, 1.5, 4.5, 10, 0.6,
         "MuJoCo + GLFW（原生）   vs   MuJoCo + PyQt6 + OpenGL（Qt）",
         18, GRAY, align=PP_ALIGN.CENTER)

# 分隔线
line = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(4), Inches(4.1), Inches(5.333), Inches(0.04))
line.fill.solid()
line.fill.fore_color.rgb = ACCENT
line.line.fill.background()

add_text(slide, 1.5, 5.8, 10, 0.5,
         "EmbodiedPlatform — Tracked Robot Demo", 14, GRAY, align=PP_ALIGN.CENTER)


# ════════════════════════════════════════════
# Slide 2: 架构总览
# ════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)

add_text(slide, 0.8, 0.4, 12, 0.7, "架构总览", 36, ACCENT, bold=True)

# main.py 方案
add_badge(slide, 0.8, 1.3, "main.py", ACCENT2)
items_main = [
    "单文件，66 行",
    "MuJoCo 内建 passive viewer（GLFW）",
    "主循环：while viewer.is_running()",
    "键盘：MuJoCo key_callback → GLFW",
    "渲染：MuJoCo 原生 OpenGL 窗口",
]
for i, item in enumerate(items_main):
    add_text(slide, 1.0, 1.9 + i * 0.45, 5, 0.4, f"  {item}", 16, WHITE)

# qt_run.py 方案
add_badge(slide, 7, 1.3, "qt_run.py", GREEN)
items_qt = [
    "双文件：qt_run.py（入口）+ viewer_widget.py（控件）",
    "PyQt6 + QOpenGLWidget + MuJoCo Renderer",
    "主循环：QApplication.exec() + QTimer 16ms",
    "键盘：Qt keyPressEvent / keyReleaseEvent",
    "渲染：MuJoCo offscreen → Texture → Qt GL",
]
for i, item in enumerate(items_qt):
    add_text(slide, 7.2, 1.9 + i * 0.45, 5.5, 0.4, f"  {item}", 16, WHITE)

# 中间分隔
sep = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(1.3), Inches(0.04), Inches(2.8))
sep.fill.solid()
sep.fill.fore_color.rgb = GRAY
sep.line.fill.background()

# 对比表格
table_data = [
    ("特性", "main.py (GLFW)", "qt_run.py (Qt)"),
    ("依赖", "glfw, mujoco", "PyQt6, OpenGL, mujoco"),
    ("窗口管理", "MuJoCo 内建", "QMainWindow"),
    ("键盘事件", "单参数回调 (无 RELEASE)", "完整 press/release"),
    ("鼠标操控", "MuJoCo 内建", "自定义实现"),
    ("仿真步进", "1 次/帧", "8 次/帧 (接近实时)"),
    ("力赋值", "+= (累加 bug)", "= (覆盖, 正确)"),
    ("代码量", "66 行", "~240 行 (双文件)"),
]

rows, cols = len(table_data), 3
tbl = slide.shapes.add_table(rows, cols,
    Inches(0.8), Inches(4.6), Inches(11.7), Inches(2.6)).table

col_widths = [Inches(2.2), Inches(4.75), Inches(4.75)]
for i, w in enumerate(col_widths):
    tbl.columns[i].width = w

for r in range(rows):
    for c in range(cols):
        cell = tbl.cell(r, c)
        cell.text = table_data[r][c]
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(14)
            p.font.name = "Microsoft YaHei"
            p.alignment = PP_ALIGN.CENTER
            if r == 0:
                p.font.bold = True
                p.font.color.rgb = BG_DARK
            else:
                p.font.color.rgb = WHITE
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        if r == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = ACCENT
        elif r % 2 == 1:
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0x1E, 0x2D, 0x50)
        else:
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0x15, 0x1F, 0x38)


# ════════════════════════════════════════════
# Slide 3: 键盘处理对比
# ════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)

add_text(slide, 0.8, 0.4, 12, 0.7, "键盘处理机制", 36, ACCENT, bold=True)

add_badge(slide, 0.8, 1.3, "main.py — GLFW 回调", ACCENT2)
add_code_box(slide, 0.8, 1.9, 5.5, 2.5,
    '# MuJoCo key_callback 只接收 1 个参数\n'
    'def key_callback(key):\n'
    '    keys_pressed.add(key)\n'
    '\n'
    '# 每帧清空 + sync() 后读取\n'
    'while viewer.is_running():\n'
    '    keys_pressed.clear()\n'
    '    viewer.sync()  # REPEAT 事件重新填充\n'
    '    if glfw.KEY_W in keys_pressed: ...')

add_text(slide, 0.8, 4.6, 5.5, 0.8,
    "限制：无 RELEASE 事件，用 REPEAT 机制模拟\n"
    "每帧必须 clear() + sync() 顺序不能错", 14, ORANGE)

add_badge(slide, 7, 1.3, "qt_run.py — Qt 事件", GREEN)
add_code_box(slide, 7, 1.9, 5.5, 2.5,
    '# Qt 天然区分按下与释放\n'
    'def keyPressEvent(self, event):\n'
    '    self.current_keys.add(event.key())\n'
    '\n'
    'def keyReleaseEvent(self, event):\n'
    '    self.current_keys.discard(event.key())\n'
    '\n'
    '# 在 render_callback 中读取\n'
    'keys = viewer.current_keys\n'
    'if Qt.Key.Key_W in keys: ...')

add_text(slide, 7, 4.6, 5.5, 0.8,
    "优势：完整的 press/release 事件\n"
    "无需 clear()，按键状态自动维护", 14, GREEN)

# 关键差异总结
add_text(slide, 0.8, 5.8, 12, 0.5,
    "核心差异：GLFW 回调是单参数设计，MuJoCo 封装层丢失了 action 信息；"
    "Qt 事件系统完整保留了按下/释放语义", 15, GRAY)


# ════════════════════════════════════════════
# Slide 4: 渲染管线对比
# ════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)

add_text(slide, 0.8, 0.4, 12, 0.7, "渲染管线", 36, ACCENT, bold=True)

# main.py 渲染流程
add_badge(slide, 0.8, 1.2, "main.py — 直接渲染", ACCENT2)
steps_main = [
    "MuJoCo 内建 GLFW 窗口",
    "viewer.sync() 触发事件轮询 + 画面刷新",
    "MuJoCo 内部管理 OpenGL 上下文",
    "无 offscreen buffer，直接渲染到屏幕",
]
for i, s in enumerate(steps_main):
    add_text(slide, 1.0, 1.8 + i * 0.42, 5, 0.4, f"  {s}", 15, WHITE)

# qt_run.py 渲染流程
add_badge(slide, 7, 1.2, "qt_run.py — 离屏渲染", GREEN)
steps_qt = [
    "QOpenGLWidget 管理 OpenGL 上下文",
    "QTimer 每 16ms 触发 update_simulation()",
    "control() → mj_applyFT + mj_step x8",
    "paintGL() → 新建 Renderer → offscreen render",
    "Renderer 生成像素 → glTexImage2D → 绘制纹理",
]
for i, s in enumerate(steps_qt):
    add_text(slide, 7.2, 1.8 + i * 0.42, 5.5, 0.4, f"  {s}", 15, WHITE)

# 渲染流程图
add_text(slide, 0.8, 4.2, 12, 0.5, "qt_run.py 每帧渲染流程", 20, ACCENT, bold=True)

flow_items = [
    ("QTimer\n16ms", GRAY),
    ("control()\nmj_step x8", ACCENT2),
    ("paintGL()\n重建 Renderer", ACCENT),
    ("offscreen\nrender", GREEN),
    ("Texture\n绘制", WHITE),
]

for i, (label, color) in enumerate(flow_items):
    x = 1.0 + i * 2.4
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(x), Inches(4.9), Inches(2.0), Inches(1.0)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0x1E, 0x2D, 0x50)
    shape.line.color.rgb = color
    shape.line.width = Pt(2)
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = label
    p.font.size = Pt(13)
    p.font.color.rgb = color
    p.font.name = "Microsoft YaHei"
    p.alignment = PP_ALIGN.CENTER
    tf.margin_left = Inches(0.1)
    tf.margin_right = Inches(0.1)

    # 箭头
    if i < len(flow_items) - 1:
        arrow = slide.shapes.add_shape(
            MSO_SHAPE.RIGHT_ARROW,
            Inches(x + 2.05), Inches(5.15), Inches(0.3), Inches(0.3)
        )
        arrow.fill.solid()
        arrow.fill.fore_color.rgb = GRAY
        arrow.line.fill.background()

add_text(slide, 0.8, 6.3, 12, 0.5,
    "关键点：qt_run.py 每帧必须新建 Renderer，"
    "因为 mj_step 修改 data 后 MuJoCo offscreen FBO 内部状态失效",
    14, ORANGE)


# ════════════════════════════════════════════
# Slide 5: 仿真步进 & 物理
# ════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)

add_text(slide, 0.8, 0.4, 12, 0.7, "仿真步进与物理参数", 36, ACCENT, bold=True)

# 对比卡片
# main.py
shape = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.8), Inches(1.3), Inches(5.5), Inches(3.0))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x1E, 0x2D, 0x50)
shape.line.color.rgb = ACCENT2
shape.line.width = Pt(2)

add_badge(slide, 1.0, 1.4, "main.py", ACCENT2)
info_main = (
    "每帧 1 次 mj_step\n"
    "timestep = 0.002s\n"
    "实际仿真速率 ≈ 0.5x 实时\n\n"
    "force/torque 直接施加\n"
    "无额外物理步进"
)
add_text(slide, 1.2, 2.0, 5, 2.0, info_main, 16, WHITE)

# qt_run.py
shape = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(7), Inches(1.3), Inches(5.5), Inches(3.0))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x1E, 0x2D, 0x50)
shape.line.color.rgb = GREEN
shape.line.width = Pt(2)

add_badge(slide, 7.2, 1.4, "qt_run.py", GREEN)
info_qt = (
    "每帧 8 次 mj_step\n"
    "timestep = 0.002s\n"
    "实际仿真速率 ≈ 0.96x 实时\n\n"
    "control() 先施力 + 步进 7 次\n"
    "update_simulation() 再步进 1 次"
)
add_text(slide, 7.4, 2.0, 5, 2.0, info_qt, 16, WHITE)

# 力赋值对比
add_text(slide, 0.8, 4.8, 12, 0.5, "力赋值 Bug 对比", 22, ACCENT, bold=True)

add_code_box(slide, 0.8, 5.5, 5.5, 1.0,
    '# main.py (修复前) — 逐帧累加\n'
    'data.qfrc_applied[:] += qfrc  # BUG!',
    font_size=14)

add_code_box(slide, 7, 5.5, 5.5, 1.0,
    '# qt_run.py — 每帧覆盖\n'
    'data.qfrc_applied[:] = qfrc  # 正确',
    font_size=14)

add_text(slide, 0.8, 6.7, 12, 0.5,
    "+= 会导致力无限累加，机器人突然加速飞天", 14, ACCENT2, bold=True)


# ════════════════════════════════════════════
# Slide 6: 鼠标 & 相机操控
# ════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)

add_text(slide, 0.8, 0.4, 12, 0.7, "鼠标与相机操控", 36, ACCENT, bold=True)

# main.py
add_badge(slide, 0.8, 1.2, "main.py — MuJoCo 内建", ACCENT2)
cam_main = (
    "左键拖拽：旋转视角\n"
    "右键拖拽：平移视角\n"
    "滚轮：缩放\n\n"
    "由 MuJoCo 内建 viewer 处理\n"
    "无法自定义行为"
)
add_text(slide, 1.0, 1.8, 5, 2.5, cam_main, 16, WHITE)

# qt_run.py
add_badge(slide, 7, 1.2, "qt_run.py — 自定义实现", GREEN)
cam_qt = (
    "左键拖拽：旋转视角\n"
    "  → azimuth -= dx * 0.5\n"
    "  → elevation += dy * 0.5\n"
    "  → elevation clamp [-89, 89]\n\n"
    "右键拖拽：平移视角\n"
    "  → 计算 right/up 方向向量\n"
    "  → lookat += (right*dx + up*dy) * speed\n\n"
    "滚轮：缩放\n"
    "  → distance *= (1 - delta * 0.001)\n"
    "  → clamp [0.5, 20.0]"
)
add_text(slide, 7.2, 1.8, 5.5, 3.5, cam_qt, 14, WHITE)

# 优势总结
add_text(slide, 0.8, 5.2, 12, 0.5, "Qt 方案优势", 22, ACCENT, bold=True)
advantages = [
    "完全可自定义：可添加轨道相机、FPS 相机、预设视角等",
    "可与 Qt UI 集成：侧边栏参数调节、状态显示",
    "鼠标事件可精确控制：灵敏度、死区、按钮映射",
]
for i, a in enumerate(advantages):
    add_text(slide, 1.0, 5.8 + i * 0.42, 11, 0.4, f"  {a}", 15, WHITE)


# ════════════════════════════════════════════
# Slide 7: Bug 修复记录
# ════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)

add_text(slide, 0.8, 0.4, 12, 0.7, "Bug 修复记录", 36, ACCENT, bold=True)

bugs = [
    ("Bug 1: key_callback 签名不匹配",
     "main.py 原始代码",
     "key_callback(key, action) 接收 2 参数",
     "MuJoCo 只传 1 个参数 → TypeError 崩溃",
     "改为 key_callback(key)，用 REPEAT 机制",
     ACCENT2),
    ("Bug 2: 力逐帧累加",
     "main.py 原始代码",
     "data.qfrc_applied[:] += qfrc",
     "力无限增大，机器人突然飞天",
     "改为 = qfrc 覆盖赋值",
     ACCENT2),
    ("Bug 3: MuJoCo Renderer FBO 崩溃",
     "viewer_widget.py",
     "self.renderer 跨帧复用 + renderer.close()",
     "mj_step 后 FBO 状态失效 → 0xC0000409 崩溃",
     "每帧新建 Renderer，不调 close()",
     ORANGE),
]

for i, (title, file, bad, cause, fix, color) in enumerate(bugs):
    y = 1.3 + i * 1.9
    add_text(slide, 0.8, y, 12, 0.4, title, 18, color, bold=True)
    add_text(slide, 1.2, y + 0.45, 3, 0.35, f"文件: {file}", 12, GRAY)
    add_code_box(slide, 1.2, y + 0.8, 5, 0.35, bad, font_size=12)
    add_text(slide, 6.5, y + 0.8, 0.3, 0.35, "→", 16, color, bold=True)
    add_code_box(slide, 7, y + 0.8, 5, 0.35, fix, font_size=12)
    add_text(slide, 1.2, y + 1.3, 10, 0.35, f"原因: {cause}", 13, GRAY)


# ════════════════════════════════════════════
# Slide 8: 总结
# ════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_bg(slide, BG_DARK)

add_text(slide, 0.8, 0.5, 12, 0.7, "总结与建议", 36, ACCENT, bold=True)

# main.py 适用场景
shape = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.8), Inches(1.5), Inches(5.5), Inches(2.5))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x1E, 0x2D, 0x50)
shape.line.color.rgb = ACCENT2
shape.line.width = Pt(2)

add_badge(slide, 1.0, 1.6, "main.py", ACCENT2)
add_text(slide, 1.2, 2.2, 5, 1.5,
    "适合场景：\n"
    "  快速原型验证\n"
    "  不需要自定义 UI\n"
    "  简单的机器人控制 demo\n\n"
    "优点：代码简洁、依赖少\n"
    "缺点：键盘事件受限、无自定义 UI", 15, WHITE)

# qt_run.py 适用场景
shape = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(7), Inches(1.5), Inches(5.5), Inches(2.5))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0x1E, 0x2D, 0x50)
shape.line.color.rgb = GREEN
shape.line.width = Pt(2)

add_badge(slide, 7.2, 1.6, "qt_run.py", GREEN)
add_text(slide, 7.4, 2.2, 5, 1.5,
    "适合场景：\n"
    "  正式项目、需要 GUI\n"
    "  参数调节面板\n"
    "  多传感器可视化\n\n"
    "优点：完整键盘/鼠标、可扩展 UI\n"
    "缺点：代码量大、依赖重", 15, WHITE)

# 推荐
add_text(slide, 0.8, 4.5, 12, 0.5,
    "项目建议", 22, ACCENT, bold=True)
add_text(slide, 1.0, 5.2, 11, 1.5,
    "  1. 当前项目使用 qt_run.py 作为主入口，main.py 保留为轻量备用\n"
    "  2. 后续可基于 Qt 方案添加：参数调节面板、传感器数据可视化、录制回放\n"
    "  3. 如需性能优化，可考虑将 Renderer 改为缓存复用 + 按需重建策略",
    16, WHITE)


# ── 保存 ──
out_path = r"E:\Project\EmbodiedPlatform\main_vs_qt_run.pptx"
prs.save(out_path)
print(f"Saved: {out_path}")
