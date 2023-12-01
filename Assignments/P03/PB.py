"""Provides a utility function for simulating PB (Priority-Based) CPU Scheduling Algorithm.

Given a `list` of `PCB`s, `priority_based` will perform the PB CPU Scheduling Algorithm,
while providing a visualization.

"""
from pcb import PCB, json2PCBs
from cpu import CPU
from tickcounter import TickCounter
from scheduling_visuals import cpu_scheduling_visualization
from time import sleep
from rich.text import Text
from rich.live import Live
from rich.style import Style
from rich.layout import Layout
from collections import deque


def priority_based(
    pcbList: list[PCB],
    num_cores: int = 1,
    io_devices: int = 1,
    sleep_delay: float = 1,
) -> None:
    """Performs the Priority-Based (PB) algorithm on a `list` of `PCB` objects.

    Performs PB algorithm on `pcbList`, then shows a visualization of the results.

    Args:
        pcbList: a `list` of `PCB` objects.
        num_cores (optional): `int` representing number of cores in CPU.
        io_devices (optional): `int` representing number of I/O devices.
        sleep_delay (optional): `int` controlling how fast the visualization occurs.
    """
    # Clear ticks
    TickCounter.reset_ticks()

    # Create instance of CPU that has `numCores` number of cores.
    cpu: CPU = CPU(num_cores, io_devices)

    # Sort processes by arrival time, and put into "new" queue
    cpu.new.extend(sorted(pcbList, key=lambda x: x.arrival_time))

    with Live(
        cpu_scheduling_visualization(
            pcbList=pcbList,
            cpu=cpu,
            scheduling_algorithm_title="Priority-Based",
            current_ticks=TickCounter.get_ticks(),
            show_priority=True,
        ),
    ) as visual:
        # Keep looping until all processes are terminated
        while len(cpu.terminated) != len(pcbList):
            # Load stuff into "ready" as it arrives
            while len(cpu.new) and TickCounter().get_ticks() >= cpu.new[0].arrival_time:
                cpu.ready.append(cpu.new.popleft())  # Move next PCB into ready queue

                # Sort ready queue by descending priority, so leftmost has highest
                cpu.ready = deque(
                    sorted(cpu.ready, key=lambda x: x.priority, reverse=True)
                )

                # Show visualization of process being moved into ready queue
                visual.update(
                    cpu_scheduling_visualization(
                        pcbList=pcbList,
                        cpu=cpu,
                        scheduling_algorithm_title="Priority-Based",
                        current_ticks=TickCounter.get_ticks(),
                        show_priority=True,
                        message=Text(
                            f"Process {cpu.ready[-1].process_id} has arrived at time"
                            f" {cpu.ready[-1].arrival_time}\n",
                            style="bold yellow",
                        ),
                    )
                )
                sleep(sleep_delay)

            # Load stuff from ready to running if there's available space, and if there is a PCB in ready.
            # Switch lowest priority PCB with incoming PCB, if applicable.
            while True:
                # Swap low priority running process with high priority ready process
                if (
                    len(cpu.running)
                    and len(cpu.ready)
                    and cpu.ready[0].priority > cpu.running[-1].priority
                ):
                    # Swap low priority PCB in "running" with next high priority PCB in "ready"
                    low_priority_pcb: PCB = cpu.running[-1]
                    cpu.running[-1] = cpu.ready[0]
                    cpu.ready.popleft()
                    cpu.ready.append(low_priority_pcb)
                    # Sort ready queue by descending priority, so leftmost has highest
                    cpu.ready = deque(
                        sorted(cpu.ready, key=lambda x: x.priority, reverse=True)
                    )

                # Move next PCB into running queue, if space available
                elif len(cpu.running) < cpu.num_cores and len(cpu.ready):
                    cpu.running.append(
                        cpu.ready.popleft()
                    )  # Move next PCB into running queue
                # Exit the loop, nothing to swap or move into running queue
                else:
                    break

                # Sort ready queue by descending priority, so leftmost has highest
                cpu.running.sort(key=lambda x: x.priority, reverse=True)

                # Show visualization of process being moved into running queue
                visual.update(
                    cpu_scheduling_visualization(
                        pcbList=pcbList,
                        cpu=cpu,
                        scheduling_algorithm_title="Priority-Based",
                        current_ticks=TickCounter.get_ticks(),
                        show_priority=True,
                        message=Text(
                            f"Process {cpu.running[-1].process_id} is running at time"
                            f" {TickCounter.get_ticks()}\n",
                            style="bold green",
                        ),
                    )
                )
                sleep(sleep_delay)

            # Increment ticks
            TickCounter.increment_ticks()

            # Reduce CPU burst times for all process in running state
            if len(cpu.running):
                run_idx: int = 0

                while run_idx < len(cpu.running):
                    # If cpu bursts is not empty
                    if cpu.running[run_idx].cpu_bursts:
                        # Increment running time
                        cpu.running[run_idx].running_time += 1
                        # If decrement does not result in 0, decrement
                        if cpu.running[run_idx].cpu_bursts[0] - 1:
                            cpu.running[run_idx].cpu_bursts[0] -= 1
                        # Else, pop cpu burst from list and move PCB to waiting queue, or terminated queue
                        else:
                            # Pop current cpu burst
                            cpu.running[run_idx].cpu_bursts.pop(0)
                            cpu.waiting.append(
                                cpu.running.pop(run_idx)
                            )  # Move next PCB into running queue
                            run_idx -= 1

                            # Show visualization of process being moved into ready queue
                            visual.update(
                                cpu_scheduling_visualization(
                                    pcbList=pcbList,
                                    cpu=cpu,
                                    scheduling_algorithm_title="Priority-Based",
                                    current_ticks=TickCounter.get_ticks(),
                                    show_priority=True,
                                    message=Text(
                                        f"Process {cpu.waiting[-1].process_id} is waiting at time"
                                        f" {TickCounter.get_ticks()}\n",
                                        style="bold blue",
                                    ),
                                )
                            )
                            sleep(sleep_delay)
                    # NOTE: This else might be redundant
                    else:
                        cpu.waiting.append(cpu.running.pop(run_idx))
                        run_idx -= 1
                        # Show visualization of process being moved into ready queue
                        visual.update(
                            cpu_scheduling_visualization(
                                pcbList=pcbList,
                                cpu=cpu,
                                scheduling_algorithm_title="Priority-Based",
                                current_ticks=TickCounter.get_ticks(),
                                show_priority=True,
                                message=Text(
                                    f"Process {cpu.waiting[-1].process_id} is waiting at time"
                                    f" {TickCounter.get_ticks()}\n",
                                    style="bold blue",
                                ),
                            )
                        )
                        sleep(sleep_delay)
                    run_idx += 1

            # Move PCB from waiting to io if there's available space, and if there is a PCB in waiting
            while len(cpu.io) < io_devices and len(cpu.waiting):
                cpu.io.append(cpu.waiting.popleft())  # Move next PCB into running queue

                # Show visualization of process being moved into running queue
                visual.update(
                    cpu_scheduling_visualization(
                        pcbList=pcbList,
                        cpu=cpu,
                        scheduling_algorithm_title="Priority-Based",
                        current_ticks=TickCounter.get_ticks(),
                        show_priority=True,
                        message=Text(
                            f"Process {cpu.io[-1].process_id} is doing I/O at time"
                            f" {TickCounter.get_ticks()}\n",
                            style="bold purple",
                        ),
                    )
                )
                sleep(sleep_delay)

            # Increment ready time and do "aging" (raising priority) to prevent starvation
            for ready_idx in range(0, len(cpu.ready)):
                cpu.ready[ready_idx].ready_time += 1

                # Raise priority of processes by 1 every 10 seconds it is in "ready" state
                if (
                    cpu.ready[ready_idx].ready_time
                    and cpu.ready[ready_idx].ready_time % 10 == 0
                ):
                    cpu.ready[ready_idx].priority += 1

            # Increment wait time
            for wait_idx in range(0, len(cpu.waiting)):
                cpu.waiting[wait_idx].wait_time += 1

            # Show visualization of process after tick
            visual.update(
                cpu_scheduling_visualization(
                    pcbList=pcbList,
                    cpu=cpu,
                    scheduling_algorithm_title="Priority-Based",
                    current_ticks=TickCounter.get_ticks(),
                    show_priority=True,
                )
            )
            sleep(sleep_delay)

            # Reduce IO burst times for all process in IO state
            if len(cpu.io):
                io_idx: int = 0

                while io_idx < len(cpu.io):
                    # If IO bursts is not empty
                    if cpu.io[io_idx].io_bursts:
                        # Increment IO time
                        cpu.io[io_idx].io_time += 1
                        # If decrement does not result in 0, decrement
                        if cpu.io[io_idx].io_bursts[0] - 1:
                            cpu.io[io_idx].io_bursts[0] -= 1
                        # Else, pop IO burst from list and move PCB to ready queue, if has more cpu bursts
                        elif cpu.io[io_idx].cpu_bursts:
                            # Pop current cpu burst
                            cpu.io[io_idx].io_bursts.pop(0)
                            cpu.ready.append(
                                cpu.io.pop(io_idx)
                            )  # Move next PCB into ready queue
                            io_idx -= 1

                            # Show visualization of process being moved into ready queue
                            visual.update(
                                cpu_scheduling_visualization(
                                    pcbList=pcbList,
                                    cpu=cpu,
                                    scheduling_algorithm_title="Priority-Based",
                                    current_ticks=TickCounter.get_ticks(),
                                    show_priority=True,
                                    message=Text(
                                        f"Process {cpu.ready[-1].process_id} is ready at time"
                                        f" {TickCounter.get_ticks()}\n",
                                        style="bold yellow",
                                    ),
                                )
                            )
                            sleep(sleep_delay)
                        # If CPU bursts is empty, move to terminated
                        else:
                            cpu.io[io_idx].exit_time = TickCounter.get_ticks() + 1
                            cpu.io[io_idx].io_bursts.pop(0)
                            cpu.terminated.append(cpu.io.pop(io_idx))
                            io_idx -= 1
                            # Show visualization of process being moved into ready queue
                            visual.update(
                                cpu_scheduling_visualization(
                                    pcbList=pcbList,
                                    cpu=cpu,
                                    scheduling_algorithm_title="Priority-Based",
                                    current_ticks=TickCounter.get_ticks() + 1,
                                    show_priority=True,
                                    message=Text(
                                        f"Process {cpu.terminated[-1].process_id} has terminated at time"
                                        f" {TickCounter.get_ticks()+1}\n",
                                        style="bold red",
                                    ),
                                )
                            )
                            sleep(sleep_delay)
                    else:
                        cpu.io[io_idx].exit_time = TickCounter.get_ticks() + 1
                        cpu.io[io_idx].io_bursts.clear()
                        cpu.terminated.append(cpu.io.pop(io_idx))
                        io_idx -= 1
                        # Show visualization of process being moved into ready queue
                        visual.update(
                            cpu_scheduling_visualization(
                                pcbList=pcbList,
                                cpu=cpu,
                                scheduling_algorithm_title="Priority-Based",
                                current_ticks=TickCounter.get_ticks() + 1,
                                show_priority=True,
                                message=Text(
                                    f"Process {cpu.terminated[-1].process_id} has terminated at time"
                                    f" {TickCounter.get_ticks()+1}\n",
                                    style="bold red",
                                ),
                            ),
                        )
                        sleep(sleep_delay)
                    io_idx += 1
        # Increment ticks counter so it is correct
        TickCounter.increment_ticks()

        # Calculate turnaround times
        for idx in range(0, len(pcbList)):
            pcbList[idx].turnaround_time = (
                pcbList[idx].exit_time - pcbList[idx].arrival_time
            )

        # Show final stats
        visual.update(
            cpu_scheduling_visualization(
                pcbList=pcbList,
                cpu=cpu,
                scheduling_algorithm_title="Priority-Based",
                current_ticks=TickCounter.get_ticks(),
                show_priority=True,
            )
        )
        sleep(sleep_delay)


if __name__ == "__main__":
    help("PB")
