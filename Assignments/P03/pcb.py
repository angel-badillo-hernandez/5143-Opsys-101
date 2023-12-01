"""`pcb` contains the class `PCB` (Process Control Block) and a function `json2PCBS`.

`PCB` represents a "Process Control Block", a data structure in Operating Systems.
It will be used for "process scheduling". `json2PCBS` is a function that reads data from
a json file, and returns `list[PCB]`.

Typical usage example:

  pcb:PCB = PCB()
  pcbList:list[PCB] = json2PCB("example.json")
"""
import json


class PCB:
    """A class for representing a "Process Control Block"

    The `PCB` class represents a "Process Control Block".
    Contains attributes such as time of arrival, id, cpu bursts, etc.
    Also contains methods for converting other data formats to and from a `PCB`.
    For example, `PCB.to_JSON`, `PCB.from_json`, and `PCB.from_dict`.

    Attributes:
        arrival_time    (int): the process's time of arrival
        process_id      (int): the process's id
        priority        (int): the process's priority
        cpu_bursts      (list[int]): the process's "cpu bursts"
        io_bursts       (list[int]): the process's "io bursts"
        turnaround_time (int): the process's turnaround time
        ready_time      (int): the process's ready time
        wait_time       (int): the process's wait time
        exit_time       (int): the process's exit time

    """

    def __init__(
        self,
        arrival_time: int = 0,
        process_id: int = 0,
        priority: int = 0,
        cpu_bursts: list[int] = [],
        io_bursts: list[int] = [],
        turnaround_time: int = 0,
        ready_time: int = 0,
        running_time:int = 0,
        io_time:int = 0,
        wait_time: int = 0,
        exit_time: int = 0,
    ) -> None:
        """__init__ method for `PCB`

        Constructs a new `PCB` object.

        Args:
            arrival_time(optional): `int` representing process arrival time.
            process_id(optional): `int` representing process id.
            priority(optional): `int` representing process priority.
            cpu_bursts(optional): `list[int]` representing process CPU burst times.
            io_bursts(optional): `list[int]` representing process IO burst times.
            turnaround_time(optional): `int` representing process turnaround time.
            wait_time(optional): `int` representing process wait time.
            exit_time(optional): `int` representing process exit time.

        """
        self.arrival_time = arrival_time
        self.process_id = process_id
        self.priority = priority
        self.cpu_bursts: list[int] = cpu_bursts
        self.io_bursts: list[int] = io_bursts
        self.turnaround_time: int = turnaround_time
        self.ready_time: int = ready_time
        self.running_time:int = running_time
        self.wait_time: int = wait_time
        self.io_time:int = io_time
        self.exit_time: int = exit_time

    def __iter__(self) -> tuple:
        """Enables iteration over attributes and representation as other iterables.

        Enables "casting" PCB as iterables such as `list`, `tuple`, `dict`, etc.

        Yields:
            (str,Any): essentially key-value pair consisting of attribute name and associated value. E.g, ("arrival_time", self.arrival_time)

        Examples:

            >>> pcb = PCB()
            >>> print([key for key in dict(pcb).keys()])
            ['arrival_time', 'process_id', 'priority', 'cpu_bursts', 'io_bursts', 'turnaround_time', 'ready_time', 'wait_time', 'exit_time']

        """
        yield "arrival_time", self.arrival_time
        yield "process_id", self.process_id
        yield "priority", self.priority
        yield "cpu_bursts", self.cpu_bursts
        yield "io_bursts", self.io_bursts
        yield "turnaround_time", self.turnaround_time
        yield "ready_time", self.ready_time
        yield "running_time", self.running_time
        yield "wait_time", self.wait_time
        yield "io_time", self.io_time
        yield "exit_time", self.exit_time

    def __repr__(self) -> str:
        """Provides `str` representation of a `PCB` object.

        Enables constructing a `PCB` object as a `str` representation with the `eval` function.

        Returns:
            str: A string representing a `PCB` object.

        Examples:

            >>> pcbStr = 'PCB()'
            >>> print(type(eval(pcbStr)) is PCB)
            True

        """

        return (
            f"PCB(arrival_time= {self.arrival_time}, process_id= {self.process_id}, "
            f"priority= {self.priority}, cpu_bursts= {self.cpu_bursts}, io_bursts= {self.io_bursts}, "
            f"turnaround_time= {self.turnaround_time}, ready_time= {self.ready_time}, "
            f"running_time= {self.running_time}, wait_time= {self.wait_time}, io_time= {self.io_time}, exit_time= {self.exit_time})"
        )

    def __str__(self) -> str:
        """Provides `str` representation of a `PCB` object.

        Provides a human readable representation of a `PCB` object`.
        Same as `__repr__`.

        Returns:
            str: A string representing a `PCB` object.

        Examples:

            >>> pcb = PCB()
            >>> print(pcb)
            PCB(arrival_time= 0, process_id= 0, priority= 0, cpu_bursts= [], io_bursts= [], turnaround_time= 0, ready_time= 0, running_time= 0, wait_time= 0, io_time= 0, exit_time= 0)


        """
        return repr(self)

    def from_dict(self, dictionary: dict) -> None:
        """Assigns data from proper-formatted `dict` to `PCB` object.

        Assigns values to the attributes in the `PCB` instance using
        key-value pairs in `dictionary`.

        Args:
            dictionary: `dict` with key-value pairs corresponding to `PCB` attributes.

        Example:
            >>> pcb = PCB()
            >>> pcb.from_dict({"arrival_time": 0, "process_id": 0, "priority": 0, "cpu_bursts": [], "io_bursts": []})
            >>> print(pcb.process_id)
            0

        """
        for key, value in dictionary.items():
            setattr(self, key, value)

    def from_json(self, json_str: str) -> None:
        """Assigns data from JSON-formatted `str` to `PCB` object.

        Assigns values to the attributes in the `PCB` instance using a
        JSON-formatted `str`.

        Args:
            json_str: a JSON-formatted `str` with key-value pairs corresponding to `PCB` attributes.

        Example:
            >>> pcb = PCB()
            >>> pcb.from_json('{"arrival_time": 0, "process_id": 0, "priority": 0, "cpu_bursts": [], "io_bursts": []}')
            >>> print(pcb.process_id)
            0

        """
        json_data: dict = json.loads(json_str)

        for key, value in json_data.items():
            setattr(self, key, value)

    def to_json(self) -> str:
        """Returns a JSON-formatted `str` representation of the `PCB` object.

        Returns:
            str: a JSON object with key-value pairs corresponding to `PCB` attributes.

        Example:
            >>> pcb = PCB()
            >>> print(pcb.to_json())
            {"arrival_time": 0, "process_id": 0, "priority": 0, "cpu_bursts": [], "io_bursts": [], "turnaround_time": 0, "ready_time": 0, "running_time": 0, "wait_time": 0, "io_time": 0, "exit_time": 0}

        """
        return json.dumps(dict(self))


def json2PCBs(file_path: str) -> list[PCB]:
    """Reads JSON-file with `PCB` objects and returns `list[PCB]`

    Reads the specified JSON file and returns the `list` of `PCB`s.
    stored in the file.

    Args:
        file_name: `str` containing the JSON file path.

    Returns:
        list[PCB]: `list` of `PCB`s within the JSON file.

    """
    pcbList: list[PCB] = []

    with open(file_path, "r") as jsonFile:
        jsonData: list[dict] = json.load(jsonFile).get("jobs", [])
        pcbList: list[PCB] = list(map(lambda data: PCB(**data), jsonData))

    return pcbList


if __name__ == "__main__":
    help("pcb")
