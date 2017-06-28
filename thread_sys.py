import psutil
import time
import threading


class ThreadSys(object):

    def __init__(self, socket, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check sys params interval, in seconds
        """
        self.interval = interval
        self.tx_prev = 0
        self.rx_prev = 0
        self.tx_speed = 0
        self.rx_speed = 0
        self.cpu_used = 0
        self.memory_total = 0
        self.memory_used = 0
        self.socket_io = socket

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    @staticmethod
    def bytes_to_mb(bts):
        mb = bts / 1048576
        return "{0:0.1f}".format(mb)

    @staticmethod
    def bytes_to_gib(bts):
        gib = bts / 1073741824
        return "{0:0.1f}".format(gib)

    @staticmethod
    def get_bytes():
        network = psutil.net_io_counters()
        return {'bytes_sent': network.bytes_sent, 'bytes_recv': network.bytes_recv}

    def some(self):
        self.socket_io.emit('some_event', {'data': 42})

    def run(self):
        """ Get sys info with 1s period """
        while True:
            self.cpu_used = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            self.memory_total = self.bytes_to_gib(memory.total)
            self.memory_used = self.bytes_to_gib(memory.used)
            tx = self.get_bytes()['bytes_sent']
            rx = self.get_bytes()['bytes_recv']

            if self.tx_prev > 0:
                self.tx_speed = self.bytes_to_mb(tx - self.tx_prev)

            if self.rx_prev > 0:
                self.rx_speed = self.bytes_to_mb(rx - self.rx_prev)
            self.some()
            time.sleep(self.interval)

            self.tx_prev = tx
            self.rx_prev = rx
