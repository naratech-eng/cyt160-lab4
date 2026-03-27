# CYT-160 Lab 4: MQTT IDS Pipeline with Suricata + Filebeat

This project builds a lightweight intrusion detection pipeline for MQTT traffic using Docker Compose.

Elasticsearch is used as the alert storage backend, and Filebeat ships Suricata events into Elasticsearch indices.

It runs three containers:
- `mosquitto` (MQTT broker)
- `suricata` (network IDS monitoring MQTT traffic)
- `filebeat` (ships Suricata alerts to Elasticsearch)

## Field Data Source (Current Lab Usage)

- Sensor publisher device: Raspberry Pi 5
- Sensor type: moisture sensor
- Publisher script: `sensor.py` on Raspberry Pi 5
- Deployment target: AWS EC2 instance (used as the VM host for this lab stack)
- Transport path: Raspberry Pi publishes moisture readings over MQTT to Mosquitto on EC2.
- End-to-end flow: `Pi5(sensor.py) -> EC2:1883 -> Mosquitto | Suricata monitors traffic -> eve.json -> Filebeat -> Elasticsearch`

## Project Structure

```text
.
├── docker-compose.yml
├── mosquitto/
│   └── config/mosquitto.conf
├── suricata/
│   └── rules/local.rules
└── filebeat/
    └── filebeat.yml
```

## How It Works

1. `mosquitto` listens on TCP `1883` on the EC2 VM and accepts anonymous clients.
2. `suricata` shares the broker's network namespace (`network_mode: service:mosquitto`) and inspects traffic on `eth0`.
3. Custom IDS signatures in `suricata/rules/local.rules` detect suspicious MQTT payload patterns.
4. Suricata writes events to `eve.json` in a shared Docker volume.
5. `filebeat` reads `/suricata-logs/eve.json` and sends events to Elasticsearch at `https://host.docker.internal:9200`.

## Detection Rules Included

Current custom Suricata alerts:
- `sid:1000001` — Detects a long repeated `A...` payload pattern.
- `sid:1000002` — Detects the string `rm -rf` in traffic to MQTT port `1883`.

## Prerequisites

- Docker Desktop (or Docker Engine + Compose plugin)
- An accessible Elasticsearch instance on the host machine at `https://localhost:9200`
- A valid Elasticsearch password for the `elastic` user

## Setup

1. In the project root, set your Elasticsearch password in the shell:

```bash
export ELASTIC_PASSWORD='your_elastic_password'
```

2. Start the stack:

```bash
docker compose up -d
```

3. Confirm all services are running:

```bash
docker compose ps
```

## Verifying Alerts

### 1) Trigger traffic that matches a local Suricata rule

From your host (requires an MQTT publisher client):

```bash
mosquitto_pub -h localhost -p 1883 -t test/topic -m 'rm -rf /tmp'
```

### 2) Check Suricata logs

```bash
docker compose logs suricata --tail=100
```

### 3) Check Filebeat logs

```bash
docker compose logs filebeat --tail=100
```

### 4) Query Elasticsearch indices

```bash
curl -k -u elastic:$ELASTIC_PASSWORD "https://localhost:9200/_cat/indices/suricata-alerts-*?v"
```

## Useful Commands

- Start: `docker compose up -d`
- Stop: `docker compose down`
- Restart: `docker compose restart`
- Follow all logs: `docker compose logs -f`

## Troubleshooting

- If `filebeat` cannot authenticate, verify `ELASTIC_PASSWORD` is exported before starting containers.
- If no alerts appear, ensure test traffic is sent to port `1883` and matches one of the local Suricata rule patterns.
- If Elasticsearch is not reachable, confirm it is available on the host at `https://localhost:9200` and that Docker can resolve `host.docker.internal`.