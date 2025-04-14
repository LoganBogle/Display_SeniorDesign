import time
import math
from xarm.wrapper import XArmAPI
from camera_handler import trigger_camera

try:
    from control_system.config import XARM_IP  # If running from project root
except ModuleNotFoundError:
    from config import XARM_IP  # If running from inside control_system

class XArmController:
    def __init__(self):
        print("🔌 Attempting to connect to xArm...")
        self.arm = XArmAPI(XARM_IP)
        time.sleep(0.5)
        if not self.arm.connected:
            raise Exception("❌ xArm is not connected.")
        self.initialize_arm()

    def initialize_arm(self):
        self.arm.clean_warn()
        self.arm.clean_error()
        self.arm.motion_enable(True)
        self.arm.set_mode(0)  # Position control mode
        self.arm.set_state(0)

    def move_to_position(self, position, speed=100):
        """Safe move: Raise Z first, move XY, then lower Z."""
        if not self.arm:
            print("❌ Cannot move. xArm is not connected.")
            return

        x, y, z, roll, pitch, yaw = position

        # Step 1: Get current position
        _, current_pos = self.arm.get_position(is_radian=False)
        if current_pos is None:
            print("❌ Cannot get current arm position")
            return

        # Step 2: Raise Z to 350mm first if not already high
        safe_z = 350  # mm
        if current_pos[2] < safe_z:
            print(f"⬆️ Raising Z to {safe_z}mm first...")
            self.arm.set_position(x=current_pos[0], y=current_pos[1], z=safe_z,
                                  roll=current_pos[3], pitch=current_pos[4], yaw=current_pos[5],
                                  speed=speed, wait=True)

        # Step 3: Move X and Y at safe Z
        print("➡️ Moving XY at safe Z height...")
        self.arm.set_position(x=x, y=y, z=safe_z,
                              roll=roll, pitch=pitch, yaw=yaw,
                              speed=speed, wait=True)

        # Step 4: Lower Z to target
        print(f"⬇️ Lowering Z down to {z}mm...")
        self.arm.set_position(x=x, y=y, z=z,
                              roll=roll, pitch=pitch, yaw=yaw,
                              speed=speed, wait=True)

        print(f"✅ Safe Move Completed to: {[x, y, z, roll, pitch, yaw]}")

    def pick(self):
        print("✅ Gripper Closed (Pick)")

    def place(self):
        print("✅ Gripper Opened (Place)")

    def disconnect(self):
        if self.arm:
            self.arm.disconnect()
            print("✅ Disconnected from xArm")

def normalize_r3(r3, tray_id):
    if tray_id == 1:
        if r3 > 110: r3 -= 180
        if r3 < -70: r3 += 180
    elif tray_id == 2:
        if r3 > 90: r3 -= 180
        if r3 < -90: r3 += 180
    elif tray_id == 3:
        if r3 > 70: r3 -= 180
        if r3 < -110: r3 += 180
    return r3

if __name__ == "__main__":
    arm = XArmController()

    trays = {
        #1: {"position": [260, 215, 320, 180, 0, 0], "job_id": 12, "pickup_z": 218.5},
        #2: {"position": [480, 5, 360, 180, 0, 0], "job_id": 13, "pickup_z": 225},
        3: {"position": [263, -225, 350, 180, 0, 0], "job_id": 14, "pickup_z": 225},
    }
    dropoff_position = [300, 0, 145, 180, 0, 0]

    NUM_LOOPS = 2  # <=== Change this to however many full tray loops you want.

    try:
        if arm.arm:
            for loop_num in range(NUM_LOOPS):
                print(f"\n🔄 Starting Loop {loop_num+1} of {NUM_LOOPS}")

                for tray_id, tray_info in trays.items():
                    print(f"\n🧩 Working on Tray {tray_id}")
                    arm.move_to_position(tray_info["position"])
                    time.sleep(1)

                    found_part = False
                    feeder_attempts = 0

                    while not found_part and feeder_attempts < 3:
                        for attempt in range(3):
                            coordinates = trigger_camera(job_id=tray_info["job_id"])
                            time.sleep(1)

                            if (coordinates
                                and coordinates.get("name") == "Run.Locate.Ok"
                                and coordinates.get("matches", 0) > 0
                                and not (coordinates.get("x") == 0.0 and coordinates.get("y") == 0.0)):

                                print(f"📸 Coordinates received: {coordinates}")

                                coordinates['r3'] = normalize_r3(coordinates['r3'], tray_id)

                                r3_rad = math.radians(coordinates['r3'])
                                offset = 0  # no offset right now
                                x_adj = coordinates['x'] - offset * math.cos(r3_rad)
                                y_adj = coordinates['y'] - offset * math.sin(r3_rad)

                                # Move above the part
                                arm.move_to_position([x_adj, y_adj, tray_info["pickup_z"], 180, 0, coordinates['r3']])
                                time.sleep(1)

                                arm.pick()
                                time.sleep(1)

                                arm.move_to_position(dropoff_position)
                                time.sleep(1)

                                arm.place()
                                time.sleep(1)

                                found_part = True
                                break
                            else:
                                print(f"❌ No valid coordinates on attempt {attempt + 1}")
                                if attempt < 2:
                                    print(f"🔔 Vibrating Tray {tray_id}... (simulate vibration)")
                                    time.sleep(1)

                        if not found_part:
                            feeder_attempts += 1
                            if feeder_attempts < 3:
                                print(f"⚡ No part found after 3 tries. Feeder attempt {feeder_attempts}/3.")
                                print(f"🚀 Feeder for Tray {tray_id} turned ON")
                                time.sleep(2)  # simulate feeder run
                                print(f"🛑 Feeder for Tray {tray_id} turned OFF")
                            else:
                                print(f"❌ No parts found after 3 feeder tries. Manual intervention required!")
                                raise SystemExit("🚨 Stopping system. No parts found.")

        else:
            print("❌ xArm is not connected. Exiting.")

    finally:
        arm.disconnect()
