# Locks

## Reentrant lock
- **DeadLock** - All Processes and threads are unable to continue executing.
No other thread is able to unlock the mutex.
- There are times where a thread may need to lock a mutex multiple times, before
unlocking the mutex. In this case a Reentrant lock should be used.
- **Reentrant Mutex** is a type of mutex that can be locked by the same
thread/process multiple times. The mutex keeps track of how many times the
thread has been locked by the thread, and it must be unlocked the same number of
times in order to so that other threads can access the lock.
- One use case for a Reentrant lock is when writing a recursive function.
- Lock vs Rlock in python is that Lock can be released by a different thread,
whereas the RLock must be released by the same thread.

## Try Lock
- A non-blocking lock/acquire method to gain access to the mutex. It will
return immediately, and will return one to two values:
  - **True** and lock it if the mutex is available
  - **False** if the mutex is not available

## Read-Write Lock
- **Shared-Read** - locked in this mode, which allows multiple threads to read
the shared resource.
- **Exculsive Write Mode** - only one thread can lock in this mode, and only
that thread can write to the mutex and unlock it.
- Makes sense to use a shared read-writer lock when you have more threads
reading than writing. For example, in a Database application.

### Types of RWLocks in Python
- **RWLockFair** - equal preference to the read and writers
- **RWLockRead** - Read gets the priority
- **RWLockWrite** - Writer gets priority

### RWLock Methods
- `gen_rlock` - generates are reader lock object
- `gen_wlock` - generates another lock object that can only be used by writers,
and can only be accessed by one thread at a time.
