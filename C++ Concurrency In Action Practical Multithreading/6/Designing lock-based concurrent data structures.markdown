# Designing lock-based concurrent data structures

## 6.1 What does it mean to design for Concurrency? 
- Multiple threads can access the data structure concurrently, no data will be
lost or corrupted, all invariants will be held up, and there will be no problem
causing race conditions. This is called a thread safe data structure.
- The type of access changes how safe the data structure is, a data structure
may be thread safe if all the threads are performing the same action, but may
not be safe if all of the threads are performing different accesses to the data
structure.
- Designing for concurrency means providing the opportunity for concurrency. A
mutex provide mutual exclusion, only one thread can access the lock on the mutex
at a time; hence a mutex prevent concurrent access to the data that it protects.
- This is called serialization, threads take turns to access the data protected
by the mutex. Must be careful when designing the data structure.
- The main idea is the try to have a small protected region, such that few
operations are serialized, and there will be greater potential for concurrency.

### 6.1.1 Guidelines for designing data structure for concurrency
- Some general guidelines:
  - Ensure threads do not see a state where invariants of the data structure
  have been broken by another thread
  - Avoid race conditions inherent in the interface to the data structure by
  providing functions for complete operations rather than for operation steps
  - Pay attention to how the data structure behaves in the presence of
  exceptions to ensure that data structures are not broken.
  - Minimize the opportunity for data lock by restricting the scope of locks,
  and avoid nesting locks when possible.
- Also need to consider if a thread is accessing the data structure through a
certain function, which functions are safe to call from the other threads?
- A developer can also consider allowing concurrent read access to the data
structure, however, serialized write access to the data structure. This is
supported by `boost::shared_mutex`
- Simplest thread safe data structure used mutexes and locks to protect the data

## 6.2 Lock-based Concurrent Data structures
- Ensure that the correct mutex is locked when accessing data, and the lock is
held for the minimum amount of time. 
- Also need to ensure that the data is not accessed outside of the protection
mechanism of the mutex, and there are no race conditions inherent in the
interface.
- Need to be very careful when designing a data structure which has more than
one mutex.

### 6.2.1 A thread safe stack using locks
```C++
#include <exception>

struct empty_stack: std::exception
{
	const char* what() const throw();
};

template<typename T>
class threadsafe_stack
{
private:
  std::stack<T> data;
  mutable std::mutex m;

public:
threadsafe_stack(){};

threadsafe_stack(const threadsafe_stack& other)
{
	std::lock_guard<std::mutex> lock(other.m);
	data=other.data;
}

threadsafe_stack& operator=(const threadsafe_stack&) = delete;

void push(T new_value)
{
    std::lock_guard<std::mutex> lock(m);
		data.push(std::move(new_value));
}

std::shared_ptr<T> pop()
{
	std::lock_guard<std::mutex> lock(m);
	if(data.empty())
		throw empty_stack();
	std::shared_ptr<T> const res(
		std::make_shared<T>(std::move(data.top())));
	data.pop();
	return res;
}

void pop(T& value)
{
	std::lock_guard<std::mutex> lock(m);
	if(data.empty())
		throw empty_stack();
	value=std::move(data.top());
	data.pop();
}

bool empty() const
{
  std::lock_guard<std::mutex> lock(m);
  return data.empty();
}
};
```
- Let see how this class/structure does or does not follow the basic guidelines
outlined before
- Each member function is protected by locking the mutex before performing each
operation, ensures only one thread can access the data at a time, no thread will
see a broken invariant.
