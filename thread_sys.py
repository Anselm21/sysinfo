import psutil
import time
import config


class ThreadSys(object):

    def __init__(self):
        """ Constructor
        """
        self.tx_prev = 0
        self.rx_prev = 0
        self.tx_speed = 0
        self.rx_speed = 0
        self.cpu_used = 0
        self.memory_total = 0
        self.memory_used = 0
        self.run()

    @staticmethod
    def bytes_to_mb(bts):
        mb = bts / 1048576
        return float("{0:0.1f}".format(mb))

    @staticmethod
    def bytes_to_gib(bts):
        gib = bts / 1073741824
        return float("{0:0.1f}".format(gib))

    @staticmethod
    def get_bytes():
        network = psutil.net_io_counters()
        return {'bytes_sent': network.bytes_sent, 'bytes_recv': network.bytes_recv}

    def run(self):
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
        self.tx_prev = tx
        self.rx_prev = rx

    def get_info(self):
        return {
            'memory_total': self.memory_total,
            'memory_used': self.memory_used,
            'cpu_used': self.cpu_used,
            'rx_speed': self.rx_speed,
            'tx_speed': self.tx_speed,
            'server_name': config.SERVER_NAME,
            'time': time.strftime("%H:%M:%S", time.gmtime())
        }
