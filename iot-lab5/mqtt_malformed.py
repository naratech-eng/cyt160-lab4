import time

import paho.mqtt.client as mqtt
from scapy.all import IP, TCP, Raw, send

TARGET = "52.201.6.72"  # Replace with current session IP.
PORT = 1883
TOPIC = "iot/lab/topic"


def main() -> None:
    # Part A: MQTT payloads via paho.
    print("[*] Sending malformed MQTT payloads (paho)...")
    client = mqtt.Client(client_id="rpi-malformed-sim")
    client.connect(TARGET, PORT, 60)

    # Triggers SID 2000002: "undefined" payload.
    client.publish(TOPIC, "undefined")
    print(" Sent: undefined payload")
    time.sleep(0.5)

    # Triggers SID 2000002: undefined inside JSON-like string.
    client.publish(TOPIC, '{"value": undefined}')
    print(' Sent: {"value": undefined}')
    time.sleep(0.5)

    # Triggers SID 2000003: repeated-byte buffer probe.
    client.publish(TOPIC, "A" * 400)
    print(" Sent: A*400 payload")
    time.sleep(0.5)
    client.disconnect()

    # Part B: Raw scapy packets.
    print("[*] Sending raw scapy payloads...")
    try:
        send(IP(dst=TARGET) / TCP(dport=PORT) / Raw(load=b"A" * 400), count=10, verbose=0)
        print(" Sent: 10 raw A*400 packets")
    except PermissionError:
        print("[!] Raw Scapy send requires root privileges.")
        print("[!] Re-run with sudo to send raw packets.")
    print("[*] Malformed payload simulation complete.")


if __name__ == "__main__":
    main()
