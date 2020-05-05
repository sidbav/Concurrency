#include <iostream>
#include <thread> // Library for Standardized multithreading support in C++

void hello() {
    std::cout<<"Hello Concurrent World\n";
}

int main() {
    std::thread t(hello);
    t.join();
}