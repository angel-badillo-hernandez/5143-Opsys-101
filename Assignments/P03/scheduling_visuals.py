"""Utility functions for visualization in CPU Scheduling Algorithms.

`processes_table` returns a `Table` showing all the information for a list
of processes. `queues_table` returns a `Table` showing all the processes in each
state. `cpu_scheduling_visualization` shows the entire visualization for the
simulation.

"""
from rich.table import Table, Column
from rich import box
from rich.style import Style
from rich.color import Color
from rich.panel import Panel
from rich.live import Live
from rich.padding import Padding
from rich.align import Align
from rich.layout import Layout
from rich.columns import Columns
from rich.text import Text
from statistics import mean
from pcb import PCB
from cpu import CPU, cpu_utilization


def cpu_scheduling_visualization(
    pcbList: list[PCB],
    cpu: CPU,
    current_ticks: int,
    message: Text | str | None = None,
    scheduling_algorithm_title: str = "Scheduling Algorithm",
    processes_table_title: str = "Processes",
    queues_table_title: str = "Process States",
    stats_table_title: str = "Stats",
    show_priority: bool = False,
) -> Table:
    """Returns a `Table` object that is a visual representation of a CPU scheduling algorithm.

    Creates a `Table` object that is a visual representation of a CPU scheduling algorithm.

    Args:
        pcbList: a `list` of `PCB` objects.
        cpu: a `CPU` object.
        scheduling_algorithm_title (optional): title for the scheduling algorithm. Defaults to "Scheduling Algorithm".
        processes_table_title (optional): title for `Panel` that contains processes table. Defaults to "Processes".
        queues_table_title (optional): title for `Panel` that contains queues table. Defaults to "Process States".
        stats_table_title (optional): title for the `Panel` that contains stats table. Defaults to "Stats".
        show_priority (optional): a `bool` to toggle priorities in the table. Defaults to `False`.
        current_ticks (optional): an `int` to show the current ticks in the simulation. Defaults to `None`.
    Returns:
        Table: a renderable for representing the visualization of CPU scheduling.

    """
    # Table for current ticks, CPU utilization, and messages.
    text_table = Table(box=box.HORIZONTALS, expand=True, show_header=False, width=50, show_edge=False)
    text_table.add_row(f"Ticks: {current_ticks}", style="bold red italic")
    text_table.add_row(
        f"CPU Utilization: {cpu_utilization(pcbList, current_ticks)*100.0 : .4f}%",
        style="bold green",
    )
    text_table.add_section()

    if message:
        text_table.add_row(message)
    else:
        text_table.add_row("")

    complete_table: Table = Table(
        box=None,
        expand=True,
        show_header=False,
        title=scheduling_algorithm_title,
        title_style="yellow bold",
        highlight=True,
    )

    complete_table.add_row(
        Panel(
            processes_table(
                pcbList,
                None,
                show_priority,
            ),
            title=processes_table_title,
            expand=True,
        ),
    )

    complete_table.add_row(
        Panel(
            Columns(
                [
                    text_table,
                    queues_table(
                        cpu,
                        None,
                    ),
                ],
                equal=True,
            ),
            title=queues_table_title,
        )
    )
    return Layout(complete_table)


