class Master(Thread):
    def __init__(self, dirlist):
        super(Master, self).__init__()
        self.dirlist = dirlist
    def run(self):#重写父类run方法，在线程启动后执行该方法内的代码
       print 'running ...'
       pass
p = Master(xxx)
#p.daemon=True#设置为守护进程,主进程结束,子进程强制结束
p.start()
p.join()

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, self.counter, 5)
        print ("退出线程：" + self.name)
