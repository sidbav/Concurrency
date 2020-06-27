# Hello, world of concurrency in C++!

## 1.1 What is concurrency?
- two or more seperate activites happening at the same time.

### 1.1.1 Concurrency in Computer Systems
- Single program perform multiple tasks in parralel
- In the past most computers only had one processor, hence making parrellel
 programs difficult to come by. Even concurrent programs would perform just like
 seqeutial programs in terms of speed.
- However, it can switch between tasks multiple times a second.
- Only multi core processors or multi-processor machines are capable of running
 a true parrallel program. This is referred to as hardware concurrency.

### 1.1.2 Approches to Concurrency
- Multiple single threaded processes OR multiple threads in a single prcoess.

#### Concurrency with Multiple Processes
- There would have to interprocess communication
  - singles, sockets, piples
  - this communication is very slow, and complex
- OS needs to provide a lot of protection against the processes from
 overwriting each other's data.
- Running a process requires a lot of overhead.
- Easier to write safe concurrent code for processes, compared to threads.

#### Concurrency with Multiple Threads
- Threads are lightweight compared to processes.
- All threads share the same address space. much easier to communicate between
 threads and share data between threads.
- The programmer must be careful to write code such that all threads access
 accurate data. Need to consider how the threads will communicate with each
 other.
- Favoured way to write concurrent code.

## 1.2 Why Use Concurrency?
- Two main reasons to use concurrency:
1. Seperation of concerns
2. Performance.

### 1.2.1 Using Concurrency for Seperation of Concerns
- By keeping related code together, and unlreated code apart, makes programs
 easier to understand and test, less likely to contain bugs.
- For example, any UI serves must perform multiple things at once.
  - Take in the users commands.
  - Respond to those users commands, and be ready to take in more commands
 from the user at the same time.
- You want to be able to run the UI while still handling the users input \
(download a file)
- Using threads by this logic makes the logic in each thread simplier, since it can just focus on its specfic task without having to worry about a lot of communication with the other threads.
- The number of threads is independent the number of CPUs since the division in threads is based on a conceptual idea rather than increasing performance.

### 1.2.2 Using Concurrency for Performance.
- **Task parrallism** - take a program, break it up into subtasks, and run them in parrallel
- Sounds simple, but extremley complex. Lots of dependencies between the different subtasks.
- Can divide the processing, one thread handles one part of the algo, while a different thread handles another.
- Can divide by data. Each thread perfroms the same operation on different pieces of data. This is referred to as **Data Parralleism**
- Data Parrallism is the easiest type of concurrent program to write. You write the code for one thread, then just have it handle multiple.

### 1.2.3 When not to use Concurrency
- Concurrent code is harder to maintain, so it is only worth if maintaining it is worth it
- Performance gain may not be as much as you are expecting. Lots of overhead.
- More threads mean that more of the OS resoures are taken up
- Also more threads mean that the OS must run lots of context switches.

## 1.3 Concurrency and MultiThreading in C++
- C++11 introduces a standardized way to multithreading in C++

## 1.4 Getting Started

### 1.4.1 Hello, Concurrent World
- A very simple multithreaded program:
```C++
#include <iostream>
#include <thread> // Library for Standardized multithreading support in C++

void hello() {
    std::cout<< "Hello Concurrent World\n";
}

int main() {
    std::thread t(hello);
    t.join();
}
```
- Each thread must have its an intial function. The Inital thread in any program
 comes from main.
- From the main thread we call `t.join()` This ensures that before we exit the
 program that the t thread is finished executing.
