from abc import ABC, abstractmethod
from collections import defaultdict
from ..pb.bookstore.order_pb2 import Timestamp

def max_timestamp(t1: Timestamp, t2: Timestamp):
    """Returns a new Timestamp combining the values of t1 and t2 using max."""
    result = Timestamp()
    for process in Timestamp.DESCRIPTOR.fields:
        setattr(result, process.name, max(getattr(t1, process.name), getattr(t2, process.name)))
    return result


def is_timestamp_leq(t1: Timestamp, t2: Timestamp) -> bool:
    """Returns True if t1 <= t2, False otherwise."""
    for process in Timestamp.DESCRIPTOR.fields:
        if getattr(t1, process.name) > getattr(t2, process.name):
            return False
    return True


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

    def is_timestamp_valid(self, order_id: str, timestamp: Timestamp) -> bool:
        """Checks if the local timestamp is lower than the given one, meaning that everything is correct."""
        local_timestamp = self.vector_clocks[order_id]
        if is_timestamp_leq(local_timestamp, timestamp):
            print(f"{order_id}: final timestamp valid - {timestamp_to_str(local_timestamp)} <= {timestamp_to_str(timestamp)}")
            return True
        else:
            print(f"{order_id}: final timestamp invalid - {timestamp_to_str(local_timestamp)} > {timestamp_to_str(timestamp)}")
            return False
