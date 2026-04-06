import json
import time

import paho.mqtt.client as mqtt

BROKER = "52.201.6.72"  # Replace with current session IP.
PORT = 1883  # Plaintext so Suricata can inspect payloads.
TOPIC = "iot/lab/topic"


def main() -> None:
    client = mqtt.Client(client_id="rpi-flood-sim")
    client.connect(BROKER, PORT, 60)

    # Send 150 messages in under 60 seconds to trigger SID 2000001.
    # Threshold is 100 in 60 seconds; 150 guarantees it fires.
    print("[*] Starting flood simulation - 150 messages in ~55 seconds...")
    count = 0
    start = time.time()

    while count < 150:
        payload = json.dumps({"flood_seq": count, "ts": time.time()})
        client.publish(TOPIC, payload)
        count += 1
        time.sleep(0.35)  # ~171 msgs/min, above the 100/min threshold.

    elapsed = round(time.time() - start, 1)
    print(f"[*] Sent {count} messages in {elapsed}s. Flood complete.")
    client.disconnect()


if __name__ == "__main__":
    main()
