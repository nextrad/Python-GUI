from suitable import Api
from getpass import getpass
import time
import configparser
import subprocess
import ast
import signal
import os
import sys


def create_host_dict():
    adjust_ini = 'connections.ini'
    config = configparser.ConfigParser()
    config.read(adjust_ini)


    hosts = config.items('Hosts')
    ping_count = config.get('Config','ping_count')
    timeout = config.get('Config','timeout')
    poll_rate = config.get('Config','poll_rate')

    host_dict = {}
    for item in hosts:
        host_dict.update({item[0] : item[1]})

    for k,v in host_dict.items():
        host_dict[k] = v.split(',')
        host_dict[k][0] = '{\'user\':' + host_dict[k][0]
        host_dict[k][1] = ',\'ip\':' + host_dict[k][1]
        host_dict[k][2] = ',\'pswd\':' + host_dict[k][2]
        host_dict[k][3] = ',\'is_con\':' + host_dict[k][3]+ '}'
        host_dict[k] = ''.join(host_dict[k])
        host_dict[k] = ast.literal_eval(host_dict[k])

    return host_dict, config, adjust_ini, ping_count, timeout, poll_rate


def handler(signum, frame):
    print('Timeout Occured')
    raise Exception('Timeout Period Reached')

signal.signal(signal.SIGALRM, handler)

while True:
    #signal.alarm(3)

    host_dict, config, adjust_ini, ping_count, timeout, poll_rate = create_host_dict()

    for hostname,data in host_dict.items():
        try:
            response = os.system('ping -c ' + ping_count + ' -W ' + timeout + ' ' + data['ip'])
            if response == 0:
                config['Hosts'][hostname] = '\'' + host_dict[hostname]['user'] + '\',\'' + str(host_dict[hostname]['ip']) + '\',\'' + str(host_dict[hostname]['pswd']) + '\',1'
                print(hostname + ' is up!')
            else:
                config['Hosts'][hostname] = '\'' + host_dict[hostname]['user']+ '\',\''  + str(host_dict[hostname]['ip']) + '\',\'' + str(host_dict[hostname]['pswd']) + '\',0'
                print(hostname + ' is down!')
            config['JSON']['packet'] = str(host_dict)

            with open(adjust_ini,'w') as configfile:
                    config.write(configfile)
            time.sleep(float(poll_rate))
        except KeyboardInterrupt:
            print('Exit Key!')
            sys.exit(0)
