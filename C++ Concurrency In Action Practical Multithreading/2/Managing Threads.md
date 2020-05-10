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
        if(t.joinable())
            t.join();
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
- by default the arguments are copied into internal storage, where they can be accessed by the newly created thread of execution, even if the corresponding parameter in the function is expecting a reference.
``` C++
void f(int i,std::string const& s);
std::thread t(f,3,”hello”);
```
- Here `"Hello"` is a char * not a std::string. It is not a problem here, however, if we were in a function, and the thread is detached from the main thread then, this could raise issues, so it is best that we ensure that the string is casted correctly:
``` C++
void f(int i,std::string const& s);
void not_oops(int some_param)
{
    char buffer[1024];
    sprintf(buffer,"%i",some_param);
    std::thread t(f,3,std::string(buffer));
    t.detach();
}
```
- `std::thread` copies values as is, hence it would have recieved.
- Essentially the main message that is comming from this is to make sure that you are correectly providing the data aruguments.

You can provide a member function pointer as a function as well. A suitable object must be provided as well in order to this.
``` C++
class X
{
public:
    void do_lengthy_work();
};
X my_x;
std::thread t(&X::do_lengthy_work,&my_x);
```
- Here we provided the class of a function (`do_lengthy_work`), and we provided as an arugument to the function the object `my_x`.
- It will invoke `my_x.do_lengthy_work()` on a seperate thread since we provided the address of the my_x object to the thread object.

There can also be cases where the supplied arguments cannot be copied to the thread, and they can only be *moved*. Moved from one object to another. An example of such an object is a `std::unique_ptr`, provides automatic memory management to pointers
- `std::move` can be used to tranfer ownship between two objects.
``` C++
void process_big_object(std::unique_ptr<big_object>);
std::unique_ptr<big_object> p(new big_object);
p->prepare_data(42);
std::thread t(process_big_object,std::move(p));
```
- The ownership of the object is transferred to the thread and the function.

## 2.3 Transferring Ownership of a Thread
- Imagine that you want to write a function that creates a thread that runs in the background, which then passes ownership of the thread to the calling function rather than waiting for the thread to be finished.
- Or you create a thread in one function, and then pass the ownership to a different function that should wait for the thread to finish executing.
- In either cases the thread needs to be "handed off", and the owner of the thread will be changing
- A `std::thread` cannot be copied, and can only be moved. For example here:
``` C++
void some_function();
void some_other_function();
std::thread t1(some_function); // A new thread is created to run function t1
std::thread t2=std::move(t1); // Another thread is created, as ownship of the thread is moved from t1--> t1
t1=std::thread(some_other_function); // A new thread is now created again with the t1 thread onject, with a different function. An important thing to not here is that we are moving owneship from a temp object to a permant? object, hence we do not need to use the std::move semantic
std::thread t3; // new thread object, not assoicated to anything
t3=std::move(t2); //  t3 takes ownership of the thread some_function
t1=std::move(t3); // This will stop program executiuon since some_other_function is likely still running on the t1 thread. std::terminate is called to end the program
```
Here is an example of returning a `std::thread` from a function
```  C++
std::thread f()
{
    void some_function();
    return std::thread(some_function);
}
std::thread g()
{
    void some_other_function(int);
    std::thread t(some_other_function,42);
    return t;
}
```
- You can simply call the functions `f()` or `g()`, and either one will invoke a thread, and return the thread to the call of function `g()` or `f()`.

Can also take an std::thread as an argument to functions.
``` C++
void f(std::thread t);
void g()
{
    void some_function();
    f(std::thread(some_function));
    std::thread t(some_function);
    f(std::move(t));
}
```
- This creates to different threads, and invokes the function `f()`

Can use the `thread_guard` class from before, and actually take ownership of the thread. If the `thread_guard` outlives the thread it was referencing then it means that no one else can join or detach from the thread once the thread_guard takes ownership.

