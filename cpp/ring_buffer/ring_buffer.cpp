#include "ring_buffer.h"

unsigned long write = 0;
unsigned long read = 0;
unsigned long size = RING_BUFFER_SIZE;
unsigned char buffer[RING_BUFFER_SIZE];
const unsigned long MASK = RING_BUFFER_SIZE - 1;
condition_variable cond_read;
condition_variable cond_write;
std::mutex mtx_;

//当读位置与写位置存在一定距离thresh，则开始写
static bool write_available()
{
    return read + Thresh >= write ;
}
//当读位置与写位置存在一定距离thresh，则开始读
static bool read_available()
{
    return read + Thresh < write ;
}

void push(unsigned char val)
{
    std::unique_lock<std::mutex> lock(mtx_);

    cond_write.wait(lock, write_available);//当读位置与写位置存在一定距离thresh内，则开始写，否则等待读位置

    buffer[write++ & MASK] = val;

    cond_read.notify_one();
}

void push2(unsigned char *val,int len)
{
    std::unique_lock<std::mutex> lock(mtx_);
    cond_write.wait(lock, write_available);//当读位置与写位置存在一定距离thresh内，则开始读，否则等待写位置
    for(int i=0;i<len;i++)
    {
        buffer[write++ & MASK] = val[i];
        printf("write pos:%d\n",write);
    }

    cond_read.notify_one();
}

unsigned char pop()
{
    std::unique_lock<std::mutex> lock(mtx_);

    cond_read.wait(lock, read_available);

    unsigned char x = buffer[read++ & MASK];
    printf("read pos:%d\n",read);
    cond_write.notify_one();

    return x;
}
