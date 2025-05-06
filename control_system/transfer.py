def get_parallel_offset(tray_id, x_val, r3):
    if tray_id == 1:
        # Adjust slope and intercept for Tray 1
        m = 0.04  # just an example
        b = -21.5
    elif tray_id == 2:
        # Your original calibration
        m = 0.0377
        b = -20.3
    elif tray_id == 3:
        # Adjust for Tray 3
        m = 0.042  # example guess
        b = -23.0
    else:
        m = 0
        b = 0

    offset_mag = m * x_val + b
    return offset_mag if r3 >= 0 else -offset_mag


parallel_offset = get_parallel_offset(tray_id, coordinates['x'], coordinates['r3'])
perpendicular_offset = 4  # still fixed

r3_rad = math.radians(coordinates['r3'])

x_adj = (
    coordinates['x']
    + parallel_offset * math.cos(r3_rad)
    - perpendicular_offset * math.sin(r3_rad)
)
y_adj = (
    coordinates['y']
    + parallel_offset * math.sin(r3_rad)
    + perpendicular_offset * math.cos(r3_rad)
)