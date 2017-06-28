from flask import Flask, request, jsonify
# from tensorflow.python.client import device_lib
from thread_sys import ThreadSys
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
sys_info = ThreadSys(socketio)


@app.route('/')
def entry_page():
    cpu_used = sys_info.cpu_used
    memory_total = sys_info.memory_total
    memory_used = sys_info.memory_used
    rx_speed = sys_info.rx_speed
    tx_speed = sys_info.tx_speed

    return """
    CPU LOAD: {}% 
    TOTAL MEMORY: {} GiB  
    MEMORY USED: {} GiB 
    RX_SPEED: {} Mbps
    TX_SPEED: {} Mbps""".format(cpu_used, memory_total, memory_used, rx_speed, tx_speed)

#
# def get_available_gpus():
#     local_device_protos = device_lib.list_local_devices()
#     gpus = [x.name for x in local_device_protos if x.device_type == 'GPU']
#     return len(gpus)

if __name__ == '__main__':
    socketio.run(app, debug=True)


