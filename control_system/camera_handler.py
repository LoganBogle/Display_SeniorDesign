import socket
import json
import time

PLOC2D_IP = "192.168.1.242"
PLOC2D_PORT = 14158

def trigger_camera(job_id=3):
    try:
        t_start = time.time()
        print(f"📡 Connecting to PLOC2D at {PLOC2D_IP}:{PLOC2D_PORT}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((PLOC2D_IP, PLOC2D_PORT))
        print(f"✅ Connected at {time.time() - t_start:.3f} seconds")

        command_json = json.dumps({"name": "Run.Locate", "job": str(job_id)})
        sock.sendall((command_json + "\n").encode())
        print(f"📤 Command sent at {time.time() - t_start:.3f} seconds")

        # ✅ Try to read full response (blocking, raw socket)
        response = sock.recv(4096)
        sock.close()

        t_end = time.time()
        response_decoded = response.decode().strip()
        print(f"📩 Response received at {t_end - t_start:.3f} seconds")
        print("📄 Raw Camera Response:", response_decoded)

        if not response_decoded:
            print("❌ Camera Error: Empty response")
            return None

        json_data = json.loads(response_decoded)
        print("✅ Parsed Response:", json_data)

        return {
            "x": json_data.get("x", 0.0),
            "y": json_data.get("y", 0.0),
            "z": json_data.get("z", 0.0),
            "r1": json_data.get("r1", 0.0),
            "r2": json_data.get("r2", 0.0),
            "r3": json_data.get("r3", 0.0),
            "score": json_data.get("score", 0.0),
            "matches": json_data.get("matches", 0)
        }

    except Exception as e:
        print(f"❌ Camera Error: {e}")
        return None