def processes_table(
    pcbList: list[PCB],
    title: str = "Processes",
    show_priority: bool = False,
) -> Table:
    """Returns a table showing the information of processes in a CPU scheduling algorithm.

    Creates a table showing the information of a list of PCBs.

    Args:
        pcbList: a `list` of `PCB` objects.
        title (optional): title of the table. Defaults to "Processes".
        show_priority (optional): a `bool` to toggle priorities in the table. Defaults to `False`.
        current_ticks (optional): an `int` to show the current ticks in the simulation. Defaults to `None`.
    Returns:
        Table: a table containing the data from a list of PCBs.

    """

    table: Table = Table(
        title=title,
        expand=True,
    )

    table.add_column("Process ID", style="cyan")
    # Add column for priority if show_priority is True
    if show_priority:
        table.add_column("Priority", style="red")
    table.add_column("Arrival Time", style="yellow")
    table.add_column(
        "Ready Time",
        style=Style(color=Color.from_rgb(255, 165, 0), bold=True),  # Orange
    )
    table.add_column("Running Time", style="bold green")
    table.add_column("Waiting Time", style="bold blue")
    table.add_column("IO Time", style="magenta")
    table.add_column(
        "Turnaround Time",
        style=Style(color=Color.from_rgb(192, 255, 0), bold=True),  # Lime
    )
    table.add_column("Exit Time", style="bold red")
    table.add_column("CPU Bursts", style="green")
    table.add_column("IO Bursts", style="magenta")
    for pcb in pcbList:
        # Add priority value to row if show_priority is True
        if show_priority:
            table.add_row(
                str(pcb.process_id),
                str(pcb.priority),
                str(pcb.arrival_time),
                str(pcb.ready_time),
                str(pcb.running_time),
                str(pcb.wait_time),
                str(pcb.io_time),
                str(pcb.turnaround_time),
                str(pcb.exit_time),
                str(pcb.cpu_bursts),
                str(pcb.io_bursts),
            )
        else:
            table.add_row(
                str(pcb.process_id),
                str(pcb.arrival_time),
                str(pcb.ready_time),
                str(pcb.running_time),
                str(pcb.wait_time),
                str(pcb.io_time),
                str(pcb.turnaround_time),
                str(pcb.exit_time),
                str(pcb.cpu_bursts),
                str(pcb.io_bursts),
            )

    # Add row for averages
    table.add_section()

    # If show_priority is True, add average priority to row
    if show_priority:
        table.add_row(
            "Averages:",
            f"{mean([pcb.priority for pcb in pcbList]): .4f}",
            f"{mean([pcb.arrival_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.ready_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.running_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.wait_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.io_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.turnaround_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.exit_time for pcb in pcbList]): .4f}",
            Text(style=Style(bgcolor="white")),
            Text(style=Style(bgcolor="white")),
            style=Style(
                color=Color.from_rgb(255, 127, 127),
                bold=True,
                italic=True,
            ),  # Light red
        )
    else:
        table.add_row(
            "Averages:",
            f"{mean([pcb.arrival_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.ready_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.running_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.wait_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.io_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.turnaround_time for pcb in pcbList]): .4f}",
            f"{mean([pcb.exit_time for pcb in pcbList]): .4f}",
            Text(style=Style(bgcolor="white")),
            Text(style=Style(bgcolor="white")),
            style=Style(
                color=Color.from_rgb(255, 127, 127),
                bold=True,
                italic=True,
            ),  # Light red
        )
    return table


def queues_table(
    cpu: CPU,
    title: str = "Process States",
) -> Table:
    """Returns a table showing states of processes in a CPU scheduling algorithm.

    Creates a table showing that states of PCBs in a CPU.

    Args:
        cpu: a `CPU` containing various queues that have processes in different states.
        title (optional): the title of the table. Defaults to "Process States".
        current_ticks (optional): an `int` to show the current ticks in the algorithm. Defaults to `None`.
    Returns:
        Table: a table representing different process in their current state in CPU scheduling.

    """
    table: Table = Table(
        title=title,
        box=box.HORIZONTALS,
        show_header=False,
        expand=True,
    )

    # Creates lists of Process IDs for each queue
    new_processes: list[int] = [i.process_id for i in cpu.new]
    ready_processes: list[int] = [i.process_id for i in cpu.ready]
    running_processes: list[int] = [i.process_id for i in cpu.running]
    waiting_processes: list[int] = [i.process_id for i in cpu.waiting]
    io_processes: list[int] = [i.process_id for i in cpu.io]
    terminated_processes: list[int] = [i.process_id for i in cpu.terminated]

    # Add info to rows
    table.add_row("New", str(new_processes), style="cyan", end_section=True)
    table.add_row("Ready", str(ready_processes), style="yellow", end_section=True)
    table.add_row("Running", str(running_processes), style="green", end_section=True)
    table.add_row("Waiting", str(waiting_processes), style="blue", end_section=True)
    table.add_row("IO", str(io_processes), style="purple", end_section=True)
    table.add_row(
        "Terminated", str(terminated_processes), style="red", end_section=True
    )
    return table


if __name__ == "__main__":
    help("scheduling_visuals")