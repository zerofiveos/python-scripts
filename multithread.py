import threading
import time
import sched

s = sched.scheduler(time.time, time.sleep)

def print1():
    print 'Thread 1 Start'
    time.sleep(5)
    print 'Thread 1 End'
    return

def print2():
    print 'Thread 2 Start'
    time.sleep(2)
    print 'Thread 2 End'
    s.enter(1, 1, print2, ())
    return

t1 = threading.Thread(name="t1",target=print1)
t2 = threading.Thread(name="t2",target=print2)

t1.start()
#t2.start()
s.enter(1, 1, print2, ())
s.run()

time.sleep(60)
