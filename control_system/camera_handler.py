import socket
import json
import time

PLOC2D_IP = "192.168.1.242"
PLOC2D_PORT = 14158

def trigger_camera(job_ids):
    """
    Triggers one or more camera jobs and returns a dict of results keyed by job ID.
    """
    if isinstance(job_ids, int):  # if someone passes a single int, convert to list
        job_ids = [job_ids]

    results = {}

    for job_id in job_ids:
        try:
            t_start = time.time()
            print(f"📡 Connecting to PLOC2D at {PLOC2D_IP}:{PLOC2D_PORT}...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((PLOC2D_IP, PLOC2D_PORT))
            print(f"✅ Connected at {time.time() - t_start:.3f} seconds")

            command_json = json.dumps({"name": "Run.Locate", "job": str(job_id)})
            sock.sendall((command_json + "\n").encode())
            print(f"📤 Command for Job {job_id} sent at {time.time() - t_start:.3f} seconds")

            response = sock.recv(4096)
            sock.close()

            t_end = time.time()
            response_decoded = response.decode().strip()
            print(f"📩 Response for Job {job_id} received at {t_end - t_start:.3f} seconds")
            print("📄 Raw Camera Response:", response_decoded)

            if not response_decoded:
                print(f"❌ Camera Error: Empty response for job {job_id}")
                results[str(job_id)] = None
                continue

            json_data = json.loads(response_decoded)
            print("✅ Parsed Response:", json_data)

            results[str(job_id)] = {
                "name": json_data.get("name", ""),
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
            print(f"❌ Camera Error for job {job_id}: {e}")
            results[str(job_id)] = None

    return results
