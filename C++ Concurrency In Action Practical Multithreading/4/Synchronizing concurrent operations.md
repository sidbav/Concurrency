## Synchronizing concurrent operations

## 4.1 Waiting for an event or other condition
- When one thread is waiting for another thread to finish up its task (release
the mutex), it can do one of three things. A, keep checking to see if the
mutex has been release. This is wasting lots of time, and processing resources
that can be used by other threads in the mean time. B is to have the thread
sleep for short periods of time, using the `std::this_thread::sleep_for()`
function.

```C++
bool flag;
std::mutex m;
void wait_for_flag()
{
    std::unique_lock<std::mutex> lk(m);
    while(!flag)
    {
        lk.unlock();
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        lk.lock();
    }
}
```
- before the sleep the mutex unlocks the thread, and then after waking up it
locks the thread again. This is great since the thread does not waste any
compute resources while it is sleeping. However, this still wastes a lot of
time!
- The final options is the preferred one. Use a conditional variables, the
thread actually waits for the other to complete its work.
- Condition variable associated with some event of condition, when a thread
knows that the condition has been met, it can notify other threads.This will
wake up the waiting threads.

### 4.1.1 Waiting for a condition with condition variables
- The Standard C++ Library provides not one but two implementations of a
condition variable: `std::condition_variable` and `std::condition_variable_any`.
Both are located in the `<condition_variable>` header file.
- Example of using `std::condition_variable`:

``` C++
std::mutex mut;
std::queue<data_chunk> data_queue;
std::condition_variable data_cond;
void data_preparation_thread()
{
    while(more_data_to_prepare())
    {
        data_chunk const data = prepare_data();
        std::lock_guard<std::mutex> lk(mut);
        data_queue.push(data);
        data_cond.notify_one();
    }
}
void data_processing_thread()
{
    while(true)
    {
        std::unique_lock<std::mutex> lk(mut);
        data_cond.wait(
        lk,[]{return !data_queue.empty();});
        data_chunk data=data_queue.front();
        data_queue.pop();
        lk.unlock();
        process(data);
        if(is_last_chunk(data))
            break;
    }
}
```
- A queue is used to pass data between the threads.
- When the data is ready, the thread preparing the data locks the mutex, and
pushes data onto the queue, Then using the condition variable notifies a thread
that it is done if there is one waiting.
- There is also a data processing thread. The thread locks the mutex first.Then
the condition variable calls wait, which passes the lock object, and waits for
the queue to not be empty. If the queue is empty, the conditon variable will
unlock the mutex, otherwise it will keep it lock.
- If the condition variable returns false, then the thread will be put in the
waiting state, and then when notified, it will obtain the lock and then continue.
- A `std::unique_lock` is used rather than a `std:lock_guard` since a waiting
thread can unlock the mutex, and locked again afterward.
- The function in the call to `wait` can be called many times, and be abandoned
at any time, so it is best that the function does not have side effects.

##### 4.1.2 Building a Thread safe queue with condition variables.
- Three basic operations for a queue:
  - query the state of the queue (`empty()`, `size()`)
  - modify the queue
  - query the elements of queue.
- The same race condition exist as before, need to combine the calls to front
and pop, and top and pop.
- Instead we can have two different functions: `try_pop()`: returns immedaitely
indicating success or failure. `wait_and_pop()`: wait until there is a value to
retrived.
- Here is the class:

```C++
#include <memory>
template<typename T>
class threadsafe_queue
{
public:
  threadsafe_queue();
  threadsafe_queue(const threadsafe_queue&);
  threadsafe_queue& operator=(
     const threadsafe_queue&) = delete;
  void push(T new_value);

  bool try_pop(T& value);
  std::shared_ptr<T> try_pop();

  void wait_and_pop(T& value);
  std::shared_ptr<T> wait_and_pop();

  bool empty() const;
};
```
- Cannot assign the assignment of the queue for simplicity.
- The first version of `try_pop()` stores a reference to a variable to store
the result. The second version returns a pointer to the value, if there is not
a value it will return a `nullptr`.

```C++
#include <queue>
#include <mutex>
#include <condition_variable>
template<typename T>
class threadsafe_queue
{
private:
    std::mutex mut;
    std::queue<T> data_queue;
    std::condition_variable data_cond;
public:
    void push(T new_value)
    {
      std::lock_guard<std::mutex> lk(mut);
      data_queue.push(new_value);
      data_cond.notify_one();
    }
    void wait_and_pop(T& value)
    {
      std::unique_lock<std::mutex> lk(mut);
      data_cond.wait(
        lk,[this]{return !data_queue.empty();}
      );
      value=data_queue.front();
      data_queue.pop();
    }
};
threadsafe_queue<data_chunk> data_queue;
void data_preparation_thread()
{
    while(more_data_to_prepare())
    {
      data_chunk const data=prepare_data();
      data_queue.push(data);
    }
}
void data_processing_thread()
{
    while(true)
    {
      data_chunk data;
      data_queue.wait_and_pop(data);
      process(data);
      if(is_last_chunk(data))
        break;
    }
}
```
- Both the mute and the condition variable and contained in the threadsafe
class
- Condition variables can be used in when there are any threads waiting for the
mutex. Instead you can use `notify_all` which triggers all the threads calling
wait to check their condition variable.

## 4.2 Waiting for One-Off events with futures.
- If you there is a one time event, a thread can obtain a "future" which
represents this object. Then the thread can periodically check if the event has
occured, while performing some other task. Once the future value has been
obtained, it cannot be reset.
- C++ has two different types of futures located n the `<future>` header file
  - A unique future `std::future<>`
  - A shared future, `std::shared_future<>`
- A `shared_future` can represent many instances of one event.
- The `std:future<void>` , `std::shared_future<void>` should be used where
there’s no associated data, just waiting for the event to occur.
- Futures are used to communicate between threads, but they must be protected by
a mutex if being accessed by multiple threads.

### 4.2.1 Returning values from background tasks
- Suppose that you need to run some functions to obtain a result, however, it,
takes a really long time to compute. A future can be used here instead.
- `std::async` may also be used so that the result can be obtained, here is an
example:
```C++
#include <future>
#include <iostream>
int find_the_answer_to_ltuae();
void do_other_stuff();
int main() {
    std::future<int> the_answer=std::async(find_the_answer_to_ltuae);
    do_other_stuff();
    std::cout<<"The answer is "<<the_answer.get()<<std::endl;
}
```

### 4.2.2 Associating a task with a future.

