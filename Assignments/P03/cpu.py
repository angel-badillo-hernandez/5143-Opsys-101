"""`cpu` contains the class `CPU` (Central Processing Unit).

`CPU` represents a single or multicore processor.

"""
from pcb import PCB
from collections import deque
from statistics import mean


class CPU:
    """A class for representing a single or multicore processor.

    The `CPU` class represents a "Central Processing Unit".
    Contains attributes such as `.

    Attributes:
        num_cores  (int): the number of cores the CPU has
        io_devices (int): the number of I/O devices
        new        (deque[PCB]): queue for holding processes in the "new" state
        ready      (deque[PCB]): queue for holding processes in the "ready" state
        running    (list[PCB]): `list` for holding processes in the "running" state
        waiting    (deque[PCB]): queue for holding processes in the "waiting" state
        io         (list[PCB]): `list` for holding processes in the "io" state
        terminated (deque[PCB]): queue for holding processes in the "teriminated state

    """

    def __init__(self, num_cores: int = 1, io_devices: int = 1) -> None:
        """__init__ method for `CPU`

        Constructs a new `CPU` object.

        Args:
            num_cores(optional): `int` representing number of cores.
            io_devices(optional): `int` representing number of I/O devices.

        """
        self.num_cores: int = num_cores
        self.io_devices: int = io_devices

        self.new: deque[PCB] = deque()
        self.ready: deque[PCB] = deque()
        self.running: list[PCB] = []
        self.waiting: deque[PCB] = deque()
        self.io: list[PCB] = []
        self.terminated: deque[PCB] = deque()


def cpu_utilization(pcbList: list[PCB], current_ticks: int) -> float:
    """Calculates CPU Utilization.

    Calculates CPU utilization using the formula `U = 1 - p^n`,
    where `p` is the probability of a process waiting for I/O, and `n`
    is the number of processes.

    Args:
        pcbList: `list` of `PCB`s.
        current_ticks: current ticks in simulation.
    Returns:
        float: CPU Utilization.
        
    """
    average_wait_time: int = mean([pcb.wait_time for pcb in pcbList])
    total_time: int = current_ticks

    n: int = len(pcbList)
    # Calculate probability of a process waiting for I/O
    p: float = average_wait_time / total_time if total_time else 0.0
    # Calculate CPU utlization
    utilization: float = 1.0 - p**n
    return utilization


if __name__ == "__main__":
    help("cpu")
