import os
import json


# use vagrant IP if env variable is not specified, generally for local testing
IP = os.environ.get("NOMAD_IP", "192.168.33.10")

# use vagrant PORT if env variable is not specified, generally for local
# testing
NOMAD_PORT = os.environ.get("NOMAD_PORT", 4646)


#Client Mocks
CLIENT_LS = json.dumps([
  {
    "Name": "alloc",
    "IsDir": True,
    "Size": 4096,
    "FileMode": "drwxrwxr-x",
    "ModTime": "2016-03-15T15:40:00.414236712-07:00"
  },
  {
    "Name": "redis",
    "IsDir": True,
    "Size": 4096,
    "FileMode": "drwxrwxr-x",
    "ModTime": "2016-03-15T15:40:56.810238153-07:00"
  }
])

CLIENT_STAT = json.dumps({
  "Name": "redis-syslog-collector.out",
  "IsDir": False,
  "Size": 96,
  "FileMode": "-rw-rw-r--",
  "ModTime": "2016-03-15T15:40:56.822238153-07:00"
})