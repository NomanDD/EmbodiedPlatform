import numpy as np
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QWheelEvent
import OpenGL.GL as gl
import mujoco


class MuJoCoViewer(QOpenGLWidget):
    def __init__(self, model, data, parent=None):
        super().__init__(parent)
        self.model = model
        self.data = data

        self.camera = mujoco.MjvCamera()
        self.camera.type = mujoco.mjtCamera.mjCAMERA_FREE
        self.camera.lookat = np.array([0.0, 0.0, 0.0])
        self.camera.distance = 3.0
        self.camera.azimuth = 45.0
        self.camera.elevation = -30.0

        self.last_mouse_pos = QPoint()
        self.mouse_pressed = False
        self.mouse_button = None

        self.current_keys = set()
        self.render_callback = None

        self.pixels = None
        self.texture_id = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)

    def initializeGL(self):
        gl.glClearColor(0.2, 0.2, 0.2, 1.0)
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        w, h = self.width(), self.height()
        # offscreen framebuffer 必须不小于渲染尺寸
        if self.model.vis.global_.offwidth < w:
            self.model.vis.global_.offwidth = w
        if self.model.vis.global_.offheight < h:
            self.model.vis.global_.offheight = h
        # 每帧重建 Renderer：mj_step 修改 data 后 MuJoCo offscreen FBO 内部
        # 状态会失效，复用同一个 Renderer 会导致 STATUS_STACK_BUFFER_OVERRUN 崩溃。
        # 注意：不能调 renderer.close()，它会释放 MuJoCo 内部 offscreen FBO，
        # 导致后续 GL 状态破坏。让 Python GC 自行回收即可。
        renderer = mujoco.Renderer(self.model, height=h, width=w)
        renderer.update_scene(self.data, self.camera)
        self.pixels = renderer.render()

        # renderer.render() 结束后 FBO 仍绑定在 MuJoCo 的离屏缓冲上，
        # 若不切回控件自身的帧缓冲，后续贴图会画进离屏缓冲（表现为只有清屏色）。
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self.defaultFramebufferObject())
        gl.glViewport(0, 0, w, h)

        # MuJoCo 渲染后会把投影/模型视图矩阵留在相机状态，固定管线的
        # NDC 坐标必须配单位矩阵，否则四边形被变换到裁剪空间外而不可见。
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glDisable(gl.GL_BLEND)
        gl.glDisable(gl.GL_SCISSOR_TEST)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glColor3f(1.0, 1.0, 1.0)

        self.draw_texture()

    def draw_texture(self):
        if self.pixels is None:
            return
        h, w = self.pixels.shape[:2]
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
        gl.glTexImage2D(
            gl.GL_TEXTURE_2D, 0, gl.GL_RGB, w, h, 0,
            gl.GL_RGB, gl.GL_UNSIGNED_BYTE, self.pixels
        )
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2f(0, 1); gl.glVertex2f(-1, -1)
        gl.glTexCoord2f(1, 1); gl.glVertex2f(1, -1)
        gl.glTexCoord2f(1, 0); gl.glVertex2f(1, 1)
        gl.glTexCoord2f(0, 0); gl.glVertex2f(-1, 1)
        gl.glEnd()

    def update_simulation(self):
        if self.render_callback:
            self.render_callback()
        mujoco.mj_step(self.model, self.data)
        self.update()

    def keyPressEvent(self, event: QKeyEvent):
        self.current_keys.add(event.key())

    def keyReleaseEvent(self, event: QKeyEvent):
        self.current_keys.discard(event.key())

    def mousePressEvent(self, event: QMouseEvent):
        self.mouse_pressed = True
        self.mouse_button = event.button()
        self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.mouse_pressed = False
        self.mouse_button = None

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.mouse_pressed:
            return

        dx = event.x() - self.last_mouse_pos.x()
        dy = event.y() - self.last_mouse_pos.y()

        if self.mouse_button == Qt.MouseButton.LeftButton:
            self.camera.azimuth -= dx * 0.5
            self.camera.elevation += dy * 0.5
            self.camera.elevation = np.clip(self.camera.elevation, -89, 89)

        elif self.mouse_button == Qt.MouseButton.RightButton:
            pan_speed = 0.005 * self.camera.distance
            azimuth = np.radians(self.camera.azimuth)
            elevation = np.radians(self.camera.elevation)
            right = np.array([-np.sin(azimuth), np.cos(azimuth), 0])
            up = np.array([
                -np.sin(elevation) * np.cos(azimuth),
                -np.sin(elevation) * np.sin(azimuth),
                np.cos(elevation)
            ])
            self.camera.lookat += right * dx * pan_speed
            self.camera.lookat += up * dy * pan_speed

        self.last_mouse_pos = event.pos()

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        self.camera.distance *= (1 - delta * 0.001)
        self.camera.distance = np.clip(self.camera.distance, 0.5, 20.0)
