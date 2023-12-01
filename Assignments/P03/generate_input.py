"""Provides utility functions for generating data and parsing command-line arguments.

Provides utility functions `generate_file` and `parse_commandline_args` for generating
randomized data for use in simulating CPU scheduling and for parsing command-line arguments.

Usage: (All params have defaults, but can be changed with the following): 

        nj              : Number of jobs[1 - n]
        minCpuBT        : Min cpu burst length.  Usually single digits: [1 - 9]
        maxCpuBT        : Max cpu burst length. Whatever you want: 
        minIOBT         : Min io burst length. Usually single digits: [1 - 9]
        maxIOBT         : Max io burst length. Whatever you want: 
        minNumBursts    : Min number of bursts [1 - n]
        maxNumBursts    : Max number of bursts [number larger than minNumBursts
        intBurstType    : Generate bursts based on cpu intensive or io intensive 
        minat           : Min jobs per arrival time [1-n]
        maxat           : Max jobs per arrival time [number larger than minat
        minp            : Min priority [1-n]
        maxp            : Max priority 
        prioWeights     : Priority weights 
        ofile           : Outfile Name will write the output to that file.

Example Commands:

        generate_input.py ofile=filename.wut nj=N minCpuBT=N maxCpuBT=N minIOBT=N maxIOBT=N minNumBursts=N 
        maxNumBursts=N minat=N maxat=N minp=N maxp=N prioWeights=
or

        generate_input.py ofile=filename.wut nj=N minCpuBT=N maxCpuBT=N minIOBT=N maxIOBT=N intBurstType= 
        minat=N maxat=N minp=N maxp=N prioWeights=
or

        generate_input.py prioWeights=low intensiveBurstType=cpu ofile=datafile_cpu_intense.json
or

        generate_input.py prioWeights=high intensiveBurstType=io ofile=datafile_io_intense.json
"""
import random
import sys
import json


class WeightedPriorities:
    def __init__(self, choiceType="even"):
        self.priorityChoiceWeights = {
            "low": [35, 25, 18, 15, 7],
            "even": [20, 20, 20, 20, 20],
            "high": [7, 15, 18, 25, 35],
        }
        self.choiceType = choiceType
        self.priorityChoiceList = []
        self.generateWeightedPriority(choiceType)

        self.nextPriority = 0  # index to walk through priorityChoiceList

    def generateWeightedPriority(self, customWeights=None):
        """generate a random priority using a weighted scheme.
        Param:
            choiceType (string):
                even             : random distribution with no bias
                high             : random distribution with bias toward high priorities
                low              :     "                            "   low priorities
            customWeights (list) : list of new weights, one weight per priority (should add to 100 but doesn't have to):
                [5,10,15,20,25,30] = priorities 1-6 with weights:
                    priority 1  5/105 or 0.04%
                    priority 2 10/105 or 0.09%
                    priority 3 15/105 or 0.14%
                    ...
                    priority 6 30/105 or 0.28%
        """

        weights = self.priorityChoiceWeights[self.choiceType]

        for i in range(len(weights)):
            self.priorityChoiceList.extend([i + 1] * weights[i])

        random.shuffle(self.priorityChoiceList)

        # print(self.priorityChoiceList)

    def getNext(self):
        # choose the next priority from front of the list
        p = self.priorityChoiceList[self.nextPriority]

        # increment the index to the next priority
        self.nextPriority = (self.nextPriority + 1) % len(self.priorityChoiceList)
        return p


def parse_commandline_args(argv: list[str]) -> tuple[list[str], dict[str, str]]:
    """
    Processes argv list into plain args and kwargs.
    Just easier than using a library like argparse for small things.
    Example:
        python file.py arg1 arg2 arg3=val1 arg4=val2 -arg5 -arg6 --arg7
        Would create:
            args[arg1, arg2, -arg5, -arg6, --arg7]
            kargs{arg3 : val1, arg4 : val2}

        Params with dashes (flags) can now be processed seperately
    Shortfalls:
        spaces between k=v would result in bad params
    Returns:
        tuple  (args,kargs)
    """
    args: list[str] = []
    kwargs: dict[str, str] = {}

    for arg in argv:
        if "=" in arg:
            key, val = arg.split("=")
            kwargs[key] = val
        else:
            args.append(arg)
    return args, kwargs


