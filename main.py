import numpy as np
import glfw
import mujoco
import mujoco.viewer


def main():
    model = mujoco.MjModel.from_xml_path("world.xml")
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)

    base_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "base")
    forward_speed = 8.0
    turn_torque = 6.0

    # MuJoCo 的 key_callback 只接收 1 个参数 (key: int)，
    # 且仅在 PRESS/REPEAT 时触发，不触发 RELEASE。
    # 策略：每次 viewer.sync() 会触发 GLFW 事件轮询，
    # 此时按住的键会以 REPEAT 事件重新写入 keys_pressed。
    # 因此每帧开始时清空集合，sync() 后读取即可。
    keys_pressed = set()

    def key_callback(key):
        keys_pressed.add(key)

    with mujoco.viewer.launch_passive(model, data, key_callback=key_callback) as viewer:
        print("=== Tracked Robot Demo ===")
        print("W/S: Forward/Backward")
        print("A/D: Turn Left/Right")
        print("Mouse: Left-drag=Rotate  Right-drag=Pan  Scroll=Zoom")
        print("ESC: Quit")

        while viewer.is_running():
            # 清空后由下一帧 viewer.sync() 中的 REPEAT 事件重新填充
            keys_pressed.clear()
            viewer.sync()

            force = np.zeros(3)
            torque = np.zeros(3)

            if glfw.KEY_W in keys_pressed:
                force[1] += forward_speed
            if glfw.KEY_S in keys_pressed:
                force[1] -= forward_speed
            if glfw.KEY_A in keys_pressed:
                torque[2] += turn_torque
            if glfw.KEY_D in keys_pressed:
                torque[2] -= turn_torque

            if np.linalg.norm(force) > 0 or np.linalg.norm(torque) > 0:
                rot = data.xmat[base_id].reshape(3, 3)
                force_world = rot @ force
                qfrc = np.zeros(model.nv)
                mujoco.mj_applyFT(
                    model, data,
                    force_world, torque,
                    data.xpos[base_id],
                    base_id, qfrc
                )
                data.qfrc_applied[:] = qfrc

            mujoco.mj_step(model, data)


if __name__ == "__main__":
    main()
