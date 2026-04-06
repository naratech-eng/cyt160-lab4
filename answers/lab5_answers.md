# Lab 5 Answers

## Q1
Open both pcaps with `tcpdump -r <file> -nn -A` and compare the output. List three specific things that are visible in the plaintext capture but hidden in the TLS capture. What does this mean for an attacker who can intercept network traffic between the Pi and the broker?

From captures:

1. The MQTT application payload is readable on `1883` (for example `temp:20C`, `temp:21C`, ...).
2. The MQTT topic + payload content appears directly in plaintext capture (for example `sensor/data` + sensor value bytes).
3. Message semantics are exposed (normal telemetry vs suspicious/malformed content can be read directly when not encrypted).

In the TLS capture on `8883`, the packet payload is encrypted, so the attacker cannot directly read or modify message content in transit without breaking TLS/session keys. They can still see metadata (IPs, ports, timing, packet sizes), but not the actual sensor message content.

## Q2
Your `mosquitto.conf` sets `require_certificate true`. What does this mean for a client that tries to connect without a certificate? Test it: run `mosquitto_sub -h <VM_IP> -p 8883 -t '#'` from a terminal that does NOT provide `--cafile`, `--cert`, and `--key` flags. What error message do you get? Why is this a security improvement over `allow_anonymous true`?

`require_certificate true` means the broker enforces mutual TLS: clients must present a valid client certificate signed by the trusted CA. A client that connects without cert/key is rejected during TLS/authentication (handshake/connection failure).

Security improvement over `allow_anonymous true`:

- Only enrolled devices with valid certificates can connect.
- Unauthorized clients cannot subscribe/publish even if they know host/port.
- It reduces spoofing, rogue publishers, and unauthorized data access.

## Q3
Suricata is monitoring port `1883` (plaintext). It cannot read the encrypted payload on port `8883` without the TLS session keys. Given this limitation, what can Suricata still usefully observe about TLS traffic — and how would you use that to detect a threat on port `8883`? This is relevant to the rules you will write in Project 2.

Even on TLS traffic, Suricata can still observe:

- Source/destination IPs, ports, and connection direction.
- Connection rates, session frequency, and timing patterns (beaconing/bursts).
- Packet/flow sizes and bytes transferred (volume anomalies).
- TLS handshake metadata (version/cipher/cert-related fields depending on visibility).

How to detect threats on `8883`:

- Alert on unusual connection spikes from one client IP.
- Alert on repeated failed handshakes / short failed sessions.
- Alert on abnormal traffic volume for a device baseline.
- Correlate known device IP/behavior baselines with deviations (new endpoints, unusual timing, sudden exfil-like volume).
