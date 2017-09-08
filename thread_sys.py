import time
import threading
import config
import os


class ThreadSys(object):

    def __init__(self, interval=1):
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
        self.last_worktime = 0
        self.last_idletime = 0

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    @staticmethod
    def bytes_to_mb(bts):
        mb = bts / 1048576
        return float("{0:0.1f}".format(mb))

    @staticmethod
    def bytes_to_gib(bts):
        gib = bts / 1073741824
        return float("{0:0.1f}".format(gib))

    @staticmethod
    def mb_to_gib(mb):
        gib = mb / 1024
        return float("{0:0.1f}".format(gib))

    # @staticmethod
    # def get_bytes():
    #     network = psutil.net_io_counters()
    #     return {'bytes_sent': network.bytes_sent, 'bytes_recv': network.bytes_recv}

    def get_cpu(self):
        f = open("/proc/stat", "r")
        line = ""
        while not "cpu " in line: line = f.readline()
        f.close()
        spl = line.split(" ")
        worktime = int(spl[2]) + int(spl[3]) + int(spl[4])
        idletime = int(spl[5])
        dworktime = (worktime - self.last_worktime)
        didletime = (idletime - self.last_idletime)
        rate = float(dworktime) / (didletime + dworktime)
        self.last_worktime = worktime
        self.last_idletime = idletime
        if (self.last_worktime == 0):
            result = 0
        else:
            result = float("%.2f" % round(rate,2))*100
        return result

    def run(self):
        """ Get sys info with 1s period """
        while True:
            tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
            self.cpu_used = self.get_cpu()
            self.memory_total = self.mb_to_gib(tot_m)
            self.memory_used = self.mb_to_gib(used_m)
            tx = 0
            rx = 0
            if self.tx_prev > 0:
                self.tx_speed = 0
            if self.rx_prev > 0:
                self.rx_speed = 0
            time.sleep(self.interval)
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
