# Asynchrous Tasks

## Computational Graph
- Key to concurrent programming is to determine which tasks can occur in any order AKA async.
- Computational Graphs can be used to draw out steps within a task, they provide gernal steps in a program. Can help determine to what extend your program can be concurrent.
- Each tasks in a Computational Graph can be assigned a time (how long it will take to perform each task).
- The sum of all of the times is referred to as the Work for the program.
- The path which takes the longest time is referred to as the Critical Path.
- The sum of all the times from Critical Path gives you a metric referred to as the **Span**. The span is the shortest amount of time a program will take to run if it is parrallized as much as possible.
- The ratio between the Work and the span (Span/Work) is referred to as the Ideal Parrallism of a program.

## Thread Pool
- After identifying which tasks are able to run asynchorusly, we can create seperate threads/processes for each of these tasks.
- In some senarios it is not efficent to have a new thread to tackle each of the indivdual tasks. It is better to have a **Thread Pool**
- **Thread Pool** - Creates and maintains a small collection of worker threads. The thread pool reuses the exisiting working threads to execute tasks.
- The benefit of just reusing the same thread is that it takes less time to execute the task than to create a new worker thread

### How to create a thread pool in Python?
- We can use the `ThreadPoolExecutor` Class, located in the `concurent.futures module`
- provides a high level interface for async tasks
- `ThreadPoolExecutor(max_workers=None)` will create 5*CPUs in the machine
- `shutdown()` frees up any resources that the ThreadPoolExecutor was using after pending tasks are finished.
- ThreadPoolExecutor is espically useful when you a lot of IO tasks. Not useful for CPU tasks, so the work around is the `ProcessPoolExecutor`.

## Future
- **Future** - a placeholder for a result that is initally unknown, but will be known later AKA in the futre.
- Lets you access the result of an async operation.
- This is similar to the concept of a Promise is JS

### Futures in Python
- Future class - returned by `Executor.submit()` method
- Some of the methods that the future class has:
  - `cancel()`
  - `cancelled()`
  - `running()`
  - `done()`
  - `result()` - returns the value returned by the call

## Divide and Conquer
- **Divide** a larger problem into smaller sub problems of about equal size.
- **Conquer** phase finds the solutions to each of the sub problems
- **Combine** the solutions to each of the subproblems.

Common structure for Divide and Conquer problems is the following:
- if "base case":
  - solve problem
- else:
  - divide the problem into two smaller pieces, and tackle does problems.
