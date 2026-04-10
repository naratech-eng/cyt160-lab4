import paho.mqtt.client as mqtt
import time
import json

try:
    import Adafruit_DHT

    SENSOR = Adafruit_DHT.DHT22
    GPIO_PIN = 4
    USE_REAL = True
    print("[*] DHT22 sensor detected.")
except ImportError:
    USE_REAL = False
    print("[!] No DHT library - using simulated values.")

BROKER = "50.17.110.31"  # update each session
PORT = 1883
TOPIC = "iot/sensor/temperature"
READINGS = 30
DELAY_SECONDS = 1
RUNTIME_FALLBACK_NOTICE_SHOWN = False


def get_simulated_reading(index):
    temp = round(22.0 + index * 0.2, 1)
    humidity = round(48.0 + index * 0.1, 1)
    return temp, humidity


def get_reading(index):
    global RUNTIME_FALLBACK_NOTICE_SHOWN

    if USE_REAL:
        humidity, temp = Adafruit_DHT.read_retry(SENSOR, GPIO_PIN)
        if temp is not None and humidity is not None:
            return temp, humidity

        if not RUNTIME_FALLBACK_NOTICE_SHOWN:
            print(
                "[!] Hardware sensor not connected or not configured; using simulated readings."
            )
            RUNTIME_FALLBACK_NOTICE_SHOWN = True
        return get_simulated_reading(index)

    return get_simulated_reading(index)


def build_payload(temp, humidity):
    return json.dumps(
        {
            "device": "rpi-iot-sensor",
            "temp": round(float(temp), 1),
            "humid": round(float(humidity), 1),
            "unit": "C",
            "ts": time.time(),
        }
    )


def publish_readings(client):
    print(f"[*] Connected. Publishing {READINGS} readings to {TOPIC}...")
    for i in range(READINGS):
        temp, humidity = get_reading(i)

        payload = build_payload(temp, humidity)
        client.publish(TOPIC, payload)
        print(f" [{i + 1:02d}/{READINGS}] {payload}")
        time.sleep(DELAY_SECONDS)


def main():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    publish_readings(client)

    client.disconnect()
    print("[*] Done.")


if __name__ == "__main__":
    main()
