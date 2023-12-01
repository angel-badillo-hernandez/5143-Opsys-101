"""Main program for simulating CPU scheduling.

CPU Scheduling Program
CMPS-5143-101: Advanced Operating Systems
11/21/23
Authors: Angel Badillo and Leslie Cook

Driver program for performing CPU Scheduling Algorithm simulations.
This CLI program expects these command-line arguments (but does provide
default values for all parameters). If any arguments are invalid, they
will be replaced with the default values.
Command-line Args:
    cpu(int, optional): Number of cores. Defaults to `1`.
    io(int, optional): Number of IO devices. Defaults to `1`.
    sched(str, optional): Scheduling algorithm to perform. Defaults to `"FCFS"` Choices are `"FCFS"`, `"RR"`, and `"PB"`.
    timeslice(int, optional): Quantum used in Round Robin. Defaults to `1`.
    delay(float, optional): Amount of `delay` in seconds between each prominent change / each tick. Defaults to `1`.
    input(str, optional): Input data file to be used in the simulation. Defaults to `"data.json"`.

Examples:
    python3.11 main.py

    python3.11 main.py sched=FCFS
    
    python3.11 main.py cpu=1 io=1 sched=FCFS delay=1 input=data.json

    python3.11 main.py cpu=2 io=4 sched=PB delay=0.1 input=data.json

    python3.11 main.py cpu=4 io=4 sched=RR timeslice=10 input=data.json

"""
import sys
import json
import csv
from rich import print
from cpu import cpu_utilization
from pcb import PCB, json2PCBs
from FCFS import first_come_first_serve
from RR import round_robin
from PB import priority_based
from generate_input import parse_commandline_args, generate_file
from time import sleep
from tickcounter import TickCounter
from statistics import mean

scheduling_algorithms: set[str] = {
    "FCFS",
    "RR",
    "PB",
}


def results2json(
    pcbList: list[PCB],
    file_name: str,
    scheduling_algorithm: str,
    time_slice: int,
    num_cores: int,
    num_io_devices: int,
    current_ticks:int,
) -> None:
    """Writes stats of PCBs and final stats to JSON File.

    Writes stats of processes and scheduling algorithm to a JSON file.

    Args:
        pcbList: `list` of `PCB`s.
        file_name: name of input file.
        scheduling_algorithm: name of the scheduling algorithm.
        num_cores: number of cores the CPU has.
        num_io_devices: number of I/O devices.
    """
    jsonData: dict = {
        "kwargs": {
            "input": file_name,
            "sched": scheduling_algorithm,
            "cpu": num_cores,
            "io": num_io_devices,
            "timeslice": time_slice
        },
        "overall_stats": {
            "total_time": current_ticks,
            "cpu_utilization": cpu_utilization(pcbList, current_ticks),
            "average_arrival_time": mean([pcb.arrival_time for pcb in pcbList]),
            "average_priority": mean(pcb.priority for pcb in pcbList),
            "average_ready_time":  mean(pcb.ready_time for pcb in pcbList),
            "average_running_time":  mean(pcb.running_time for pcb in pcbList),
            "average_waiting_time":  mean(pcb.wait_time for pcb in pcbList),
            "average_io_time":  mean(pcb.io_time for pcb in pcbList),
        },
        "jobs": []
    }

    
    output_file_name: str = f"{scheduling_algorithm}_timeslice={time_slice}_cpu={num_cores}_io={num_io_devices}_{file_name}"
    jsonData["kwargs"]["timeslice"] = time_slice

    for pcb in pcbList:
        pcbDict:dict = dict(pcb)
        pcbDict.pop("cpu_bursts", None)
        pcbDict.pop("io_bursts", None)
        jsonData["jobs"].append(pcbDict)

    with open(output_file_name, "w") as jsonFile:
        json.dump(jsonData, jsonFile, indent=4)

