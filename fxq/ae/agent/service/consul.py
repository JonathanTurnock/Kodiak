import logging
import os
import requests
from fxq.core.stereotype import Service

LOGGER = logging.getLogger(__name__)


@Service
class ConsulService:
    def __init__(self):
        self.host = os.environ["spring.cloud.consul.discovery.hostname"]
        self.port = 5000
        self.consul_host = os.environ["spring.cloud.consul.host"]
        self.consul_port = 8500
        self._register_host()

    def _register_host(self):
        service_def = {
            "ID": "service:ae-agent-5000",
            "Name": "ae-agent",
            "Tags": ["secure=false"],
            "Address": self.host,
            "Port": self.port,
            "Meta": {
            },
            "EnableTagOverride": False,
            "Check": {
                "DeregisterCriticalServiceAfter": "60s",
                "HTTP": f"http://{self.host}:{self.port}/api/actuator/health",
                "Interval": "10s"
            },
            "Weights": {
                "Passing": 10,
                "Warning": 1
            }
        }

        requests.put(f'http://{self.consul_host}:{self.consul_port}/v1/agent/service/register', json=service_def)
