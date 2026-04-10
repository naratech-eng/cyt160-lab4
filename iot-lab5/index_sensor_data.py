import os
import time
from pathlib import Path

import requests


def load_env_file() -> None:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_env_file()

ELASTIC_URL = os.getenv("ELASTIC_URL", "https://localhost:9200")
ELASTIC_USER = os.getenv("ELASTIC_USER", "elastic")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
VERIFY_TLS = os.getenv("ELASTIC_VERIFY_TLS", "false").lower() == "true"
ELASTIC_CA_CERT = os.getenv("ELASTIC_CA_CERT")


def main() -> None:
    if not ELASTIC_PASSWORD:
        raise RuntimeError("ELASTIC_PASSWORD is not set. Add it to .env or export it in shell.")

    verify_opt = False
    if VERIFY_TLS:
        verify_opt = ELASTIC_CA_CERT if ELASTIC_CA_CERT else True

    index_name = f"iot-sensor-data-{time.strftime('%Y.%m.%d')}"

    for i in range(30):
        temp = round(22.0 + i * 0.2, 1)
        humid = round(48.0 + i * 0.1, 1)
        doc = {
            "device": "rpi-iot-sensor",
            "sensor": {"temp": temp, "humid": humid},
            "unit": "C",
            "@timestamp": time.strftime(
                "%Y-%m-%dT%H:%M:%S.000Z",
                time.gmtime(time.time() - (30 - i) * 60),
            ),
            "tags": ["mqtt_sensor"],
        }

        requests.post(
            f"{ELASTIC_URL}/{index_name}/_doc",
            json=doc,
            headers={"Content-Type": "application/json"},
            auth=(ELASTIC_USER, ELASTIC_PASSWORD),
            verify=verify_opt,
            timeout=10,
        )

    print("Indexed 30 sensor readings")


if __name__ == "__main__":
    main()
