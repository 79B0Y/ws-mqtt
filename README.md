
# WebSocket ↔ MQTT Bridge (Verbose Edition)

This document provides a comprehensive **design overview** and **usage guide** for the `ws-mqtt` bridge tool that enables seamless integration between a WebSocket server and an MQTT broker.

---

## 📌 Overview

`ws-mqtt` is a Python-based tool that dynamically bridges WebSocket streams and MQTT topics. It is designed to be:

- **Dynamic**: WebSocket URL is provided via MQTT (`bridge/wsurl`)
- **Bidirectional**: Supports sending/receiving messages to/from WebSocket and MQTT
- **Observable**: All major actions are logged to console and status events are published to MQTT
- **Easy to Integrate**: Compatible with n8n and Home Assistant via MQTT

---

## ⚙️ System Design

### MQTT Topics

| Topic               | Direction        | Purpose                                           |
|--------------------|------------------|---------------------------------------------------|
| `bridge/wsurl`     | MQTT → Bridge    | Dynamically sets WebSocket URL                   |
| `bridge/incoming`  | Bridge → MQTT    | Publishes messages received from WebSocket       |
| `bridge/outgoing`  | MQTT → Bridge    | Sends MQTT-published commands to WebSocket       |
| `bridge/status`    | Bridge → MQTT    | Publishes status updates (JSON)                  |

### Status Messages (JSON format)

Published to `bridge/status`:

```json
{
  "type": "ws_connected",
  "info": {
    "url": "ws://192.168.0.10:8080"
  },
  "ts": 1716541512.825
}
```

Possible types:
- `mqtt_connected`
- `mqtt_disconnected`
- `ws_connected`
- `ws_disconnected`
- `ws_error`

---

## 📦 Installation

1. Extract the package:
```bash
unzip ws-mqtt-verbose.zip
cd ws-mqtt
```

2. Install the package:
```bash
pip install .
```

3. Prepare configuration file:
```bash
cp config.yaml.example config.yaml
```

---

## 🛠️ Configuration (`config.yaml`)

Example:

```yaml
mqtt:
  broker: "127.0.0.1"
  username: "admin"
  password: "admin"
  publish_topic: "bridge/incoming"
  subscribe_topic: "bridge/outgoing"
  ws_url_topic: "bridge/wsurl"
  status_topic: "bridge/status"
```

Place `config.yaml` in the **same directory** where you run the `ws-mqtt` command.

---

## 🚀 Usage

1. Start the bridge:
```bash
ws-mqtt
```

2. Use MQTT to send a WebSocket URL:
```bash
mosquitto_pub -t bridge/wsurl -m "ws://192.168.0.100:8080/ws"
```

3. Send a command from MQTT to WebSocket:
```bash
mosquitto_pub -t bridge/outgoing -m '{"command":"ping"}'
```

4. Observe messages returned from WebSocket via:
```bash
mosquitto_sub -t bridge/incoming
```

5. Monitor status messages:
```bash
mosquitto_sub -t bridge/status
```

---

## 🔁 Integration with n8n

You can use the following nodes:

- **MQTT Publish** to `bridge/wsurl` — set WebSocket URL
- **MQTT Publish** to `bridge/outgoing` — send control commands
- **MQTT Trigger** from `bridge/incoming` — receive WS responses
- **MQTT Trigger** from `bridge/status` — monitor bridge state

---

## 🔒 Security Tips

- Enable MQTT username/password auth (already supported)
- Add TLS with Mosquitto (not yet handled in code)
- Consider allowing only internal network access

---

## 🧩 Extension Ideas

- Support multiple WebSocket connections
- Persistent WebSocket reconnect
- Retained status via MQTT
- Message queueing and retry
- Dockerization and systemd service wrapper

---

## 📄 License

MIT

(C) 2024 by LinknLink – Customized for AIoT applications and edge automation.
