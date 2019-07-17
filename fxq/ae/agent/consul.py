import requests

# r = requests.get('http://localhost:8500/v1/catalog/nodes')
# first_node = r.json()[0]
# print(first_node["Node"])


# service_def = {
#     "ID": "ae-agent-5000",
#     "Service": "ae-agent",
#     "Tags": [
#       "secure=false"
#     ],
#     "Address": "172.16.0.101",
#     "Meta": {},
#     "Port": 5000
#   }
#
# service_check = {
#     "Node": first_node["Node"],
#     "CheckID": "service:ae-agent-5000",
#     "Name": "Service 'ae-agent' check",
#     "Status": "passing",
#     "ServiceID": "ae-agent-5000",
#     "Definition": {
#       "Http": "http://172.16.0.101:5000/api/health",
#       "Interval": "15s",
#       "Timeout": "5s",
#       "DeregisterCriticalServiceAfter": "120s"
#     }
# }

service_def = {
  "ID": "service:ae-agent-5000",
  "Name": "ae-agent",
  "Tags": ["secure=false"],
  "Address": "172.16.0.101",
  "Port": 5000,
  "Meta": {},
  "EnableTagOverride": False,
  "Check": {
    "DeregisterCriticalServiceAfter": "60s",
    "HTTP": "http://172.16.0.101:5000/api/health",
    "Interval": "10s"
  },
  "Weights": {
    "Passing": 10,
    "Warning": 1
  }
}

# first_node["Service"] = service_def
# first_node["Check"] = service_check

r = requests.put('http://localhost:8500/v1/agent/service/register', json=service_def)
print(r.text)