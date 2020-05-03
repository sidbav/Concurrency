# Designing Parrallel Programs

The 4 stages to writing a Parrallel Prgram are the following:
1. Paritioning
2. Communication
3. Agglomeration
4. Mapping

## 1. Paritioning
- Breaking the problem down into smaller subproblems
- This can be done in one of two ways:
  - Domain Decomposition
  - Functional Decomposition

### Domain Decomposition
- Dividing the data associated with the problem into small and if possible, equally-sized partitions.
- Then focus on the processing that needs to be applied to each section of the data.

### Functional Decomposition
- First consider all of the computational work a program needs to do.
- Then divide these computational tasks into seperate tasks.
- Afterwards consider the data that is involved with each of the tasks.

Typically, you will use a combination of Functional and Domain Decomposition.

## 2. Communication
- How to corrdinate execution, and share data between tasks.
- Some tasks do not need to share any communication between each other, needs to be considered on a case by base basis

### Point to Point Communication
- When we need to estalish communication between each neigbouring task. For each task, one is acting as a sender (producer), and the other is the reciver (consumer).
- This is ideal when the communication is done between a small number of tasks.

### Collective Communication
- you can have a brodcaster, sends the same data to all other tasks, or you can have a scatter, sends data to a variety of tasks.
- In this case it is very important to consider scaling of the tasks, you need to be able to scale. Divide and Conquer is a good idea for, allowing scalling to be pretty easy.

### Synchrous Communication
- all tasks must wait until the entire communication is complete.
- Cannot do other work while this comminication is in progress
- Referred to as Blocking Communication.

### Asynchrous Communication
- Tasks do not have to wait for entire communication to complete.
- Can do other work as the communication is in progress
- Referred to as NonBlocking Communication.

Need to consider:
- **Overhead** (Compute time/resources) spent on communication
- **Latency**
- **Bandwidth** - The amount of data that can be communicated per second (GB/s)

## 3. Aggolometration
- Considering the solution developed from the Paritioning and Communication steps, and now consider the specfic hardware that you have on your specfic hardware.
- ReConsider the design from the previous steps, and then come up with a way to make it work better on your hardware.
- Granularity = Computation/Communication

### Fine Grain Parallelism
- Large number of small tasks.
- Advantage: Small tasks can be evenly distributed among processors. (Load balancing)
- Disadvantage: Low Granularity, loads of overhead for communication (since there are a lot tasks).

### Corse Gain Parallelism
- Small number of large tasks
- Advantage: Lower Granularity
- Disadvantage: Inefficent load balancing.

## Mapping
- Specify where each of the tasks will execute.
- Does not apply to single processor systems, or a system with automated task scheduling.
- The goal of mapping is to reduce the total execution time
- To do this, you can place tasks that are executing on different processors. OR you can focus on placing tasks that communicate often on the same processor
- Sometimes may require a dynamic load balacing technique.
- Hardware and program structure are key in considering mapping.
