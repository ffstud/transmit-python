from enum import Enum

class PacketType(Enum):
    INITIALIZATION = 0
    DATA = 1
    FINALIZE = 2