def results2csv(
    pcbList: list[PCB],
    file_name: str,
    scheduling_algorithm: str,
    time_slice: int,
    num_cores: int,
    num_io_devices: int,
) -> None:
    """Write stats of PCBs to csv file.

    Writes the stats of processes to a csv file.

    Args:
        pcbList: `list` of `PCB`s.
        file_name: name of input file.
        scheduling_algorithm: name of the scheduling algorithm.
        num_cores: number of cores the CPU has.
        num_io_devices: number of I/O devices.

    """
    # Generate output file name
    output_file_name: str = f"{scheduling_algorithm}_timeslice={time_slice}_cpu={num_cores}_io={num_io_devices}_{file_name.removesuffix('.json')}.csv"

    with open(output_file_name, "w") as csvFile:
        # Create list of field names
        field_names: list[str] = list(dict(PCB()).keys())
        field_names.remove("cpu_bursts")
        field_names.remove("io_bursts")

        # Write PCB info to csv file
        writer: csv.DictWriter = csv.DictWriter(
            csvFile, field_names, extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows([dict(pcb) for pcb in pcbList])


if __name__ == "__main__":
    argv: list[str] = sys.argv[1:]
    args, kwargs = parse_commandline_args(argv)
    num_cores: int = 1
    num_io_devices: int = 1
    time_slice: int = 1
    sched_alg: str = "FCFS"
    infile: str = "data.json"
    pcbList: list[PCB] = []
    sleep_delay: float = 1

    # If --help flag is present, print module level doc-string,
    # then exit program.
    if "--help" in args:
        # Print documentation
        help("main")
        sys.exit()

    # Change number of cores if "cpu" kwarg is present
    if "cpu" in kwargs.keys():
        try:
            temp: int = int(kwargs["cpu"])

            if temp < 1:
                raise ValueError()

            num_cores = temp
        except ValueError as e:
            print(
                f"Error: invalid argument '{kwargs['cpu']}'"
                " for 'cpu'. Must be positive, nonzero integer value."
            )

    # Change scheduling algorithm if "sched" kwarg is present
    if "sched" in kwargs.keys():
        try:
            if kwargs["sched"] in scheduling_algorithms:
                sched_alg = kwargs["sched"]
            else:
                raise ValueError()
        except ValueError as e:
            print(
                f"Error: invalid argument '{kwargs['cpu']}'"
                f" for 'sched'. Must be a value in {scheduling_algorithms}."
            )
            sleep(1)

    # Change number of io devices if "io" kwarg is present
    if "io" in kwargs.keys():
        try:
            temp: int = int(kwargs["io"])

            if temp < 1:
                raise ValueError()

            num_io_devices = temp
        except ValueError as e:
            print(
                f"Error: invalid argument '{kwargs['io']}'"
                " for 'io'. Must be positive, nonzero integer value."
            )
            sleep(1)

    # Change time slice if "timeslice" kwarg is present
    if "timeslice" in kwargs.keys():
        try:
            temp: int = int(kwargs["timeslice"])

            if temp < 1:
                raise ValueError("Value is negative or zero.")

            time_slice = temp
        except ValueError as e:
            print(
                f"Error: invalid argument '{kwargs['timeslice']}'"
                " for 'timeslice'. Must be positive, nonzero integer value."
            )
            sleep(1)

    # Change input file if "input" kwarg is present
    if "input" in kwargs.keys():
        try:
            pcbList = json2PCBs(kwargs["input"])
            infile = kwargs["input"]
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            print(
                f"Error: invalid argument '{kwargs['input']}'"
                f" for 'input'. File does not exist, or is wrongly formatted."
            )
            sleep(1)
            pcbList = json2PCBs(infile)
    # If kwarg is not present, attempt to use default file.
    # If file does not exist or wrongly formatted, generate it again.
    else:
        try:
            pcbList = json2PCBs(infile)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            generate_file(ofile=infile)
            pcbList = json2PCBs(infile)

    # Change delay if "delay" kwarg is present
    if "delay" in kwargs.keys():
        try:
            temp: float = float(kwargs["delay"])

            if temp < 0:
                raise ValueError()

            sleep_delay = temp
        except ValueError as e:
            print(
                f"Error: invalid argument '{kwargs['delay']}'"
                " for 'delay'. Must be positive, floating-point value."
            )
            sleep(1)

    # Then we perform the algorithm here
    if sched_alg == "FCFS":
        first_come_first_serve(
            pcbList=pcbList,
            num_cores=num_cores,
            io_devices=num_io_devices,
            sleep_delay=sleep_delay,
        )
    elif sched_alg == "RR":
        round_robin(
            pcbList=pcbList,
            num_cores=num_cores,
            io_devices=num_io_devices,
            time_slice=time_slice,
            sleep_delay=sleep_delay,
        )
    else:
        priority_based(
            pcbList=pcbList,
            num_cores=num_cores,
            io_devices=num_io_devices,
            sleep_delay=sleep_delay,
        )

    # Write results to output file
    results2csv(pcbList, infile, sched_alg, time_slice, num_cores, num_io_devices)
    results2json(pcbList, infile, sched_alg, time_slice, num_cores, num_io_devices, TickCounter.get_ticks())
