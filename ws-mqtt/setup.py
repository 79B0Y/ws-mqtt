
from setuptools import setup, find_packages

setup(
    name="ws_mqtt_bridge",
    version="0.5",
    packages=find_packages(),
    install_requires=["paho-mqtt", "websocket-client", "pyyaml"],
    entry_points={
        'console_scripts': [
            'ws-mqtt=ws_mqtt_bridge.__main__:main'
        ]
    },
)
