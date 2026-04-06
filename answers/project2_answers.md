# Project 2 Answers

## Question 1
SID 2000001 uses `threshold: type threshold, track by_src, count 100, seconds 60`. The flood script sends 150 messages at 0.35-second intervals. How many alert events for SID 2000001 did you see in `eve.json`? Explain why the threshold keyword controls how many alerts fire, not just whether one fires at all.

## Answer 1
I observed **1 alert event** for `sid:2000001` in `eve.json`.

Why one alert (not many): the rule uses `threshold:type threshold, track by_src, count 100, seconds 60`.
- `track by_src` means Suricata counts events per source IP.
- `count 100, seconds 60` means the alert condition is reached after 100 matching packets/messages from that source within 60 seconds.
- With `type threshold`, Suricata alerts when the threshold is crossed, then suppresses additional alerts for that same source during the active threshold window.

So threshold controls **alert frequency/rate**, not only yes/no detection.

## Question 2
The flood simulation uses `paho-mqtt` on port `1883` (plaintext) rather than port `8883` (TLS). Looking at your Lab 5 analysis Q3 answer, explain why Suricata can inspect the payload on port 1883 but not on port 8883. What are the trade-offs between running attacks on the plaintext versus TLS port for testing purposes?

## Answer 2
Suricata can inspect payload on port `1883` because MQTT is plaintext there. It can parse application-layer content and match `content` patterns directly.

On port `8883`, MQTT runs inside TLS. Without TLS decryption keys/session context, Suricata sees encrypted bytes only, so payload signatures (like `undefined` or repeated `A` patterns) are not visible.

Trade-offs:
- **Plaintext (1883):** best for IDS rule development/validation because payload rules are testable and observable.
- **TLS (8883):** realistic production security/confidentiality, but payload-based signatures lose visibility unless a decryption strategy is added.

## Question 3
SID 2000003 uses `depth:100`. The malformed script sends `'A'*400`. Would the rule still fire if the repeated pattern started at byte 200 of the payload? Explain what `depth:` means and how you would change the rule to detect a late-starting pattern.

## Answer 3
If the repeated `A...` pattern starts at byte 200, this rule with `depth:100` would likely **not fire**.

`depth` limits how far into the payload Suricata searches from the start of the payload for that `content`.
- `depth:100` means only the first 100 bytes are inspected for that content match.

To detect a late-starting pattern, remove/relax `depth` or use explicit position controls, for example:
- remove `depth` entirely, or
- use `offset:200` (and optionally a larger `depth`) to search starting later in payload.

## Question 4
Your rules use the `alert` action (IDS mode — log only). Name two specific changes you would make — one in the rule file and one in the Suricata/Docker configuration — to switch to IPS mode and actively drop matching packets instead of just alerting.

## Answer 4
To switch from IDS alert-only to IPS dropping:

1. **Rule file change (detection action):**
   - change `alert tcp ...` to `drop tcp ...` for rules you want to block.

2. **Suricata/Docker runtime change (inline mode):**
   - run Suricata in inline IPS mode using NFQUEUE/iptables integration (instead of passive sniffing).
   - in practice: configure host firewall rules to send traffic to `NFQUEUE`, and run Suricata with NFQ support so `drop` actions are enforced.

Without inline packet path integration, `drop` rules still behave like alerts only.
