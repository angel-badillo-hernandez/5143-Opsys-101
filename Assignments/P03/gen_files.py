"""
Generates the JSON files needed for presentation.
"""
from generate_input import generate_file
NJ = 25
generate_file(
    nj=NJ,
    minNumBursts=4,
    maxNumBursts=10,
    intBurstType="cpu",
    ofile="cpu_int.json",
    maxat=10,
    minat=5
)

generate_file(
    nj=NJ,
    minNumBursts=4,
    maxNumBursts=10,
    intBurstType="io",
    ofile="io_int.json",
)

generate_file(
    nj=NJ,
    minNumBursts=4,
    maxNumBursts=10,
    prioWeights="high",
    ofile="prio_high.json",
)