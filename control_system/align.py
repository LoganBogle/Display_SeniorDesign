import socket
import json
import time
from xarm.wrapper import XArmAPI

# === xArm Configuration ===
XARM_IP = "192.168.1.243"

# === PLOC2D Configuration ===
PLOC2D_IP = "192.168.1.242"
PLOC2D_PORT = 14158

# === Update this: the index of the work plane you want to align ===
WORKPLANE_INDEX = 4  # Change this to the work plane you're aligning

def get_robot_pose():
    """Get the current Cartesian pose from the xArm."""
    arm = XArmAPI(XARM_IP)
    time.sleep(0.5)
    arm.clean_error()
    arm.clean_warn()
    arm.motion_enable(True)
    arm.set_mode(0)
    arm.set_state(0)

    result = arm.get_position(is_radian=False)
    print("🤖 Raw xArm Pose Response:", result)

    arm.disconnect()

    if isinstance(result, tuple) and result[0] == 0 and isinstance(result[1], list) and len(result[1]) >= 6:
        pos = result[1]
        return {
            "alignment": WORKPLANE_INDEX,  # required for Alignment.Align
            "x": pos[0],
            "y": pos[1],
            "z": pos[2],
            "r1": pos[3],
            "r2": pos[4],
            "r3": pos[5],
        }
    else:
        raise RuntimeError("❌ Failed to get valid pose from xArm. Full response: " + str(result))

def send_json_command(command_dict):
    """Send a JSON command to the PLOC2D and print the response."""
    try:
        print(f"📡 Connecting to PLOC2D at {PLOC2D_IP}:{PLOC2D_PORT}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((PLOC2D_IP, PLOC2D_PORT))
        print("✅ Connection to PLOC2D successful!")

        command_json = json.dumps(command_dict)
        print(f"📤 Sending JSON command: {command_json}")
        sock.sendall((command_json + "\n").encode())

        response = sock.recv(4096).decode()
        print("📩 Raw Response from PLOC2D:", response)

        sock.close()
    except Exception as e:
        print(f"❌ Error: {e}")

# === Main Process ===
try:
    pose = get_robot_pose()
    alignment_command = {
        "name": "Alignment.Align",
        **pose
    }
    send_json_command(alignment_command)
except Exception as err:
    print(f"❌ Failed to align work plane: {err}")
