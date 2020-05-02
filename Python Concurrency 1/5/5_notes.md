# Liveness

## Deadlock
- Assume that there are two threads, and two locks. A **DeadLock** occurs when one thread obtains one lock, and the other obtains the other lock. Now both threads are waiting for the second lock to be released, but that will never happen.
- **Liveness** is a set of properties that require a system to make progress. Members may have to "take turns" in crictical sections
- One way to avoid a deadlock like described in the previous example is to ensure that there is "first" lock, and then a second lock that must be accquired.
- The simplest way to avoid Deadlocks is to ensure that locks are taken in the same order by any thread. However one flaw with this method is a thread may not know all of the locks it will need to acquire ahead of taking any of them.
- Another method is lock timeout. If a thread is not able to successfully acquire all of the locks it needs within a certain amount of time, it will back up, free all of the locks that it did take. Then it will wait for a random amount of time before trying again to give other threads a chance to take the locks they need.

## Abandoned Locks
- Thread accquires a lock, but then it unexpectly terminates, it may not release the lock for other threads to use.
- Good pratice to release a lock if anything goes wrong in your program, so that remaining threads can still continue

## Starvation
- OS schedules when each thread will execute.... this can lead to problems.
- **Starvation** occurs when a thread/process is unable to gain access to a neccessary resource.

## LiveLock
- Multiple threads are actively responding to each other to avoid conflict, but that prevents them from making progress.
- LiveLocks can occur when two threads are designed to respond to the actions of each other.Both threads are busy doing something, but the combination of their efforts prevent them from doing anything useful
- Livelocks typyically arise from algos which attempt to detect and resolve deadlock