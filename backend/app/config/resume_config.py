import json
from pathlib import Path

# Load resume formatting configuration
_config_path = Path(__file__).with_suffix('.json')
try:
    with open(_config_path, 'r') as _f:
        CONF = json.load(_f)
except Exception:
    CONF = {}