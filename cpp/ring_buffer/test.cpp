#include "ring_buffer.h"
#include <chrono>
#include <ctime>

void producter()
{
    unsigned int i = 0,t=150;
    while(1)
    {
        push(i++);
        printf("producter:%d\n",i-1);
        //t=100+std::rand()/((RAND_MAX + 1u)/6);  // Note: 100+rand()%6 is biased
        std::this_thread::sleep_for(std::chrono::milliseconds(t));
    }
}

void consumer()
{
    unsigned long val;
    while(1)
    {
        val = pop();
        printf("consumer:%ld\n",val);
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

int main()
{
    
    std::srand(std::time(nullptr)); // use current time as seed for random generator

    std::thread t1(producter);
    std::thread t2(consumer);

    t1.join();
    t2.join();
}
