import time
import math
from xarm.wrapper import XArmAPI
from camera_handler import trigger_camera

try:
    from control_system.config import XARM_IP  # If running from project root
except ModuleNotFoundError:
    from config import XARM_IP  # If running inside control_system

class XArmController:
    def __init__(self):
        """Initialize xArm connection and set up motion."""
        try:
            print("🔌 Attempting to connect to xArm...")
            self.arm = XArmAPI(XARM_IP)
            time.sleep(0.5)

            if not self.arm.connected:
                raise Exception("❌ xArm is not connected.")

            self.initialize_arm()
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Skipping xArm initialization.")
            self.arm = None

    def initialize_arm(self):
        """Clear errors, enable motion, and set control mode."""
        if self.arm:
            self.arm.clean_warn()
            self.arm.clean_error()
            self.arm.motion_enable(True)
            self.arm.set_mode(0)  # Position Control Mode
            self.arm.set_state(0)

    def move_to_position(self, position, speed=100):
        """Move xArm to a specific position."""
        if self.arm:
            x, y, z, roll, pitch, yaw = position
            self.arm.set_position(x, y, z, roll, pitch, yaw, speed=speed, wait=True)
            print(f"✅ Moved to Position: {position}")
        else:
            print("❌ Cannot move. xArm is not connected.")

    def pick(self):
        """Close the gripper."""
        if self.arm:
            print("✅ Closing gripper (picking part)")
            self.arm.set_gripper_position(800, wait=True)
        else:
            print("❌ Cannot pick. xArm is not connected.")

    def place(self):
        """Open the gripper."""
        if self.arm:
            print("✅ Opening gripper (placing part)")
            self.arm.set_gripper_position(0, wait=True)
        else:
            print("❌ Cannot place. xArm is not connected.")

    def disconnect(self):
        """Disconnect xArm."""
        if self.arm:
            self.arm.disconnect()
            print("✅ Disconnected from xArm")

if __name__ == "__main__":
    arm = XArmController()

    try:
        if arm.arm:  # Ensure arm is connected
            # --- Define Coordinates ---
            trays = [
                [470, 5, 425, 180, 0, 0],   # Tray 1 Position
                [285, -250, 350, 180, 0, 0], # Tray 2 Position
                [150, -300, 320, 180, 0, 0], # Tray 3 Position
            ]
            drop_off_location = [300, 200, 300, 180, 0, 0]  # Drop-off Position

            while True:  # 🔁 Infinite loop
                for idx, tray_position in enumerate(trays, 1):
                    print(f"\n🧺 Moving to Tray {idx}")
                    arm.move_to_position(tray_position)

                    # ✅ Trigger the camera
                    coordinates = trigger_camera(job_id=10)

                    if coordinates:
                        print(f"📍 Part Detected: {coordinates}")

                        # Normalize rotation
                        if coordinates['r3'] > 90:
                            coordinates['r3'] -= 180
                        if coordinates['r3'] < -90:
                            coordinates['r3'] += 180

                        # Apply offset if needed
                        r3_rad = math.radians(coordinates['r3'])
                        offset = 0  # (change if you have a gripper offset)

                        x_adj = coordinates['x'] - offset * math.cos(r3_rad)
                        y_adj = coordinates['y'] - offset * math.sin(r3_rad)

                        # ✅ Move above part (hover)
                        arm.move_to_position([x_adj, y_adj, 250, 180, 0, coordinates['r3']])

                        time.sleep(1)  # Settle a little
                        # ✅ Move down to part
                        arm.move_to_position([x_adj, y_adj, 180, 180, 0, coordinates['r3']])

                        # ✅ Pick part
                        arm.pick()

                        # ✅ Move up with part
                        arm.move_to_position([x_adj, y_adj, 300, 180, 0, coordinates['r3']])

                        # ✅ Move to drop-off location
                        print("🚚 Moving to Drop-Off")
                        arm.move_to_position(drop_off_location)

                        # ✅ Place part
                        arm.place()

                        # ✅ Move up after placing
                        arm.move_to_position([drop_off_location[0], drop_off_location[1], 400, 180, 0, 0])

                    else:
                        print(f"❌ No part detected at Tray {idx}, skipping to next tray.")

                print("\n🔁 Restarting loop from Tray 1...")

        else:
            print("❌ xArm is not connected. Skipping movement.")

    finally:
        arm.disconnect()
