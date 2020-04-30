# Chapter 1: Parrellel Computing Hardware

## 1.1: Sequential vs. parallel computing

### Sequential

- One step at a time, the program is broken up into each individual step, one thing can only happen at a time.
- Only one intstruction can be exectued at any one moment, there is no overlap between the instructions.
- The time that a sequential program takes to run is limited by the hardware the program is ran on,


### Parrallel
- Tasks can run at the exact same time. There is overlap between the steps, hence saving a lot of time, making the exection much faster.
- Parrallel programming requires extra effort inorder to communicate with the other threads in order to complete tasks that are dependent on one another
- completexity is added in order to improve the speed.
- Parrallel Extrectuon allows you to increase the throughput (the rate at which something is processed) of a program.


## 1.2: Parralled Computing Architectures

- Parrallel Programming requires having hardware that is parraellel; parrallel processors.

### Flynn's Taxonmy
- Used to describe multiprocessor architectures based on two factors:
  - The number of concurrent instruction or control streams
  - The number of data streams.

![Different Types of Multiprocessor Architectures](images/Flynn's Taxonomy.png)


