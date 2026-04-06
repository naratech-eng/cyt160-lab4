import json
import ssl
import time

import paho.mqtt.client as mqtt

BROKER = "52.201.6.72"  # Replace with current session IP.
PORT = 8883  # TLS port.
TOPIC = "iot/lab/topic"
CA = "/home/nara/iot-lab/mqtt-certs/ca.crt"
CERT = "/home/nara/iot-lab/mqtt-certs/client.crt"
KEY = "/home/nara/iot-lab/mqtt-certs/client.key"


def main() -> None:
    client = mqtt.Client(client_id="rpi-tls-client")

    # Configure TLS: CA verifies broker, client cert/key enables mutual TLS.
    client.tls_set(
        ca_certs=CA,
        certfile=CERT,
        keyfile=KEY,
        tls_version=ssl.PROTOCOL_TLSv1_2,
    )

    print("[*] Connecting to broker with TLS...")
    client.connect(BROKER, PORT, 60)
    print("[*] Connected.")

    for i in range(10):
        payload = json.dumps(
            {
                "device": "rpi-tls-client",
                "temp": 20 + i * 0.5,
                "unit": "C",
            }
        )
        client.publish(TOPIC, payload)
        print(f"Sent: {payload}")
        time.sleep(1)

    client.disconnect()
    print("[*] Done.")


if __name__ == "__main__":
    main()
