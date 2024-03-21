from abc import ABC, abstractmethod
from collections import defaultdict
from ..pb.bookstore.order_pb2 import Timestamp

def max_timestamp(t1: Timestamp, t2: Timestamp):
    """Returns a new Timestamp combining the values of t1 and t2 using max."""
    result = Timestamp()
    for process in Timestamp.DESCRIPTOR.fields:
        setattr(result, process.name, max(getattr(t1, process.name), getattr(t2, process.name)))
    return result


def timestamp_to_str(timestamp: Timestamp) -> str:
    return f"({', '.join(str(getattr(timestamp, process.name)) for process in Timestamp.DESCRIPTOR.fields)})"


class ClockService(ABC):
    def __init__(self):
        self.vector_clocks: defaultdict[str, Timestamp] = defaultdict(Timestamp)

    @property
    @abstractmethod
    def service_name(self) -> str:
        raise NotImplementedError
    
    def inc_clock(self, order_id: str, message: str = None):
        old_clock = getattr(self.vector_clocks[order_id], self.service_name)
        setattr(self.vector_clocks[order_id], self.service_name, old_clock + 1)
        if message is not None:
            print(f"{order_id} - {timestamp_to_str(self.vector_clocks[order_id])}: {message}")
        return self.vector_clocks[order_id]

    def update_clock(self, order_id: str, timestamp: Timestamp, message: str = None):
        self.vector_clocks[order_id] = max_timestamp(self.vector_clocks[order_id], timestamp)
        self.inc_clock(order_id)
        if message is not None:
            print(f"{order_id} - {timestamp_to_str(self.vector_clocks[order_id])}: {message}")
        return self.vector_clocks[order_id]
