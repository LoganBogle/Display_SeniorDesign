from gpiozero import OutputDevice
from time import sleep

# Mapping of relay names to GPIO pin numbers
PIN_MAP = {
    "tray1": 25,
    "tray2": 24,
    "tray3": 23,
    "solenoid": 16,
    "feeder1": 22,
    "feeder2": 27,
    "feeder3": 17,
}

# Store OutputDevice instances
_relays = {}

# Configuration: Use active-high relays (True = relay ON when GPIO is HIGH)
ACTIVE_HIGH = True

def init_gpio():
    """Initializes GPIOs and ensures all relays are off."""
    for name, pin in PIN_MAP.items():
        if name not in _relays:
            # Initial state is OFF (LOW if active-high)
            initial_state = not ACTIVE_HIGH
            relay = OutputDevice(pin, active_high=ACTIVE_HIGH, initial_value=initial_state)
            _relays[name] = relay
            relay.off()
            print(f"[INIT] {name} relay set to OFF (GPIO {'LOW' if not ACTIVE_HIGH else 'HIGH'})")
    sleep(0.2)  # Stabilization time

def control_relay(relay_name, state):
    init_gpio()

    if relay_name not in _relays:
        print(f"[ERROR] Unknown relay: {relay_name}")
        return

    relay = _relays[relay_name]

    if state == 1:
        relay.on()
        print(f"[ACTION] {relay_name} ON (GPIO {'HIGH' if ACTIVE_HIGH else 'LOW'})")
    elif state == 0:
        relay.off()
        print(f"[ACTION] {relay_name} OFF (GPIO {'LOW' if ACTIVE_HIGH else 'HIGH'})")
    else:
        print(f"[ERROR] Invalid state for {relay_name}: {state}. Use 0 or 1.")

def cleanup_gpio():
    """Turns off all relays and clears internal state."""
    for name, relay in _relays.items():
        relay.off()
        print(f"[CLEANUP] {name} relay set to OFF")
    _relays.clear()
    print("[CLEANUP] All relays cleaned up.")
