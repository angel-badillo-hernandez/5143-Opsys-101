"""Provides a utility function for simulating RR (Round Robin) CPU Scheduling Algorithm.

Given a `list` of `PCB`s, `round_robin` will perform the RR CPU Scheduling Algorithm,
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


def round_robin(
    pcbList: list[PCB],
    num_cores: int = 1,
    io_devices: int = 1,
    sleep_delay: float = 1,
    time_slice: int = 1,
) -> None:
    """Performs the Round Robin (RR) algorithm on a `list` of `PCB` objects.

    Performs RR algorithm on `pcbList`, then shows a visualization of the results.

    Args:
        pcbList: a `list` of `PCB` objects.
        num_cores (optional): `int` representing number of cores in CPU.
        io_devices (optional): `int` representing number of I/O devices.
        sleep_delay (optional): `int` controlling how fast the visualization occurs.
    """
    # Countdowns for timeslice for each process that is in running
    # resets each time timeslice is up
    countdown_timers: dict[int, int] = {pcb.process_id: time_slice for pcb in pcbList}

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
            scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
            current_ticks=TickCounter.get_ticks(),
        ),
    ) as visual:
        # Keep looping until all processes are terminated
        while len(cpu.terminated) != len(pcbList):
            # Load stuff into "ready" as it arrives
            while len(cpu.new) and TickCounter().get_ticks() >= cpu.new[0].arrival_time:
                cpu.ready.append(cpu.new.popleft())  # Move next PCB into ready queue

                # Show visualization of process being moved into ready queue
                visual.update(
                    cpu_scheduling_visualization(
                        pcbList=pcbList,
                        cpu=cpu,
                        scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
                        current_ticks=TickCounter.get_ticks(),
                        message=Text(
                            f"Process {cpu.ready[-1].process_id} has arrived at time"
                            f" {TickCounter.get_ticks()}\n",
                            style="bold yellow",
                        ),
                    ),
                )
                sleep(sleep_delay)

            # Load stuff from ready to running if there's available space, and if there is a PCB in ready
            while len(cpu.running) < cpu.num_cores and len(cpu.ready):
                cpu.running.append(
                    cpu.ready.popleft()
                )  # Move next PCB into running queue

                # Show visualization of process being moved into running queue
                visual.update(
                    cpu_scheduling_visualization(
                        pcbList=pcbList,
                        cpu=cpu,
                        scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
                        current_ticks=TickCounter.get_ticks(),
                        message=Text(
                            f"Process {cpu.running[-1].process_id} is running at time"
                            f" {TickCounter.get_ticks()}\n",
                            style="bold green",
                        ),
                    ),
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
                        # If decrement from cpu burst and countdown timer does not result in 0, decrement
                        if cpu.running[run_idx].cpu_bursts[0] - 1 and countdown_timers[cpu.running[run_idx].process_id] - 1:
                            cpu.running[run_idx].cpu_bursts[0] -= 1
                            countdown_timers[cpu.running[run_idx].process_id] -= 1
                        # Else, pop cpu burst from list and move PCB to waiting queue
                        elif not cpu.running[run_idx].cpu_bursts[0] - 1:
                            # Reset countdown timer
                            countdown_timers[cpu.running[run_idx].process_id] = time_slice

                            # Pop current cpu burst
                            cpu.running[run_idx].cpu_bursts.pop(0)
                            cpu.waiting.append(
                                cpu.running.pop(run_idx)
                            )  # Move next PCB waiting queue
                            run_idx -= 1

                            # Show visualization of process being moved into waiting queue
                            visual.update(
                                cpu_scheduling_visualization(
                                    pcbList=pcbList,
                                    cpu=cpu,
                                    scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
                                    current_ticks=TickCounter.get_ticks(),
                                    message=Text(
                                        f"Process {cpu.waiting[-1].process_id} is waiting at time"
                                        f" {TickCounter.get_ticks()}\n",
                                        style="bold blue",
                                    ),
                                ),
                            )
                            sleep(sleep_delay)
                        # If decrement from countdown timer results in 0, decrement cpu burst and move to ready queue
                        else:
                            cpu.running[run_idx].cpu_bursts[0] -= 1
                            # Reset countdown timer
                            countdown_timers[cpu.running[run_idx].process_id] = time_slice

                            cpu.ready.append(
                                cpu.running.pop(run_idx)
                            )  # Move next PCB into ready queue
                            run_idx -= 1

                            # Show visualization of process being moved into ready queue
                            visual.update(
                                cpu_scheduling_visualization(
                                    pcbList=pcbList,
                                    cpu=cpu,
                                    scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
                                    current_ticks=TickCounter.get_ticks(),
                                    message=Text(
                                        f"Process {cpu.ready[-1].process_id} is ready at time"
                                        f" {TickCounter.get_ticks()}\n",
                                        style="bold blue",
                                    ),
                                ),
                            )
                            sleep(sleep_delay)
                        
                    # NOTE: This else might be redundant
                    else:
                        cpu.waiting.append(cpu.running.pop(run_idx))
                        run_idx -= 1
                        # Show visualization of process being moved into waiting queue
                        visual.update(
                            cpu_scheduling_visualization(
                                pcbList=pcbList,
                                cpu=cpu,
                                scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
                                current_ticks=TickCounter.get_ticks(),
                                message=Text(
                                    f"Process {cpu.waiting[-1].process_id} is waiting at time"
                                    f" {TickCounter.get_ticks()}\n",
                                    style="bold blue",
                                ),
                            ),
                        )
                        sleep(sleep_delay)
                    run_idx += 1

            # Move PCB from waiting to io if there's available space, and if there is a PCB in waiting
            while len(cpu.io) < io_devices and len(cpu.waiting):
                cpu.io.append(cpu.waiting.popleft())  # Move next PCB into io queue

                # Show visualization of process being moved into io queue
                visual.update(
                    cpu_scheduling_visualization(
                        pcbList=pcbList,
                        cpu=cpu,
                        scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
                        current_ticks=TickCounter.get_ticks(),
                        message=Text(
                            f"Process {cpu.io[-1].process_id} is doing I/O at time"
                            f" {TickCounter.get_ticks()}\n",
                            style="bold purple",
                        ),
                    ),
                )
                sleep(sleep_delay)

            # Increment ready time
            for ready_idx in range(0, len(cpu.ready)):
                cpu.ready[ready_idx].ready_time += 1

            # Increment wait time
            for wait_idx in range(0, len(cpu.waiting)):
                cpu.waiting[wait_idx].wait_time += 1

            # Show visualization of process after tick
            visual.update(
                cpu_scheduling_visualization(
                    pcbList=pcbList,
                    cpu=cpu,
                    scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
                    current_ticks=TickCounter.get_ticks(),
                ),
            )
            sleep(sleep_delay)

            # Reduce IO burst times for all process in IO state
            if len(cpu.io):
                io_idx: int = 0

                while io_idx < len(cpu.io):
                    # If IO bursts is not empty
                    if len(cpu.io[io_idx].io_bursts):
                        # Increment IO time
                        cpu.io[io_idx].io_time += 1
                        # If decrement does not result in 0, decrement
                        if cpu.io[io_idx].io_bursts[0] - 1 > 0:
                            cpu.io[io_idx].io_bursts[0] -= 1
                        # Else, pop IO burst from list and move PCB to ready queue, if has more cpu bursts
                        elif len(cpu.io[io_idx].cpu_bursts) and len(
                            cpu.io[io_idx].io_bursts
                        ):
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
                                    scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
                                    current_ticks=TickCounter.get_ticks(),
                                    message=Text(
                                        f"Process {cpu.ready[-1].process_id} is ready at time"
                                        f" {TickCounter.get_ticks()}\n",
                                        style="bold yellow",
                                    ),
                                ),
                            )
                            sleep(sleep_delay)
                        # If CPU bursts is empty, move to terminated
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
                                    scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
                                    current_ticks=TickCounter.get_ticks() + 1,
                                    message=Text(
                                        f"Process {cpu.terminated[-1].process_id} has terminated at time"
                                        f" {TickCounter.get_ticks()+1}\n",
                                        style="bold red",
                                    ),
                                ),
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
                                scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
                                current_ticks=TickCounter.get_ticks() + 1,
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
                scheduling_algorithm_title=f"Round Robin\nTime Slice: {time_slice}",
                current_ticks=TickCounter.get_ticks(),
            ),
        )
        sleep(sleep_delay)


if __name__ == "__main__":
    help("RR")
