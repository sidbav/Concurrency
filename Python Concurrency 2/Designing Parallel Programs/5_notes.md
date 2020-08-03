# Designing Parallel Programs

The 4 stages to writing a Parallel Program are the following:
1. Partitioning
2. Communication
3. Agglomeration
4. Mapping

## 1. Partitioning
- Breaking the problem down into smaller subproblems
- This can be done in one of two ways:
  - Domain Decomposition
  - Functional Decomposition

### Domain Decomposition
- Dividing the data associated with the problem into small and if possible,
equally-sized partitions.
- Then focus on the processing that needs to be applied to each section of the
data.

### Functional Decomposition
- First consider all of the computational work a program needs to do.
- Then divide these computational tasks into separate tasks.
- Afterwards consider the data that is involved with each of the tasks.

Typically, you will use a combination of Functional and Domain Decomposition.

## 2. Communication
- How to coordinate execution, and share data between tasks.
- Some tasks do not need to share any communication between each other, needs to
be considered on a case by base basis

### Point to Point Communication
- When we need to establish communication between each neighbouring task. For
each task, one is acting as a sender (producer), and the other is the receiver
(consumer).
- This is ideal when the communication is done between a small number of tasks.

### Collective Communication
- you can have a broadcaster, sends the same data to all other tasks, or you can
have a scatter, sends data to a variety of tasks.
- In this case it is very important to consider scaling of the tasks, you need
to be able to scale. Divide and Conquer is a good idea for, allowing scaling to
be pretty easy.

### Synchronous Communication
- all tasks must wait until the entire communication is complete.
- Cannot do other work while this communication is in progress
- Referred to as Blocking Communication.

### Asynchronous Communication
- Tasks do not have to wait for entire communication to complete.
- Can do other work as the communication is in progress
- Referred to as NonBlocking Communication.

Need to consider:
- **Overhead** (Compute time/resources) spent on communication
- **Latency** - The difference in time between indicating start of a data
transfer and when the data transfer started.
- **Bandwidth** - The amount of data that can be communicated per second (GB/s)

## 3. Agglomeration
- Considering the solution developed from the Partitioning and Communication
steps, and now consider the specific hardware.
- Reconsider the design from the previous steps, and then come up with a way to
make it work better on your hardware.
- Granularity = Computation/Communication

### Fine Grain Parallelism
- Large number of small tasks.
- Advantage: Small tasks can be evenly distributed among processors. (Load
balancing)
- Disadvantage: Low Granularity, loads of overhead for communication (since
there are a lot tasks).

### Coarse Gain Parallelism
- Small number of large tasks
- Advantage: Lower Granularity
- Disadvantage: Inefficient load balancing.

## Mapping
- Specify where each of the tasks will execute.
- Does not apply to single processor systems, or a system with automated task
scheduling.
- The goal of mapping is to reduce the total execution time
- To do this, you can place tasks that are executing on different processors.
OR you can focus on placing tasks that communicate often on the same processor
- Sometimes may require a dynamic load balancing technique.
- Hardware and program structure are key in considering mapping.
