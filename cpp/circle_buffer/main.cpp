#include <cstdio>
#include <memory>
#include <mutex>

typedef float T;
class circular_buffer {
    public:
	
	float *buf_;
	size_t head_ = 0;
	size_t tail_ = 0;
	size_t max_size_;
	bool full_ = 0;
public:
	explicit circular_buffer(size_t size)
	{
        buf_ = new T[size];
		max_size_ = size;
	}

	void put(T item)
	{
		buf_[head_] = item;

		if(full_)
		{
			tail_ = (tail_ + 1) % max_size_;
		}

		head_ = (head_ + 1) % max_size_;
		full_ = head_ == tail_;
	}

	T get()
	{
		if(empty())
		{
			return T();
		}
		//Read data and advance the tail (we now have a free space)
		auto val = buf_[tail_];
		full_ = false;
		tail_ = (tail_ + 1) % max_size_;
		return val;
	}
    void print(){
        for(int i=0;i<this->size();i++){
            printf("i:%d,val:%f\n", i,buf_[(tail_+i)%max_size_]);
        }
    }
	void reset()
	{
		head_ = tail_;
		full_ = false;
	}

	bool empty() const
	{
		//if head and tail are equal, we are empty
		return (!full_ && (head_ == tail_));
	}

	bool full() const
	{
		//If tail is ahead the head by 1, we are full
		return full_;
	}

	size_t capacity() const
	{
		return max_size_;
	}

	size_t size() const
	{
		size_t size = max_size_;

		if(!full_)
		{
			if(head_ >= tail_)
			{
				size = head_ - tail_;
			}
			else
			{
				size = max_size_ + head_ - tail_;
			}
		}
		return size;
	}
};

int main(void)
{
	circular_buffer circle(5);
    int x;
	printf("Adding %d values\n", circle.capacity() );
	for(uint32_t i = 0; i < circle.capacity(); i++)
	{
		circle.put(i);
	}
    circle.print();

    x = 10;
	printf("Put %d\n", x);
	circle.put(x);
	
	x = 12;
	printf("Put %d\n", x);
	circle.put(x);
	
    circle.print();

	return 0;
}
