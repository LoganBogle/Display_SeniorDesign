import time
import math
import relay_api
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
        if not self.arm:
            print("❌ Cannot move. xArm is not connected.")
            return

        x, y, z, roll, pitch, yaw = position
        _, current_pos = self.arm.get_position(is_radian=False)
        if current_pos is None:
            print("❌ Cannot get current arm position")
            return

        safe_z = 350
        if current_pos[2] < safe_z:
            print(f"⬆️ Raising Z to {safe_z}mm first...")
            self.arm.set_position(x=current_pos[0], y=current_pos[1], z=safe_z,
                                  roll=current_pos[3], pitch=current_pos[4], yaw=current_pos[5],
                                  speed=speed, wait=True)

        print("➡️ Moving XY at safe Z height...")
        self.arm.set_position(x=x, y=y, z=safe_z,
                              roll=roll, pitch=pitch, yaw=yaw,
                              speed=speed, wait=True)

        print(f"⬇️ Lowering Z down to {z}mm...")
        self.arm.set_position(x=x, y=y, z=z,
                              roll=roll, pitch=pitch, yaw=yaw,
                              speed=speed, wait=True)

        print(f"✅ Safe Move Completed to: {[x, y, z, roll, pitch, yaw]}")

    def pick(self):
        relay_api.solenoid(1)
        print("✅ Gripper Closed (Pick)")

    def place(self):
        relay_api.solenoid(0)
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
        1: {"position": [270, 220, 320, 180, 0, 0], "job_id": 12, "pickup_z": 218, "job_idcount": 1},
        #2: {"position": [480, 5, 360, 180, 0, 0], "job_id": 13, "pickup_z": 225, "job_idcount": 2},
        #3: {"position": [263, -225, 350, 180, 0, 0], "job_id": 14, "pickup_z": 222.5, "job_idcount": 3},
    }

    dropoff_position = [300, 0, 155, 180, 0, 0]
    NUM_LOOPS = 2

    try:
        if arm.arm:
            for loop_num in range(NUM_LOOPS):
                print(f"\n🔄 Starting Loop {loop_num+1} of {NUM_LOOPS}")

                for tray_id, tray_info in trays.items():
                    print(f"\n🧩 Working on Tray {tray_id}")
                    arm.move_to_position(tray_info["position"])
                    time.sleep(1)

                    part_picked = False
                    attempts = 0

                    while not part_picked and attempts < 5:
                        # Step 1: Run camera job to look for pickable part
                        results = trigger_camera([tray_info["job_id"]])
                        time.sleep(1)
                        coordinates = results.get(str(tray_info["job_id"]))

                        if (coordinates
                            and coordinates.get("name") == "Run.Locate.Ok"
                            and coordinates.get("matches", 0) > 0
                            and not (coordinates.get("x") == 0.0 and coordinates.get("y") == 0.0)):

                            print(f"📸 Coordinates received: {coordinates}")
                            coordinates['r3'] = normalize_r3(coordinates['r3'], tray_id)
                            r3_rad = math.radians(coordinates['r3'])
                            offset = 0
                            x_adj = coordinates['x'] - offset * math.cos(r3_rad)
                            y_adj = coordinates['y'] - offset * math.sin(r3_rad)

                            relay_api.solenoid(0)
                            arm.move_to_position([x_adj, y_adj, tray_info["pickup_z"], 180, 0, coordinates['r3']])
                            time.sleep(1)

                            arm.pick()
                            time.sleep(1)

                            arm.move_to_position(dropoff_position)
                            time.sleep(1)

                            arm.place()
                            time.sleep(1)

                            part_picked = True
                        else:
                            print("❌ No pickable parts found. Checking part count...")
                            # Step 2: Run count job
                            results = trigger_camera([tray_info["job_idcount"]])
                            time.sleep(1)
                            count_result = results.get(str(tray_info["job_idcount"]))
                            part_count = count_result.get("matches", 0) if count_result else 0
                            print(f"🔢 Detected part count: {part_count}")

                            if part_count > 5:
                                print("🔔 Vibrating tray...")
                                getattr(relay_api, f"tray{tray_id}")(1)
                                time.sleep(1)
                                getattr(relay_api, f"tray{tray_id}")(0)
                                time.sleep(1)
                            else:
                                print("🚀 Triggering feeder...")
                                getattr(relay_api, f"feeder{tray_id}")(1)
                                time.sleep(4)
                                getattr(relay_api, f"feeder{tray_id}")(0)
                                time.sleep(1)

                            attempts += 1

                    if not part_picked:
                        print(f"❌ Failed to pick part from Tray {tray_id} after {attempts} attempts.")
                        raise SystemExit("🛑 Exiting loop due to repeated failures.")

        else:
            print("❌ xArm is not connected. Exiting.")

    finally:
        arm.disconnect()
