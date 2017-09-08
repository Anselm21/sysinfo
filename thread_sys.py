import psutil
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
    def get_bytes():
        network = psutil.net_io_counters()
        return {'bytes_sent': network.bytes_sent, 'bytes_recv': network.bytes_recv}

    def run(self):
        """ Get sys info with 1s period """
        while True:
            mem = str(os.popen('free -t -m').readlines())
            """
            Get a whole line of memory output, it will be something like below
            ['             total       used       free     shared    buffers     cached\n', 
            'Mem:           925        591        334         14         30        355\n', 
            '-/+ buffers/cache:        205        719\n', 
            'Swap:           99          0         99\n', 
            'Total:        1025        591        434\n']
             So, we need total memory, usage and free memory.
             We should find the index of capital T which is unique at this string
            """
            T_ind = mem.index('T')
            """
            Than, we can recreate the string with this information. After T we have,
            "Total:        " which has 14 characters, so we can start from index of T +14
            and last 4 characters are also not necessary.
            We can create a new sub-string using this information
            """
            mem_G = mem[T_ind + 14:-4]
            """
            The result will be like
            1025        603        422
            we need to find first index of the first space, and we can start our substring
            from from 0 to this index number, this will give us the string of total memory
            """
            S1_ind = mem_G.index(' ')
            mem_Total = mem_G[0:S1_ind]
            """
                    Similarly we will create a new sub-string, which will start at the second value. 
                    The resulting string will be like
                    603        422
                    Again, we should find the index of first space and than the 
                    take the Used Memory and Free memory.
                    """
            mem_G1 = mem_G[S1_ind + 8:]
            S2_ind = mem_G1.index(' ')
            mem_Used = mem_G1[0:S2_ind]
            mem_Free = mem_G1[S2_ind + 8:]

            self.cpu_used =  CPU_Pct=str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2))
            memory = psutil.virtual_memory()
            self.memory_total = mem_Total
            self.memory_used = mem_Used
            tx = self.get_bytes()['bytes_sent']
            rx = self.get_bytes()['bytes_recv']

            if self.tx_prev > 0:
                self.tx_speed = self.bytes_to_mb(tx - self.tx_prev)

            if self.rx_prev > 0:
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
