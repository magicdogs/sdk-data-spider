import queue
import _thread
import threading
import time


class FixThreadPool:

    def __init__(self):
        self.job_queue = queue.Queue(100)
        self.thread_max_size = 10
        self.state = 0
        for i in range(0, self.thread_max_size):
            QueueThread("Thread-" + str(i), self).start()

    def shutdown(self):
        print("shutdown fixed thread_pool")
        self.state = 1


class QueueThread (threading.Thread):

    def __init__(self, tid, pool):
        threading.Thread.__init__(self)
        self.name = tid
        self.pool = pool
        self.task_queue = pool.job_queue

    def run(self):
        print("Starting " + self.name)
        while self.pool.state == 0:
            try:
                task = self.task_queue.get(True, 0.2)
                func = task[0]
                args = task[1]
                if func is not None:
                    print(threading.current_thread().name + " start new task: " + str(args))
                    func(args)
                self.task_queue.task_done()
            except queue.Empty as e:
                pass
            except Exception as e:
                self.task_queue.task_done()

        print("Exiting " + self.name)


total = 0
lock = threading.Lock()


# _thread.start_new_thread(run_able, (("aaa"),))
def run_able(name):
    global total
    lock.acquire()
    total = total + 1
    lock.release()
    print(threading.current_thread().name + str(name))


# thread_pool = FixThreadPool()
# count = 0
# while True:
#     count = count + 1
#     thread_pool.job_queue.put((run_able, ({"a": "b", "c": 2})))
#     if count > 9999:
#         break
#
# thread_pool.job_queue.join()
# thread_pool.shutdown()
# print(total)
