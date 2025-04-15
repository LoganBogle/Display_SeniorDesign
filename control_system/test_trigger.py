# test_trigger.py
import relay_api
import time

relay_api.tray1(1)  # ON
time.sleep(0.5)
relay_api.tray1(0)  # OFF
time.sleep(0.5)
relay_api.tray2(1)  # ON
time.sleep(0.5)
relay_api.tray2(0)  # OFF
time.sleep(0.5)
relay_api.tray3(1)  # ON
time.sleep(0.5)
relay_api.tray3(0)  # OFF
time.sleep(0.5)

