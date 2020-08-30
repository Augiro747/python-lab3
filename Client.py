import socket
import psutil
import time
import configparser

def get_config():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 6050))
    res=sock.recv(4096)
    sock.close()
    return res.decode('utf-8')

def config_read():
    config = configparser.ConfigParser()
    config.read("config.ini")
    server_ip = config['config'].get('address')
    server_port = config['config'].get('port')
    timeout = config['config'].get('timeout')
    print(server_ip, int(server_port), int(timeout))
    return server_ip, int(server_port), int(timeout)

def get_processor_info():
    processor = (psutil.cpu_percent(interval=1))
    print(processor)
    return processor

def get_memory_info():
    av_mem=(psutil.virtual_memory())
    gb=1024.0 ** 3
    print(round(av_mem.available/gb))
    return round(av_mem.available/gb)

def get_free_space():
    disk=psutil.disk_usage("/")
    gb=1024.0 ** 3
    print(round(disk.free/gb,3))
    return round(disk.free/gb,3)

def get_procs_count():
    quantity = 0
    for _ in psutil.process_iter():
        quantity += 1
    print(quantity)
    return quantity

def get_users_list():
    users = len(psutil.users())
    print(users)
    return users

def transmit(ip,port):
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    msg='cpu '+str(get_processor_info())+'%|mem '+str(get_memory_info())+'Gb|free '+str(get_free_space())+'Gb|proc '+str(get_procs_count())+' |usrs '+str(get_users_list())+' | '+str(time.strftime('%X'))
    sock.send(msg.encode('utf-8'))
    sock.close()

f=open("config.ini","w")
f.write(get_config())
f.close()
ip,port,timer=config_read()
while True:
    transmit(ip,port)
    time.sleep(timer)