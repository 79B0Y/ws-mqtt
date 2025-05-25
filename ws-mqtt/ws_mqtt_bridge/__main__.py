import yaml
import time
import threading
import websocket
import paho.mqtt.client as mqtt
import os
import json
from urllib.parse import urlparse

CONFIG_PATH = os.path.join(os.getcwd(), "config.yaml")

with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)

mqtt_cfg = config['mqtt']
parsed = urlparse(mqtt_cfg['broker'])
mqtt_host = parsed.hostname or "localhost"
mqtt_port = parsed.port or 1883

ws_url = None
ws_connected = False
mqtt_connected = False
ws = None

def publish_status(client, status_type="status_report", info_override=None):
    info = info_override if info_override else {
        "mqtt": "connected" if mqtt_connected else "disconnected",
        "mqtt_broker": mqtt_host,
        "websocket": "connected" if ws_connected else "disconnected",
        "ws_url": ws_url
    }
    info["service_name"] = "ws_mqtt_bridge"
    payload = json.dumps({"type": status_type, "info": info, "ts": time.time()})
    print(f"📡 Status → MQTT [{status_type}]: {payload}")
    client.publish(mqtt_cfg['status_topic'], payload)

# MQTT Setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    global mqtt_connected
    mqtt_connected = True
    print("✅ MQTT connected")
    client.subscribe(mqtt_cfg['ws_url_topic'])
    client.subscribe(mqtt_cfg['status_request_topic'])
    if mqtt_cfg.get('subscribe_topic'):
        client.subscribe(mqtt_cfg['subscribe_topic'])
    publish_status(client, "mqtt_connected", {"rc": rc, "mqtt_broker": mqtt_host})

def on_disconnect(client, userdata, rc):
    global mqtt_connected
    mqtt_connected = False
    print("⚠️ MQTT disconnected")
    publish_status(client, "mqtt_disconnected", {"rc": rc, "mqtt_broker": mqtt_host})

def on_message(client, userdata, msg):
    global ws_url
    payload = msg.payload.decode()
    print(f"📥 MQTT Received [{msg.topic}]: {payload}")
    if msg.topic == mqtt_cfg['ws_url_topic']:
        ws_url = payload
        print(f"🔗 New WS URL from MQTT: {ws_url}")
        start_ws()
    elif msg.topic == mqtt_cfg['subscribe_topic']:
        if ws and ws.sock and ws.sock.connected:
            print(f"➡️ MQTT → WS: {payload}")
            ws.send(payload)
    elif msg.topic == mqtt_cfg['status_request_topic']:
        print("🔄 Status request received via MQTT")
        publish_status(client)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(mqtt_cfg['username'], mqtt_cfg['password'])
client.connect(mqtt_host, mqtt_port, 60)

def mqtt_loop():
    client.loop_forever()

mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.daemon = True
mqtt_thread.start()

# WebSocket Setup
def on_message_ws(wsapp, message):
    print(f"⬅️ WS → MQTT: {message}")
    client.publish(mqtt_cfg['publish_topic'], message)

def on_error(wsapp, error):
    print(f"❌ WS Error: {error}")
    publish_status(client, "ws_error", {"error": str(error)})

def on_close(wsapp, code, msg):
    global ws_connected
    ws_connected = False
    print("🔌 WS Disconnected")
    publish_status(client, "ws_disconnected", {"code": code, "reason": msg})

def on_open(wsapp):
    global ws_connected
    ws_connected = True
    print("🔗 WebSocket connected")
    publish_status(client, "ws_connected", {"url": ws_url})

def start_ws():
    global ws
    if ws_url:
        def run():
            global ws
            ws = websocket.WebSocketApp(
                ws_url,
                on_open=on_open,
                on_message=on_message_ws,
                on_error=on_error,
                on_close=on_close
            )
            ws.run_forever()
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

def periodic_status_reporter():
    while True:
        time.sleep(600)
        publish_status(client, "periodic_status")

periodic_thread = threading.Thread(target=periodic_status_reporter)
periodic_thread.daemon = True
periodic_thread.start()

def main():
    print("📡 Waiting for WebSocket URL via MQTT...")
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
