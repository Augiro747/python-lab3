import socket
import psutil
import time
import configparser

def get_config():
    """get config from server(default port 6050)"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 6050))
    res=sock.recv(4096)
    sock.close()
    return res.decode('utf-8')

def config_read():
    """Read config file and take configs data for work"""
    config = configparser.ConfigParser()
    config.read("config.ini")
    server_ip = config['config'].get('address')
    server_port = config['config'].get('port')
    timeout = config['config'].get('timeout')
    print(server_ip, int(server_port), int(timeout))
    return server_ip, int(server_port), int(timeout)

def get_processor_info():
    """Return a float representing the current system-wide CPU utilization as a percentage."""
    processor = (psutil.cpu_percent(interval=1))
    print(processor)
    return processor

def get_memory_info():
    """Return statistics about system memory usage"""
    av_mem=(psutil.virtual_memory())
    gb=1024.0 ** 3
    print(round(av_mem.available/gb))
    return round(av_mem.available/gb)

def get_free_space():
    """Return free disk space Gb count"""
    disk=psutil.disk_usage("/")
    gb=1024.0 ** 3
    print(round(disk.free/gb,3))
    return round(disk.free/gb,3)

def get_procs_count():
    """Return count of active processes"""
    quantity = 0
    for _ in psutil.process_iter():
        quantity += 1
    print(quantity)
    return quantity

def get_users_list():
    """Return list of active users count"""
    users = len(psutil.users())
    print(users)
    return users

def transmit(ip,port):
    """Transmitting data as string to server throught tcp"""
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    msg='cpu '+str(get_processor_info())+'%|mem '+str(get_memory_info())+'Gb|free '+str(get_free_space())+'Gb|proc '+str(get_procs_count())+' |usrs '+str(get_users_list())+' | '+str(time.strftime('%X'))
    sock.send(msg.encode('utf-8'))
    sock.close()

if __name__=="__main__"
    f=open("config.ini","w")
    f.write(get_config())
    f.close()
    ip,port,timer=config_read()
    while True:
        transmit(ip,port)
        time.sleep(timer)