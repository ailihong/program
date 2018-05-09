#pragma once
#include<thread>
#include<mutex>
#include <condition_variable>
using namespace std;

#define RING_BUFFER_SIZE (24 * 1024)//  24k
#define Thresh (1 * 30)//4*1024


void push(unsigned char val);

void push2(unsigned char *val,int len);

unsigned char pop();
