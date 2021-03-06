# Synchronization

## Condition Variable
- Limitation of mutexes - do not provide a method for threads to communicate
with each other, to allows threads to synchronize their actions.
- **Condition Variable** - Queue of threads waiting for a certain condition. A
place where threads can wait to be notified.
- **Monitor**:
  - Protects a critical section of code with a mutex
  - Provides threads with the ability to wait until a condition occurs, and it
  can signal the waiting  threads when their condition has been met.
- A condition variable has three main operations:
  - Wait:
    - Automatically releases the lock on the mutex
    - puts the thread into the waiting queue.
    - reacquire once given signal
  - Signal
    - Wake up *one* thread from the waiting queue, and now it can acquire the
    lock.
    - Also called *wake* or *notify* in other languages
  - Broadcast
    - Wake up *all* threads from the condition variable queue.
    - Also called *notify all* or *wake all*

A common situation where you will use a condition variable is a
**Shared Queue or Shared Buffer**. In this case, you will need to use the
following:
- Mutex - only one thread can modify the queue a time.
- Condition Variables:
  - BufferNotFull
  - BufferNotEmpty
- These condition variables allow threads to communicate to each other when the
state of the queue changes.

### Usage of Condition Variables
Typically will follow this structure:
``` Python
lock.accquire()

while not (SOME CONDITION):
    condition_variable.wait()

# do something (critical task)

lock.release()
conditon_variable.notify()
```
In Python you can use `with` to handle acquiring/releasing the lock.
``` Python
with lock:

    while not (SOME CONDITION):
        condition_variable.wait()

    # do something (critical task)

    conditon_variable.notify()
```

**Note**: The condition variable is not the same as the actual condition, the
condition variable is used so that it can be signalled. They are just a place
for the threads to wait until the threads are signalled again.

## Producer Consumer
- One of more thread acts as the producer:
  - Adds elements to a shared data structure
- One or more thread acts as the consumer:
  - Accesses elements in the shared data
- Synchronization Challenges:
  - Enforce Mutual Exclusion of the producers and consumers.
  - Prevent the producer from adding data to the queue when it is full
  - Prevent the consumer from removing data from an empty queue
- You may face a situation where the producer is an external data source. Hence
it is important to consider the Average rate at which the items are produced and
consumed from a queue. Ideally, you want the rate of consumption to be greater
than the rate of production.

### Pipeline
- Chain of processing elements, the output of one task is the input to the
other. Producer consumer pairs, with a buffer (Queue) between each element.

## Semaphores
- Synchronization Mechanism that is used to control access to a shared resource
- Can be used by many threads at the same time. Includes a counter to see how
many times it was acquired/released.

### Acquire
- If the counter > 0, the semaphore is available, decrements the counter
- If counter < 0, threads must wait until it is available, will be placed into a
queue.

### Release
- Increments the counter.
- If threads are waiting for the semaphore, they will be notified

A **Counting Semaphore** is counting the number of resources that are available.
  - Used to count the number of resources we have available
  - Track how many number are in a queue.

Can restrict a counting Semaphore to have values 0 or 1 only. This is called a 
**Binary Semaphore**
- Similar to a mutex by acquiring/releasing.
- **Key Difference** between a mutex and Semaphore:
  - Mutex must be acuired/released by the *same* thread
  - Semaphores can be acuired/released by *different* threads.

A pair of of Semaphores can be used to synchnorize a pair of producer and
consumer threads. One Semaphore can be used to track the number of empty spaces
(emptyCount), and another can track the number of items in the buffer
(fillCount).
- To add an item to the buffer, the producer thread will acquire the emptyCount
semaphore (decrementing its value by 1), put an item in the buffer, and then
release the fillCount semaphore (incrementing it value)
- To remove an item to the buffer, the consumer thread will acquire the
fillCount semaphore (decrementing its value by 1), remove an item in the buffer,
and then release the emptyCount semaphore (incrementing it value).

