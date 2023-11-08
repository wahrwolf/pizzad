from enum import Enum, auto


class Event(Enum):
    ORDER_CLOSED = auto()
    ORDER_CLOSE_FAILED = auto()

    ORDER_CREATED = auto()
    ORDER_CREATE_FAILED = auto()

    ERROR = ORDER_CLOSE_FAILED | ORDER_CREATE_FAILED
