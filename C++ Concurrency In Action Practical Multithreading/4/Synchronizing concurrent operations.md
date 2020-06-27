# Synchronizing concurrent operations

## 4.1 Waiting for an event or other condition
- When one thread is waiting for another thread to finish up its task (release \
the mutex), it can do one of three things. A, keep checking to see if the \
mutex has been release. This is wasting lots of time, and processing resources \
that can be used by other threads in the mean time. B is to have the thread \
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
- before the sleep the mutex unlocks the thread, and then after waking up it \
locks the thread again. This is great since the thread does not waste any \
compute resoucres while it is sleeping. However, this still wastes a lot of \
time!
- The final options is the perffered one. Use a conditional variables, the \
thread actually waits for the other to complete its work.
- Condition variable associated with some event of condidition, when a thread \
knows that the condiditon has been ment, it can notify other threads. \
This will wake up the waiting threads.

### 4.1.1 Waiting for a condition with condition variables
- The Standard C++ Library provides not one but two implementations of a \
condition variable: `std::condition_variable` and `std::condition_variable_any`\
. Both are located in the `<condition_variable>` header file.
- Example of using `std::condition_variable`:

``` C++
std::mutex mut;
std::queue<data_chunk> data_queue;
std::condition_variable data_cond;
void data_preparation_thread()
{
    while(more_data_to_prepare())
    {
        data_chunk const data=prepare_data();
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
