from flask import Flask, request
import psutil
from tensorflow.python.client import device_lib

app = Flask(__name__)


@app.route('/')
def entry_page():
    cpu_used = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    memory_total = bytes_to_gib(memory.total)
    memory_used = bytes_to_gib(memory.used)
    gpus = get_available_gpus()
    return """
    CPU LOAD: {}% 
    TOTAL MEMORY: {} GiB  
    MEMORY USED: {} GiB 
    GPUs NUMBER: {} """.format(cpu_used, memory_total, memory_used, gpus)


def bytes_to_mb(bts):
    mb = bts/1048576
    return "{0:0.1f}".format(mb)


def bytes_to_gib(bts):
    gib = bts/1073741824
    return "{0:0.1f}".format(gib)


def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    gpus = [x.name for x in local_device_protos if x.device_type == 'GPU']
    return len(gpus)


if __name__ == '__main__':
    app.run(debug=True)


