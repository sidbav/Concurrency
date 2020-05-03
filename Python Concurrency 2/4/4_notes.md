# Evalulating Parallel Performance

## Speedup, Latency, Throughput
- **Weak Scaling** - Variable number of processors, with a fixed problem size for each processor.
  - Accomplish more work, in the same time.
- **Strong Scaling** -Variable number of processors with a fixed total problem size.
  - Accomplish same work, in less time.
- **Throughput** - (number of task)/time
- **Latency** - time per task
- **SpeedUp** - (time to solve the problem sequentially) over (parrallel execution time with N workers)

## Amdahl's law
- Used to estimate speedup.
- Overall Speedup = ((1-P) + P/S)^-1:
  - Portion of a program that can be parrallizable
  - Speedup of the parallized portion
- Shows that there is really a limit to how much speedup you can achieve from a program

## Measure SpeedUp
- **Efficency** - How well additonal resources are used.
  - Speedup/ Processors.
