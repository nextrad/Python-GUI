from suitable import Api
from getpass import getpass
import time
import configparser
import subprocess
import ast
import signal


def create_host_dict():
    adjust_ini = 'connections.ini'
    config = configparser.ConfigParser()
    config.read(adjust_ini)


    hosts = config.items('Hosts')

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

    return host_dict, config, adjust_ini


def handler(signum, frame):
    print('Timeout Occured')
    raise Exception('Timeout Period Reached')

signal.signal(signal.SIGALRM, handler)

while True:
    signal.alarm(3)
    subprocess.call(['rm -r ~/.ansible/cp/'],shell=True)

    host_dict, config, adjust_ini = create_host_dict()
    api_dict = {}

    for k,v in host_dict.items():

        api_dict.update({k:Api(host_dict[k]['ip'],extra_vars={'ansible_user':host_dict[k]['user'],'ansible_connection': 'ssh','ansible_password':host_dict[k]['pswd']})})
    #print(host_dict)
    #print(api_dict)
    for k,v in api_dict.items():

        try:
            result = api_dict[k].ping()
            #print(result['contacted'][host_dict[k]['ip']]['ping'])
            config['Hosts'][k] = '\'' + host_dict[k]['user'] + '\',\'' + str(host_dict[k]['ip']) + '\',\'' + str(host_dict[k]['pswd']) + '\',1'
            print(result)
        except:
            print('Failed to connect:' + k)
            config['Hosts'][k] = '\'' + host_dict[k]['user']+ '\',\''  + str(host_dict[k]['ip']) + '\',\'' + str(host_dict[k]['pswd']) + '\',0'
            #print(Exception)
        signal.alarm(3)

    config['JSON']['packet'] = str(host_dict)

    with open(adjust_ini,'w') as configfile:
            config.write(configfile)


