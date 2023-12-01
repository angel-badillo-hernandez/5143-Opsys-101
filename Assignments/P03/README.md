## CMPS 5143-101

## P03 - CPU Scheduling

### Group Members

#### [Angel Badillo](https://github.com/It-Is-Legend27)

#### [Leslie Cook](https://github.com/Leslie-N-Cook)

### Overview:

This project involves simulating CPU scheduling with a focus on implementing various scheduling algorithms such as First-Come-First-Serve (FCFS), Round-Robin (RR), and Priority-Based (PB). The simulation involves representing processes in different states, including New, Ready, Running, Waiting, IO, and Terminated. The system includes CPUs and IO devices, with the number of resources affecting the turnaround times, waiting times, and ready times. The input files generated represent different process loads, and the program's visual presentation displays the state of each queue in the CPU and relevant messages. Users can specify scheduling algorithm, time slices, CPUs, IO devices, and the input file from the command line. The simulation outputs detailed messages during its run and provides comprehensive statistics at the end, including CPU utilization, average turn-around time, average ready wait time, and average I/O wait time. Furthermore, it generates 2 output files, one is in the format of a CSV file, showing the stats of each process. The second file is a JSON file, which shows the keyword arguments specified by the user, the overall stats of the simulation, and the individual stats of each process.

### Files

| # | File                                        | Description                                                               |
| :-: | ------------------------------------------- | ------------------------------------------------------------------------- |
| 1 | [main.py](main.py)                             | Main script for running the simulation through the command line.          |
| 2 | [scheduling_visuals.py](scheduling_visuals.py) | Utility functions for creating the visualization.                         |
| 3 | [pcb.py](pcb.py)                               | Contains `PCB` class and `json2PCBs` function.                        |
| 4 | [cpu.py](cpu.py)                               | Contains `CPU` class and `cpu_utlization` function.                   |
| 5 | [tickcounter.py](tickcounter.py)               | Contains "global" tick counter,`TickCounter` class.                     |
| 6 | [generate_input.py](generate_input.py)         | Contains `generate_file` function for generating input data.            |
| 7 | [FCFS.py](FCFS.py)                             | Contains `first_come_first_serve` function for running FCFS simulation. |
| 8 | [PB.py](PB.py)                                 | Contains `priority_based` function for running PB simulation.           |
| 9 | [RR.py](RR.py)                                 | Contains `round_robin` function for running RR simulation.              |
| 10 | [cpu_int.json](cpu_int.json)                   | Input data for CPU intensive run.                                         |
| 11 | [io_int.json](io_int.json)                     | Input data for I/O intensive run.                                         |
| 12 | [prio_high.json](prio_high.json)               | Input data for high weighted high priority run.                           |
| 13 | [requirements.txt](requirements.txt)           | Required packages to be installed.                                        |
| 14 | [vis.py](vis.py)                               | For creating graphs.                                                      |

### Instructions

- Install the required packages.

  ```console
  pip install -r requirements.txt
  ```
- Execute `main.py` through the command line, and specify these command-line arguments:

  ```
  cpu(int, optional): Number of cores. Defaults to 1.
  io(int, optional): Number of IO devices. Defaults to 1.
  sched(str, optional): Scheduling algorithm to perform. Defaults to "FCFS" Choices are "FCFS", "RR", and "PB".
  timeslice(int, optional): Quantum used in Round Robin. Defaults to 1.
  delay(float, optional): Amount of `delay` in seconds between each prominent change / each tick. Defaults to 1.
  input(str, optional): Input data file to be used in the simulation. Defaults to "data.json".
  ```
- Example Commands:

  ```console
  python3.11 main.py cpu=<int> io=<int> sched=<Scheduling algorithm acronym> timeslice=<int> delay=<float> input=<JSON file name>
  ```
  ```console
  python3.11 main.py
  ```
  ```console
  python3.11 main.py sched=FCFS
  ```
  ```console
  python3.11 main.py cpu=1 io=1 sched=FCFS delay=1 input=data.json
  ```
  ```console
  python3.11 main.py cpu=2 io=4 sched=PB delay=0.1 input=data.json
  ```
  ```console
  python3.11 main.py cpu=4 io=4 sched=RR timeslice=10 input=data.json
  ```
