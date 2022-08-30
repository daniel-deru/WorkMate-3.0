from enum import Enum

class ServerConnectStatus(Enum):
    verified: str = "verified"
    denied: str = "denied"
    failed: str = "failed"
    
class RegisterStatus(Enum):
    user_created: str = "user created"
    window_closed: str = "window closed"