```C++
class scoped_thread
{
    std::thread t;
public:
    explicit scoped_thread(std::thread t_):t(std::move(t_)) {
        if(!t.joinable())
            throw std::logic_error("No Error!");
    }
    ~scoped_thread() {
        t.join();
    }
    scoped_thread(scoped_thread const&)=delete;
    scoped_thread& operator=(scoped_thread const&)=delete;
};

struct func;

void f() {
    int some_local_statel;
    // A new thread is passed directly to the scoped_thread, rather than creating a seperate variable for it
    scoped_thread t(std::thread(func(some_local_state)));
    do_something_in_current_thread();
}
```
- When the initial thread reaches the end of `f`, the `scoped_thread` will be destoryed, hence the thread that was created will be joined. Before, the destrcutor had to check before actually joining the thread

`std::thread` is also move aware. This allows you to write code like this:
``` C++
void do_work(unsigned id);
void f() {
    std::vector<std::thread> threads;
    for(unsigned i=0;i<20;++i) {
        threads.push_back(std::thread(do_work,i));
    }
    std::for_each(threads.begin(),threads.end(), std::mem_fn(&std::thread::join));
}
```
- The for loop spawns threads, and we also join each thread. This allows you to treat threads as a group, rather than a individuals.
- One problem is this does not handle any of the data the threads may return

## 2.4 Chosing the Number of Threads at Runtime.
- `std::thread::hardware_concurrency()` - determines the number of processors that a machine has. Useful for determining how to split a tasks in multiple threads.
- Lets take a look at an example of a parrallel interperation of `std::accumlate`. Divides work among threads with a minimum number of elements thread.
``` C++
template<typename Iterator,typename T>
struct accumulate_block
{
    void operator()(Iterator first,Iterator last,T& result)
    {
        result=std::accumulate(first,last,result);
    }
};

template<typename Iterator,typename T>
T parallel_accumulate(Iterator first,Iterator last,T init)
{
    unsigned long const length=std::distance(first,last);
    if(!length)
        return init;
    unsigned long const min_per_thread=25;
    unsigned long const max_threads = (length+min_per_thread-1)/min_per_thread;
    unsigned long const hardware_threads = std::thread::hardware_concurrency();
    unsigned long const num_threads =
            std::min(hardware_threads!=0?hardware_threads:2,max_threads);
    unsigned long const block_size=length/num_threads;

    std::vector<T> results(num_threads);
    std::vector<std::thread> threads(num_threads-1);

    Iterator block_start=first;
    for(unsigned long i=0;i<(num_threads-1);++i) {
        Iterator block_end=block_start;
        std::advance(block_end,block_size);
        threads[i]=std::thread(accumulate_block<Iterator,T>(),
            block_start,block_end,std::ref(results[i]));
        block_start=block_end;
    }
    accumulate_block<Iterator,T>()(block_start,last,results[num_threads-1]);
    std::for_each(threads.begin(),threads.end(),
        std::mem_fn(&std::thread::join));
    return std::accumulate(results.begin(),results.end(),init);
}
```
- Calculate the number of threads that you will create depending on the number of threads avilable on the machine, and depending on the number elements that we would like to sum up.
- Do not want to run more threads than your hardware can support, this is referred to as **oversubscription** since the more threads we have will actually decrease the performance of our program.
- launch one thread less than required since we already have one thread. (the main thread)
- the result of the parrallel accumlate may vary each run, and second it may wary with just the accumlate block. This depends on the type of T.
- cannot return anything from a thread (void function), and we use the results arrary to collect the summation of all of the results.
- In this case we were able to pass of the required information to the thread, even the location where the result should be stored. May not always be the case

## 2.5 Identifying Threads.
- call the `get_id()` function on a `std::thread` object. If the thread is not associated with a thread that is running (the owner ship of the thread was moved to another), will return a default "not any thread".
- if two `std::thread::id` have the same id, then they represent the same thread. IDs can be compared with each other if needed.
- The thread IDs are often used to checked wether a thread needs to perform some operation. Example: threads need to divide work among each others. For example the main thread that lauched the other threads may need to do it work slightly differently. the main thread can call `std::this_thread::get_id()` before lauching the other threads and save this value. Then each thread can check its ID compared to the one stored.
``` C++
std::thread::id master_thread;
void some_core_part_of_algorithm()
{
    if(std::this_thread::get_id()==master_thread)
    {
        do_master_thread_work();
    }
    do_common_work();
}
```
-  can also store the thread id in some sort of data structure

