import json
from pathlib import Path

# Load resume formatting configuration
_config_path = Path(__file__).with_suffix('.json')

# Check if the configuration file exists
print(f"Loading resume configuration from {_config_path}")

try:
    with open(_config_path, 'r') as _f:
        CONF = json.load(_f)
except Exception:
    CONF = {}