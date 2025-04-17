import socket
import json
import time

PLOC2D_IP = "192.168.1.242"
PLOC2D_PORT = 14158

def test_multi_job_camera_call(jobs):
    try:
        print(f"📡 Connecting to PLOC2D at {PLOC2D_IP}:{PLOC2D_PORT}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((PLOC2D_IP, PLOC2D_PORT))
        print("✅ Connection successful!")

        # Format job list
        job_list = [{"job": str(j)} for j in jobs]
        command = {"name": "Run.Locate", "jobs": job_list}
        command_json = json.dumps(command)

        print(f"📤 Sending JSON command: {command_json}")
        sock.sendall((command_json + "\n").encode())

        response = sock.recv(4096)
        sock.close()

        response_decoded = response.decode().strip()
        print("📩 Raw Camera Response:")
        print(response_decoded)

    except Exception as e:
        print(f"❌ Error during camera communication: {e}")

if __name__ == "__main__":
    # Try any combination you want here:
    test_multi_job_camera_call([12, 1])  # Replace with different job IDs as needed
