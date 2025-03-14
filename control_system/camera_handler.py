import socket
import json

# PLOC2D Camera Connection Details
PLOC2D_IP = "192.168.1.242"  # Ensure this is the correct IP
PLOC2D_PORT = 14158          # Make sure this matches the Native Protocol setting

def trigger_camera(job_id=3):
    """Triggers the PLOC2D camera and waits for the full response."""
    try:
        print(f"📡 Connecting to PLOC2D at {PLOC2D_IP}:{PLOC2D_PORT}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Keep timeout at 5s
        sock.connect((PLOC2D_IP, PLOC2D_PORT))
        print("✅ Connection to PLOC2D successful!")

        # ✅ Send the JSON Command
        command_json = json.dumps({"name": "Run.Locate", "job": str(job_id)})
        sock.sendall((command_json + "\n").encode())  # Ensure newline at end
        print("📡 Command Sent to Camera:", command_json)

        # ✅ Read Full Response in a Loop (to avoid truncation)
        response = b""
        while True:
            try:
                chunk = sock.recv(4096)  # Read in chunks
                if not chunk:
                    break
                response += chunk
            except socket.timeout:
                print("⏳ Warning: Timeout while waiting for more data.")
                break

        response_decoded = response.decode()

        # ✅ Debug: Print the raw received response
        print("📩 Raw Camera Response:", response_decoded)

        sock.close()

        # ✅ Attempt to parse JSON
        try:
            json_data = json.loads(response_decoded)
            print("🎯 Parsed Camera Data:", json.dumps(json_data, indent=4))
            return json_data
        except json.JSONDecodeError:
            print("⚠️ Error: Response was not valid JSON!")
            return None

    except socket.timeout:
        print("❌ Camera Error: Timed Out - PLOC2D may not be sending data properly.")
        return None
    except ConnectionRefusedError:
        print("❌ Error: Connection refused - Is Native Protocol enabled in PLOC2D?")
        return None
    except socket.gaierror:
        print("❌ Error: Could not resolve IP address - Check your network settings.")
        return None
    except Exception as e:
        print(f"❌ Camera Error: {e}")
        return None
