import relay_control_python as rc

# Feeder controls
def feeder1(state): rc.control_relay("feeder1", state)
def feeder2(state): rc.control_relay("feeder2", state)
def feeder3(state): rc.control_relay("feeder3", state)

# Tray controls
def tray1(state): rc.control_relay("tray1", state)
def tray2(state): rc.control_relay("tray2", state)
def tray3(state): rc.control_relay("tray3", state)

# Solenoid control
def solenoid(state): rc.control_relay("solenoid", state)