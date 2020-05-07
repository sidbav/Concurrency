# 2 Managing Threads

## 2.1 Basic Thread Managment
- Each C++ program has atleast one thread.

### 2.1.1 Launching a Thread
- Threads must be associated with a function. In the simplest case, a thread is assciated with a void function, that takes no parameters.
- In a more complex case the function can take additional parameters, performs a series of independent operations which it is instructed to do so, and it only stops when it is instructed to do so.
- Doesnt matter what a thread is gonna do, whether it be complex or straightforward the basic structure of forming a thread is the following:
``` C++
void do_work();
std::thread t(do_work);
```
- std:: s works with any callable type, can pass an instance of a class with a function call operator to the std::thread constructor.
For example:
```C++
class background_task {
public:
    void operator()() const
    {
        do_something();
        do_something_else();
    }
};
background_task f;
std::thread my_thread(f);
```
- In this case the function object `f` is copied into storage belonging to the newly created thread.
- When a thread is started, you can wait for it to be finished (by calling join) OR you can leave it on its own and detaching it.
- If you do not wait for your thread to finish, you need to ensure that the data the thread is accessing is valid. This can occur when the threade holds pointers or referecnes to local variables and the thread has not finished when the function exits.
``` C++
struct func {
    int& i;
    func(int& i_):i(i_) {}
    void operator()() {
        for(unsigned j=0;j<1000000;++j)
            do_something(i);
    }
};

void oops() {
    int some_local_state=0;
    func my_func(some_local_state);
    std::thread my_thread(my_func);
    my_thread.detach();
}
```
- In this case, when oops exits, the thread will still be running. If the thread is stilling running, it will attempt to access an already destoryed variable.
- One way to avoid this type of reference is to ensure that each thread has its own copy of the data

### 2.1.2 Waiting for a thread to complete
- call `join()` on the thread, and this will wait for the thread to finish.
- can only call join once on a given thread. The thread is no longer `joinable()`, joinable will return false

### 2.1.3 Waiting in Exceptional Circumstances
- Typically if you are going to call `detach()` on a thread, you will call it imedialely
- Additionally, when you are calling `join()` you need to be carefully, when you call it. It is possible it is skipped when an exception is called.
- Typically when you are calling join, you also need to perpare to call join when you catch any exceptions. For example:
``` C++
struct func; (from previous example)
void f() {
    int some_local_state=0;
    func my_func(some_local_state);
    std::thread t(my_func);
    try {
      do_something_in_current_thread();
    } catch(....) {
      t.join();
      throw;
    }
    t.join();
}
```
- Using a try catch block is not ideal. If is is nessacary to ensure that a thread is complete before a thread completes then you must consider the case for all possible exit paths, wether is is normal or an exception.
- One way to do this is to Resource Acquisition Is Initialization (RAII) idiom and provide a class that does the join in its constructor.
``` C++
class thread_guard {
    std::thread& t;
public:
    explicit thread_guard(std::thread& t_):t(t_) {}

    ~thread_guard() {
        if(t.joinable()) {
        t.join(); }
    }
    thread_guard(thread_guard const&)=delete;
    thread_guard& operator=(thread_guard const&)=delete;
};

struct func;
void f() {
    int some_local_state=0;
    func my_func(some_local_state);
    std::thread t(my_func);
    thread_guard g(t);
    do_something_in_current_thread();
}
```
- When the execution of the current thread ends, the thread_guard is destoryed, thus the thread will be joined. This will occur regardless of if the function `do_something_in_current_thread();` throws an exception
- The copy constructor and copy-assignment operator are marked `=delete` to ensure that they’re not automatically provided by the compiler. Copying or assigning such an object would be dangerous, because it might then outlive the scope of the thread it was joining. By declaring them as deleted, any attempt to copy a `thread_guard` object will generate a compilation error.
- In the case that you do not care if the thread is done executing, you can just detach from the thread immedaitely. The thread is now not associated with the std::thread object, so the new thread will not be destoryed when the std::thread object is destoryed.

### Running Threads in the Background
- Detached threads run in the background, there is no way of communicating with these threads. They are referred to as daemon threads.
- You can only detach from a thread that is joinable.
- A good example of where you can use detached threads is when you have mutiple windows in one application which are independent of each other. You can have detached threads running each window since they do not need to rely on each other.
``` C++
void edit_document(std::string const& filename)
{
    open_document_and_display_gui(filename);
    while(!done_editing())
    {
        user_command cmd=get_user_input();
        if(cmd.type==open_new_document)
        {
            std::string const new_name=get_filename_from_user();
            std::thread t(edit_document,new_name);
            t.detach();
        } else
            process_user_input(cmd);
    }
}
```

## 2.2 Passing Arguments to a Thread Function
- you will pass the arguments like this:
- by default the arguments are copied into inter- nal storage, where they can be accessed by the newly created thread of execution, even if the corresponding parameter in the function is expecting a reference.


