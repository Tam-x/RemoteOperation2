from queue import Queue

class Log:
    log = None
    def __init__(self):
        pass
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_queue(self):
        if not self.log:
            self.log = Queue()
        return self.log

def put(info):
    l = Log()
    l.get_queue().put(str(info))