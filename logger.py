import logging
import threading
import multiprocessing


class MultiprocessLogger(logging.Handler):
    def __init__(self, filename):
        logging.Handler.__init__(self)

        self._handler = logging.FileHandler(filename)
        self.queue = multiprocessing.Queue(-1)

        listener = threading.Thread(target=self.listen)
        listener.daemon = True
        listener.start()

    def setFormatter(self, fmt):
        logging.Handler.setFormatter(self, fmt)
        self._handler.setFormatter(fmt)

    def listen(self):
        while True:
            record = self.queue.get()
            self._handler.handle(record)

    def handle(self, record):
        self.queue.put(record)

    def close(self):
        self._handler.close()
        logging.Handler.close(self)
