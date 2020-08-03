# Barriers

## Race Conditions
- **Race Condition** is a flaw in a program's timing or ordering of a program's
execution which causes incorrect behaviour. Many Races are caused by data races,
data races lead to races.
- The order in which two threads run can lead to incorrect results in many
cases.
- A mutex can be used to protect a program from a data race, but the possibility
of a race condition can still exist in a program.
- Changing the timing, and thus the order of execution of threads can help you
detect race conditions, however they are not easy to find.

## Barrier
- In order to prevent Race conditions from occurring, we can use a Barrier
- **Barrier** - Prevents a group of threads from preceding until enough threads
have reached the barrier.
