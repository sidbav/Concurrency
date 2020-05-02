# Liveness

## Deadlock
- Assume that there are two threads, and two locks. A **DeadLock** occurs when one thread obtains one lock, and the other obtains the other lock. Now both threads are waiting for the second lock to be released, but that will never happen.
- **Liveness** is a set of properties that require a system to make progress. Members may have to "take turns" in crictical sections
- One way to avoid a deadlock like described in the previous example is to ensure that there is "first" lock, and then a second lock that must be accquired. This will help to avoid any situation of deadlocks.