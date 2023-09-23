from threading import Thread
from time import sleep

class ThreadManager:
    def __init__(self, threads=None):
        self.threads = threads if threads is not None else []

    def add_thread(self, thread):
        self.threads.append(thread)

    def start(self):
        for thread in self.threads:
            thread.start()

    def start_and_join(self):
        for thread in self.threads:
            thread.start()
            thread.join()

    def start_with_sleep(self, secs=1):
        for thread in self.threads:
            thread.start()
            sleep(secs)

    def join(self):
        for thread in self.threads:
            thread.join()

    def get_len(self):
        return len(self.threads)

    def get_list_threads(self):
        return list(self.threads)

    def delete_all_threads(self):
        self.threads = []
