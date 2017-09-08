from __future__ import division
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
        return float("{0:.2f}".format(mb))

    @staticmethod
    def bytes_to_gib(bts):
        gib = bts / 1073741824
        return float("{0:0.1f}".format(gib))

    @staticmethod
    def mb_to_gib(mb):
        gib = mb / 1024
        return float("{0:0.1f}".format(gib))

    @staticmethod
    def get_network_bytes(interface):
        for line in open('/proc/net/dev', 'r'):
            if interface in line:
                data = line.split('%s:' % interface)[1].split()
                rx_bytes, tx_bytes = (data[0], data[8])
                return (int(rx_bytes), int(tx_bytes))

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
            try:
                rx, tx = self.get_network_bytes('eth0')
            except:
                rx = 0
                tx = 0
            tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
            self.cpu_used = self.get_cpu()
            self.memory_total = self.mb_to_gib(tot_m)
            self.memory_used = self.mb_to_gib(used_m)
            if int(self.tx_prev) > 0:
                self.tx_speed = self.bytes_to_mb(tx - self.tx_prev)
            if int(self.rx_prev) > 0:
                self.rx_speed = self.bytes_to_mb(rx - self.rx_prev)
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
