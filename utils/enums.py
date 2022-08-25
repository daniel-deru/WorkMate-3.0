from enum import Enum

class ServerConnectStatus(Enum):
    verified: str = "verified"
    denied: str = "denied"
    failed: str = "failed"