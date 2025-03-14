import time
from xarm.wrapper import XArmAPI

try:
    from control_system.config import XARM_IP  # If running from project root
except ModuleNotFoundError:
    from config import XARM_IP  # If running from inside control_system

# Connect to xArm
print("🔌 Attempting to connect to xArm...")
try:
    arm = XArmAPI(XARM_IP)
    time.sleep(0.5)
    
    if not arm.connected:
        raise Exception("❌ xArm is not connected.")
    
    print("✅ Successfully connected to xArm!")
    
    # Clear warnings and errors
    arm.clean_warn()
    arm.clean_error()
    arm.motion_enable(True)
    arm.set_mode(0)
    arm.set_state(0)
    
    # Check error codes before proceeding
    error_code = arm.get_err_warn_code()
    print(f"📋 Active Errors: {error_code}")
    
    # Check GPIO Power State
    print("🔌 Checking Tool GPIO (TGPIO) status...")
    tgpio_power_status = arm.get_tgpio_digital()
    print(f"Tool GPIO Status: {tgpio_power_status}")
    
    print("🔌 Checking Controller GPIO (CGPIO) status...")
    cgpio_power_status = arm.get_cgpio_digital()
    print(f"Controller GPIO Status: {cgpio_power_status}")
    
    # Test Tool GPIO (TGPIO) Output
    print("🔌 Setting Tool GPIO Pin 0 HIGH (24V)...")
    result = arm.set_tgpio_digital(0, 1)
    print(f"Result: {result}")
    time.sleep(2)
    
    print("🔌 Setting Tool GPIO Pin 0 LOW (0V)...")
    result = arm.set_tgpio_digital(0, 0)
    print(f"Result: {result}")
    time.sleep(2)
    
    # Try Pin 1 in case Pin 0 is inactive
    print("🔌 Setting Tool GPIO Pin 1 HIGH (24V)...")
    result = arm.set_tgpio_digital(1, 1)
    print(f"Result: {result}")
    time.sleep(2)
    
    print("🔌 Setting Tool GPIO Pin 1 LOW (0V)...")
    result = arm.set_tgpio_digital(1, 0)
    print(f"Result: {result}")
    time.sleep(2)
    
    # Test Controller GPIO (CGPIO) Output
    print("🔌 Setting Controller GPIO DO0 HIGH (24V)...")
    result = arm.set_cgpio_digital(0, 1)
    print(f"Result: {result}")
    time.sleep(2)
    
    print("🔌 Setting Controller GPIO DO0 LOW (0V)...")
    result = arm.set_cgpio_digital(0, 0)
    print(f"Result: {result}")
    time.sleep(2)
    
    # Retry setting GPIO multiple times to ensure activation
    for i in range(3):
        print(f"🔄 Attempt {i+1}: Setting Tool GPIO Pin 0 HIGH")
        arm.set_tgpio_digital(0, 1)
        time.sleep(1)
        
        print(f"🔄 Attempt {i+1}: Setting Tool GPIO Pin 0 LOW")
        arm.set_tgpio_digital(0, 0)
        time.sleep(1)
    
    arm.disconnect()
    print("✅ Disconnected from xArm")

except Exception as e:
    print(f"❌ Error: {e}")
    print("Skipping GPIO tests because the xArm is not connected or an error occurred.")
