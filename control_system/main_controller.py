from modbus_controller import ModbusController

COBOT_IP = "192.168.1.100"  # Change to your Cobot's IP

def main():
    modbus = ModbusController(COBOT_IP)

    if modbus.connect():
        # ✅ Step 1: Test Modbus Communication
        print("🔄 Checking Modbus Connection...")
        if modbus.read_register(100) is not None:
            print("✅ Modbus Communication is WORKING!")

        # ✅ Step 2: Send Test Coordinates
        modbus.send_coordinates(120.56, 45.78, 90.34)

        # ✅ Step 3: Turn ON Tray 1 (for testing)
        modbus.send_tray_signal(1, 1)  # Turn Tray 1 ON
        modbus.send_tray_signal(1, 0)  # Turn Tray 1 OFF

        modbus.close()

if __name__ == "__main__":
    main()
