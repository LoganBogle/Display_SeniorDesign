import time
from xarm.wrapper import XArmAPI
from camera_handler import trigger_camera

try:
    from control_system.config import XARM_IP  # If running from project root
except ModuleNotFoundError:
    from config import XARM_IP  # If running from inside control_system

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

    def move_to_home(self):
        """Move xArm to home position using servo angles."""
        if self.arm:
            self.arm.set_servo_angle(angle=[0, 0, 0, 0, 0, 0], speed=10, wait=True)
            print("✅ Moved to Home Position (Servo Angles)")
        else:
            print("❌ Cannot move to home. xArm is not connected.")

    def move_to_position(self, position, speed=100):
        """
        Move xArm to a specific position using Cartesian coordinates.
        
        :param position: [X, Y, Z, Roll, Pitch, Yaw]
        :param speed: Movement speed (default: 100)
        """
        if self.arm:
            x, y, z, roll, pitch, yaw = position
            self.arm.set_position(x, y, z, roll, pitch, yaw, speed=speed, wait=True)
            print(f"✅ Moved to Position: {position}")
        else:
            print("❌ Cannot move. xArm is not connected.")

    def wave(self):
        """Make the robot wave."""
        if self.arm:
            print("👋 Waving at you!")
            for _ in range(3):  # Repeat wave motion 3 times
                self.move_to_position([250, 50, 150, 180, 0, 0])  # Up position
                print(f"✅ Verified Current Position: {arm.arm.get_position()}")
                self.move_to_position([250, 50, 100, 180, 0, 0])  # Down position
                print(f"✅ Verified Current Position: {arm.arm.get_position()}")
            print("✅ Finished waving!")
        else:
            print("❌ Cannot wave. xArm is not connected.")

    def pick(self, pick_position):
        """Move to pick position and close gripper."""
        if self.arm:
            print("✅ Moving to Pick Position")
            self.move_to_position(pick_position)
            self.arm.set_gripper_position(800, wait=True)  # Close gripper (adjust as needed)
        else:
            print("❌ Cannot pick. xArm is not connected.")

    def place(self, place_position):
        """Move to place position and open gripper."""
        if self.arm:
            print("✅ Moving to Place Position")
            self.move_to_position(place_position)
            self.arm.set_gripper_position(0, wait=True)  # Open gripper
        else:
            print("❌ Cannot place. xArm is not connected.")

    def disconnect(self):
        """Disconnect xArm."""
        if self.arm:
            self.arm.disconnect()
            print("✅ Disconnected from xArm")

# If run directly, test movements
if __name__ == "__main__":
    arm = XArmController()
    
    try:
        if arm.arm:  # Ensure arm is connected before running movements
            arm.move_to_home()
            
            arm.move_to_position([204.6, 2.6, 250, 180, 0, 0])
            # ✅ Move above Tray 1
            arm.move_to_position([317.6, 42.7, 376.4, 178.8, 2.6, 0.4])

            # ✅ Trigger the camera to take a picture
            coordinates = trigger_camera(job_id=2)  # Call the function from camera_handler.py

            # ✅ Print the results
            if coordinates:
                print("\n📸 **Camera Detection Results**")
                print(f"📍 X: {coordinates['x']} mm")
                print(f"📍 Y: {coordinates['y']} mm")
                print(f"📍 Z: {coordinates['z']} mm")
                print(f"🔄 Rotation 1 (Roll): {coordinates['r1']}°")
                print(f"🔄 Rotation 2 (Pitch): {coordinates['r2']}°")
                print(f"🔄 Rotation 3 (Yaw): {coordinates['r3']}°")
                print(f"✅ Match Confidence: {coordinates['score']}%")
                print(f"🔎 Total Matches Found: {coordinates['matches']}")
                print("Moving to part position")
                arm.move_to_position([coordinates['x']-155, coordinates['y'], 188.7, -179.9, -1.2, 25.6])
                time.sleep(1)
                arm.move_to_position([317.6, 42.7, 376.4, 178.8, 2.6, 0.4])

            
            
            arm.move_to_position([174.9, 207.4, 376.4, -179.9, -1.6, 42.3])
            arm.move_to_position([174.9, 207.4, 109.1, -179.9, -1.6, 42.3])
            time.sleep(1)
            arm.move_to_home()


            
        else:
            print("❌ xArm is not connected. Skipping movement tests.")
    finally:
        arm.disconnect()

