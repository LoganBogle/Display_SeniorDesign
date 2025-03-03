from pymodbus.client import ModbusTcpClient

class ModbusController:
    def __init__(self, cobot_ip, port=502):
        self.client = ModbusTcpClient(cobot_ip, port=port)

    def connect(self):
        if self.client.connect():
            print("✅ Modbus Connected to Cobot")
            return True
        else:
            print("❌ Failed to Connect to Cobot")
            return False

    def send_coordinates(self, x, y, r):
        """Send X, Y, and R coordinates to the cobot."""
        if not self.client.connect():
            print("❌ Connection Failed. Check IP or Network.")
            return
        
        x_int, y_int, r_int = int(x * 100), int(y * 100), int(r * 100)
        
        self.client.write_register(100, x_int)  # X Coordinate
        self.client.write_register(101, y_int)  # Y Coordinate
        self.client.write_register(102, r_int)  # Rotation

        print(f"📤 Sent: X={x_int}, Y={y_int}, R={r_int}")

    def send_tray_signal(self, tray_number, state):
        """Send a signal to vibratory trays (ON=1, OFF=0)."""
        if not self.client.connect():
            print("❌ Connection Failed. Check IP or Network.")
            return
        
        register = 200 + tray_number  # Example: Tray 1 -> Register 201
        self.client.write_register(register, state)
        print(f"📤 Tray {tray_number} set to {'ON' if state else 'OFF'}")

    def read_register(self, register):
        """Read a Modbus register (for debugging)."""
        if not self.client.connect():
            print("❌ Connection Failed. Check IP or Network.")
            return None
        
        response = self.client.read_holding_registers(register, 1)
        if response.isError():
            print(f"❌ Error reading register {register}")
            return None
        return response.registers[0]

    def close(self):
        self.client.close()
        print("🔌 Modbus Disconnected")
