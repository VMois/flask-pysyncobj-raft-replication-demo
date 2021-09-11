# Flask + PySyncObj Raft replication demo

## Testing

Examples of commands to start node for local testing:

```bash
python3 main.py --flask_host localhost:5000 --raft_host localhost:6000 --partners localhost:6001 localhost:6002
python3 main.py --flask_host localhost:5001 --raft_host localhost:6001 --partners localhost:6000 localhost:6002
python3 main.py --flask_host localhost:5002 --raft_host localhost:6002 --partners localhost:6001 localhost:6000
```

Send POST request:

```python
import requests
headers = {'Content-type': 'application/json'}
requests.post('http://localhost:5000/task', json={'some_key': 'some_value'})
```