def generate_file(
    nj: int | str = 5,
    minCpuBT: int | str = random.randint(5, 10),
    maxCpuBT: int | str | None = None,
    minIOBT: int | str = random.randint(10, 15),
    maxIOBT: int | None = None,
    minNumBursts: int | str = random.randint(5, 8),
    maxNumBursts: int | str | None = None,
    intBurstType: str | list[str] = "normal",
    minat: int | str = 1,
    maxat: int | str | None = None,
    prioWeights: str = "even",
    ofile: str = "data",
) -> None:
    """Generates JSON-formatted data for CPU Scheduling Simulation.

    Generates a JSON file with semi-randomly generated data for processes.

    Args:
        nj (optional): Number of processes. Defaults to 5.
        minCpuBT (optional): Minimum value of a CPU burst time. Defaults to random.randint(5, 10).
        maxCpuBT (optional): Maximum value of a CPU burst time. Defaults to None.
        minIOBT (optional): Minimum value of an IO burst time. Defaults to random.randint(10, 15).
        maxIOBT (optional): Maximum value of an IO burst time. Defaults to None.
        minNumBursts (optional): Minimum number of bursts. IO bursts will always have 1 less than CPU bursts. Defaults to random.randint(5, 8).
        maxNumBursts (optional): Maximum number of bursts. IO bursts will always have 1 less than CPU bursts. Defaults to None.
        intBurstType (optional): Alters generated data to be CPU intensive, IO intensive, or normal. Defaults to "normal".
        minat (optional): Minimum number of process that can arrive at one time. Defaults to 1.
        maxat (optional): Maximum number of processes that can arrivate at one time. Defaults to None.
        prioWeights (optional): Alters ratio of high priority and low priority processes. Defaults to "even".
        ofile (optional): Name of output fille. Defaults to "data".

    """
    process_id: int = 0
    time: int = 0

    if "." in ofile:
        name, ext = ofile.split(".")
    else:
        name = ofile
        ofile = ofile + ".json"

    jsonJobs: list = []

    # If file is run with command line args, cast `str` numbers to `int`
    nj = int(nj)
    minCpuBT = int(minCpuBT)
    minIOBT = int(minIOBT)
    minNumBursts = int(minNumBursts)
    minat = int(minat)

    # default values
    if not maxCpuBT:
        maxCpuBT = random.randint(minCpuBT + 3, minCpuBT + 8)
    else:
        maxCpuBT = int(maxCpuBT)

    if not maxIOBT:
        maxIOBT = random.randint(minIOBT, minIOBT + 5)
    else:
        maxIOBT = int(maxIOBT)

    if not maxNumBursts:
        maxNumBursts = random.randint(minNumBursts + 3, minNumBursts + 8)
    else:
        maxNumBursts = int(maxNumBursts)

    if not maxat:
        maxat = random.randint(minat, minat + 2)
    else:
        maxat = int(maxat)

    if "cpu" in intBurstType:
        minCpuBT += 10
        maxCpuBT += 20
        minIOBT -= 9
        maxIOBT -= 9

    if "io" in intBurstType:
        minIOBT += 10
        maxIOBT += 20
        minCpuBT += 4
        maxCpuBT += 4

    prios = WeightedPriorities(prioWeights)

    while process_id < nj:
        jsonJob = {}
        jobs = random.randint(minat, maxat)  # num jobs at this time
        for _ in range(jobs):
            jsonJob["arrival_time"] = time
            cpub = random.randint(minNumBursts, maxNumBursts)  # num cpu bursts
            jsonJob["process_id"] = process_id
            priority = prios.getNext()
            jsonJob["priority"] = priority

            ioBursts = []
            cpuBursts = []

            for _ in range(cpub - 1):
                b = random.randint(minCpuBT, maxCpuBT)
                i = random.randint(minIOBT, maxIOBT)
                cpuBursts.append(b)
                ioBursts.append(i)

            b = random.randint(minCpuBT, maxCpuBT)
            cpuBursts.append(b)

            jsonJob["cpu_bursts"] = cpuBursts
            jsonJob["io_bursts"] = ioBursts
        process_id += 1
        jsonJobs.append(jsonJob)
        time += 1

    with open(ofile, "w") as jsonFile:
        kwargs: dict = {
            "nj": nj,
            "minCpuBT": minCpuBT,
            "maxCpuBT": maxCpuBT,
            "minIOBT": minIOBT,
            "maxIOBT": maxIOBT,
            "minNumBursts": minNumBursts,
            "maxNumBursts": maxNumBursts,
            "intBurstType": intBurstType,
            "minat": minat,
            "maxat": maxat,
            "prioWeights": prioWeights,
            "ofile": ofile,
        }

        jsonData: dict = {"kwargs": kwargs, "jobs": jsonJobs}

        json.dump(jsonData, jsonFile, indent=4)

    return None


if __name__ == "__main__":
    from rich import print

    argv: list[str] = sys.argv[1:]

    args, kwargs = parse_commandline_args(argv)

    if "--help" in args:
        # Print documentation
        help("generate_input")
        sys.exit()

    print("Default values can be changed in the `generate_file` function. \n")
    print("However run this file with `--help` after filename to get a usage ")
    print("example to change values from command line. \n")
    generate_file(**kwargs)
