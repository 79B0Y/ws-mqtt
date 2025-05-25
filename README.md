
# WebSocket ↔ MQTT Bridge (v0.5)

This document describes the design, configuration, and usage of `ws-mqtt` v0.4, which connects WebSocket servers and MQTT brokers with advanced status reporting and bi-directional message bridging.

---

## 📦 Key Features

- ✅ Receives WebSocket URL dynamically via MQTT (`bridge/wsurl`)
- 🔁 Bridges messages between WebSocket and MQTT
- 📡 Sends automatic status reports to `bridge/status`
- 📥 Supports MQTT-initiated status requests via `bridge/status/get`
- 🕒 Sends **periodic status updates every 10 minutes**

---

## 📑 Configuration (`config.yaml`)

```yaml
mqtt:
  broker: "127.0.0.1"
  username: "admin"
  password: "admin"
  publish_topic: "bridge/incoming"
  subscribe_topic: "bridge/outgoing"
  ws_url_topic: "bridge/wsurl"
  status_topic: "bridge/status"
  status_request_topic: "bridge/status/get"
```

Place `config.yaml` in the same directory where you run `ws-mqtt`.

---

## 📡 MQTT Topic Overview

| Topic               | Direction        | Description                                      |
|--------------------|------------------|--------------------------------------------------|
| `bridge/wsurl`     | MQTT → Bridge    | Dynamically configure WebSocket URL              |
| `bridge/incoming`  | Bridge → MQTT    | Messages received from WebSocket                 |
| `bridge/outgoing`  | MQTT → Bridge    | Messages to send to WebSocket                    |
| `bridge/status`    | Bridge → MQTT    | Bridge status reports                            |
| `bridge/status/get`| MQTT → Bridge    | Trigger status report immediately                |

---

## 🕒 Periodic Status Push

Every 10 minutes, the bridge publishes the following JSON to `bridge/status`:

```json
{
  "type": "periodic_status",
  "info": {
    "mqtt": "connected",
    "mqtt_broker": "127.0.0.1",
    "websocket": "connected",
    "ws_url": "ws://192.168.1.100/ws"
  },
  "ts": 1716543030.153
}
```

---

## 🚀 Usage

### Installation

```bash
unzip ws-mqtt-v0.4-periodic.zip
cd ws-mqtt
pip install .
cp config.yaml.example config.yaml  # or edit manually
```

### Start the bridge

```bash
ws-mqtt
```

### Send WebSocket URL via MQTT

```bash
mosquitto_pub -t bridge/wsurl -m "ws://192.168.0.100:8080/ws"
```

### Send a message to WebSocket

```bash
mosquitto_pub -t bridge/outgoing -m '{"command": "ping"}'
```

### Receive message from WebSocket

```bash
mosquitto_sub -t bridge/incoming
```

### Request status manually

```bash
mosquitto_pub -t bridge/status/get -m ""
mosquitto_sub -t bridge/status
```

---

## 📡 Integration with n8n

- Use **MQTT Publish** node to `bridge/wsurl` or `bridge/outgoing`
- Use **MQTT Trigger** node for `bridge/incoming` and `bridge/status`

---

## 🔒 Security Tips

- Use strong MQTT authentication
- Isolate network access or use TLS
- Restrict `bridge/status/get` topic if needed

---

## 🛠 Possible Extensions

- Configurable status interval
- Add request_id to status responses
- Status caching and REST endpoint
- Docker container + health probe

---

## 📄 License

MIT — Developed for LinknLink AIoT integration.
