# Pi Publisher/Client Simulation

This folder contains the Raspberry Pi MQTT client scripts used to simulate normal and attack traffic for Suricata testing.

- `sensor.py`: sends baseline sensor data and one malformed payload sample.
- `mqtt_flood.py`: sends high-rate publish traffic to trigger the rate-limit alert (`sid:2000001`).
- `mqtt_malformed.py`: sends malformed payloads (`undefined`, long repeated `A` bytes) to trigger malformed-content alerts (`sid:2000002`, `sid:2000003`).
- `mqtt_publish_tls.py`: sends nominal MQTT messages over TLS (`8883`) for encrypted-traffic validation.

These scripts were used to generate simulation traffic and related `.pcap` captures for lab validation.
