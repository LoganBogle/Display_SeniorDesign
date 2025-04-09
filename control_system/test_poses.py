import socket
import json
import time
from xarm.wrapper import XArmAPI

# === Robot and Camera Configuration ===
XARM_IP = "192.168.1.243"   # Your robot IP
PLOC2D_IP = "192.168.1.242" # Your camera IP
PLOC2D_PORT = 14158         # PLOC2D native protocol port

# === Your 10 Real Calibration Poses ===
calibration_poses = [
    [470.0, 0.0, 425.0, 179.173356, 0.007792, 0.000286],
    [449.87088, -88.761742, 447.335388, 167.938284, -4.841493, 54.039947],
    [430.687408, -79.097176, 631.711243, 169.324957, -3.638167, 54.484276],
    [295.98468, 6.206091, 543.015564, 178.774349, -20.122049, 0.779165],
    [548.606812, 0.925445, 529.239319, 178.746044, 7.876222, 0.08348],
]


def send_json_command(command_dict, expect_response=True):
    """Send a JSON command to the PLOC2D camera and optionally print the response."""
    try:
        print(f"📡 Connecting to PLOC2D at {PLOC2D_IP}:{PLOC2D_PORT}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((PLOC2D_IP, PLOC2D_PORT))
        print("✅ Connection to PLOC2D successful!")

        command_json = json.dumps(command_dict)
        print(f"📤 Sending JSON command: {command_json}")
        sock.sendall((command_json + "\n").encode())

        if expect_response:
            try:
                response = sock.recv(4096).decode()
                print("📩 Raw Response from PLOC2D:", response)
                try:
                    parsed = json.loads(response)
                    print("✅ Parsed Response:")
                    for key, value in parsed.items():
                        print(f"   {key}: {value}")
                except Exception:
                    print("⚠️  Could not parse response as JSON.")
            except socket.timeout:
                print("⏳ No immediate response from camera (this is OK)")

        sock.close()
    except Exception as e:
        print(f"❌ Error sending to camera: {e}")

def main():
    """Main function to move robot, send poses, and auto-calculate alignment."""
    arm = XArmAPI(XARM_IP)
    time.sleep(0.5)
    arm.clean_error()
    arm.clean_warn()
    arm.motion_enable(True)
    arm.set_mode(0)
    arm.set_state(0)

    print("✅ Robot Connected!")

    # Move through each calibration pose
    for idx, pose in enumerate(calibration_poses, 1):
        print(f"\n🚀 Moving to Pose {idx}: {pose}")
        x, y, z, roll, pitch, yaw = pose
        arm.set_position(x, y, z, roll, pitch, yaw, speed=100, wait=True)

        time.sleep(1.5)

        # Capture and send pose immediately
        current_pose = arm.get_position(is_radian=False)
        if isinstance(current_pose, tuple) and current_pose[0] == 0 and isinstance(current_pose[1], list) and len(current_pose[1]) >= 6:
            pos = current_pose[1]
            pose_command = {
                "name": "Alignment.HandEye.Pose.Add",
                "x": pos[0],
                "y": pos[1],
                "z": pos[2],
                "r1": pos[3],
                "r2": pos[4],
                "r3": pos[5],
            }
            send_json_command(pose_command, expect_response=False)
        else:
            print(f"❌ Failed to get current pose: {current_pose}")

        # Wait after sending the pose
        print("🕒 Waiting 6 seconds for camera to process...")
        time.sleep(6)

    arm.disconnect()
    print("✅ Finished all calibration moves!")

    # Now Calculate Alignment!
    print("\n🧠 Sending Alignment.HandEye.Pose.Calculate...")
    calculate_command = {
        "name": "Alignment.HandEye.Pose.Calculate"
    }
    send_json_command(calculate_command, expect_response=True)

if __name__ == "__main__":
    main()
