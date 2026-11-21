# -*- coding: utf-8 -*-
"""基于 viewer_widget.MuJoCoViewer 的运行入口。

为什么有这个文件：
  MuJoCo 原生 viewer (mujoco.viewer.launch_passive) 的 key_callback 只接收
  1 个 int 参数 (Callable[[int], None])，且只在按键按下/重复时触发、不在
  释放时触发，无法可靠跟踪"按住/松开"状态。原 main.py 照搬 glfw 的
  key_callback(key, action) 写法，因此签名不匹配导致线程崩溃窗口闪退。

解决：
  改用 viewer_widget.MuJoCoViewer（基于 PyQt6 + QOpenGLWidget），借助 Qt 的
  keyPressEvent / keyReleaseEvent 天然跟踪按下与释放，实现按住即动、松开
  即停的 WASD 控制。
"""
import sys
import mujoco
import numpy as np

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt

from viewer_widget import MuJoCoViewer

FORWARD_SPEED = 8.0
TURN_TORQUE = 6.0
# 每帧物理步进次数：QTimer ~60fps × 8 × 0.002s ≈ 0.96，接近实时
# (原 viewer_widget 单帧只步进 1 次 → 仿真比真实慢约 8 倍)
PHYSICS_STEPS_PER_FRAME = 8


def main():
    model = mujoco.MjModel.from_xml_path("world.xml")
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)

    base_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "base")

    app = QApplication(sys.argv)

    viewer = MuJoCoViewer(model, data)
    viewer.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # 必须设，否则收不到键盘事件

    def control():
        # ESC 退出
        if Qt.Key.Key_Escape in viewer.current_keys:
            QApplication.instance().quit()
            return

        force = np.zeros(3)
        torque = np.zeros(3)
        keys = viewer.current_keys
        if Qt.Key.Key_W in keys:
            force[1] += FORWARD_SPEED
        if Qt.Key.Key_S in keys:
            force[1] -= FORWARD_SPEED
        if Qt.Key.Key_A in keys:
            torque[2] += TURN_TORQUE
        if Qt.Key.Key_D in keys:
            torque[2] -= TURN_TORQUE

        # 力转世界系并施加到 base body
        rot = data.xmat[base_id].reshape(3, 3)
        force_world = rot @ force
        qfrc = np.zeros(model.nv)
        mujoco.mj_applyFT(
            model, data,
            force_world, torque,
            data.xpos[base_id],
            base_id, qfrc
        )
        # 覆盖式赋值（原 main.py 用 += 会逐帧累加，力越来越大，是个 bug）
        data.qfrc_applied[:] = qfrc

        # 额外步进若干次使仿真接近实时（viewer_widget.update_simulation 还会再 step 1 次）
        for _ in range(PHYSICS_STEPS_PER_FRAME - 1):
            mujoco.mj_step(model, data)

    viewer.render_callback = control

    window = QMainWindow()
    window.setWindowTitle("EmbodiedPlatform — Tracked Robot (Qt Viewer)")
    window.resize(900, 620)
    window.setCentralWidget(viewer)
    window.show()
    window.move(100, 100)
    window.raise_()
    window.activateWindow()

    print("=== Tracked Robot Demo (Qt Viewer) ===")
    print("W/S: Forward/Backward")
    print("A/D: Turn Left/Right")
    print("Mouse: Left-drag=Rotate  Right-drag=Pan  Scroll=Zoom")
    print("ESC: Quit")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
