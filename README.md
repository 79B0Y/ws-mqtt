
# WebSocket ↔ MQTT Bridge (Dynamic WebSocket URL via MQTT)

A Python-based bridge that connects to an MQTT broker and listens for WebSocket URLs via MQTT topic. Once a WebSocket URL is received, it connects to the WebSocket server and bridges messages between WebSocket and MQTT.

---

## 📦 Features

- MQTT is used to dynamically set the WebSocket URL
- WebSocket → MQTT message forwarding
- MQTT → WebSocket command forwarding
- Auto-reconnect on WebSocket failure
- YAML configuration for MQTT only

---

## 🧱 Requirements

- Python 3.7+
- MQTT Broker (e.g., Mosquitto)
- Optional: [n8n](https://n8n.io) for message automation

---

## 🚀 Installation

```bash
git clone https://github.com/yourname/ws-mqtt-bridge.git
cd ws-mqtt-bridge
pip install .
```

---

## 🛠 Configuration (`config.yaml`)

```yaml
mqtt:
  broker: "mqtt://localhost:1883"
  username: "your_username"
  password: "your_password"
  publish_topic: "bridge/incoming"
  subscribe_topic: "bridge/outgoing"
  ws_url_topic: "bridge/wsurl"
```

---

## 📡 MQTT Protocol Design

| Topic             | Direction         | Description |
|------------------|-------------------|-------------|
| `bridge/wsurl`   | MQTT → Bridge     | Set the WebSocket URL dynamically |
| `bridge/incoming`| WS → MQTT         | Data from WebSocket gets published here |
| `bridge/outgoing`| MQTT → WS (opt.)  | Commands to be sent to the WebSocket |

Example: Send a WebSocket URL to connect

```bash
mosquitto_pub -t bridge/wsurl -m "wss://example.com/ws"
```

---

## 🔁 Integration with n8n

You can use `MQTT Trigger` and `MQTT Publish` nodes in n8n:

### 1. Trigger WebSocket Connection

- **Node**: `MQTT Publish`
- **Topic**: `bridge/wsurl`
- **Payload**: `"wss://your.websocket.server/path"`

### 2. Receive WebSocket Messages

- **Node**: `MQTT Trigger`
- **Topic**: `bridge/incoming`
- You’ll get WebSocket data as message payload here

### 3. Send Commands to WebSocket

- **Node**: `MQTT Publish`
- **Topic**: `bridge/outgoing`
- **Payload**: Any valid command your WS server expects

These nodes require an `MQTT Broker` credential configured in n8n with same broker info as in `config.yaml`.

---

## ▶️ Run the Bridge

```bash
ws-mqtt
```

Console will show status logs.

---

## 🧪 Testing Tools

- [MQTT Explorer](https://mqtt-explorer.com) for MQTT
- [wscat](https://github.com/websockets/wscat) to emulate WebSocket server

---

## 📄 License

MIT
