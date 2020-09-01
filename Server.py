import socket
import time
import configparser

def config_set():
    """Creates config file if it does not exist and return config data"""
    config = configparser.ConfigParser()
    try:
        file=open('configServ.ini')
        file.close()
        config.read("configServ.ini")
        server_ip=config['config'].get('address')
        server_port = config['config'].get('port')
        timeout = config['config'].get('timeout')
    except IOError:
        file = open('configServ.ini','w')
        file.close()
        config.add_section("config")
        config.set('config', 'address', str(socket.gethostbyname(socket.getfqdn())))
        config.set('config', 'port', str(6050))
        config.set('config', 'timeout', str(20))
        with open('configServ.ini', 'w') as configfile:
            config.write(configfile)
        config.read("configServ.ini")
        server_ip = config['config'].get('address')
        server_port = config['config'].get('port')
        timeout = config['config'].get('timeout')
    return server_ip, int(server_port), int(timeout)

def conf_send(onip,port,timeout):
    """Sending clients config to client"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    confmsg='[config]\naddress = '+str(socket.gethostbyname(socket.getfqdn()))+'\nport = '+str(port)+'\ntimeout = '+str(timeout)
    sock.sendto(confmsg.encode('utf-8'), (onip, port))
    print(str(socket.gethostbyname(socket.getfqdn())))

def ipl_change(ipl):
    """IP list of clients in program changing"""
    nipl=[]
    f = open("iplist.txt", 'r')
    f.seek(0)
    for line in f:
        nipl.append(line[0:len(line)-1])
    if len(nipl)>len(ipl):
        ipl=nipl
    f.close()
    return ipl

if __name__='__main__'
    ip,port,timeout=config_set()
    iplist=[]
    liplist=0
    t=time.time()
    file=open("monitor.txt","w")
    file.close()
    try:
        file=open("iplist.txt")
        file.close()
    except IOError:
        file = open("iplist.txt","w")
        file.close()
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(2)
    while True:
        if time.time()>t+5:
            t=time.time()
            iplist=ipl_change(iplist)
            while liplist<len(iplist):
                conf_send(iplist[liplist],port,timeout)
                liplist=liplist+1
            print('t changed')
            print(str(liplist)+"/"+str(len(iplist)))
        if liplist>0:
            try:
                client, addr=sock.accept()
            except KeyboardInterrupt:
                sock.close()
                break
            else:
                res=client.recv(4096)
                client.close()
                file=open("monitor.txt","a")
                file.write(res.decode('utf-8')+'\n')
                file.close()
