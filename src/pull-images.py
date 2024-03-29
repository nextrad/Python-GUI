import configparser
import subprocess
import sys
import time
import ast

nextrad_ini = 'gui_cfg.ini'
con_in = 'connections.ini'
while True:
    config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
    config.optionxform = lambda option: option  # preserve case for letters
    config.read(nextrad_ini)

    src = config.get('HeaderDirects','pentek_imgs')
    dest = config.get('HeaderDirects','save_imgs')

    src_n = config.get('HeaderDirects','gps_config')

    dest_n0 = config.get('HeaderDirects','gps0')
    dest_n1 = config.get('HeaderDirects','gps1')
    dest_n2 = config.get('HeaderDirects','gps2')

    image_poll_rate = int(config.get('Config','image_poll_rate'))

    config2 = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
    config2.optionxform = lambda option: option  # preserve case for letters
    config2.read(con_in)

    host_dict =  ast.literal_eval((config2.get('JSON','packet')))


    try:
        for host, data in host_dict.items():
            #print(host[:3], type(data['is_con']))
            if host[:3] == 'pen' and data['is_con'] == 1:
                print(host)
                subprocess.call('ansible ' + host + ' -m synchronize -a \"src=' + src +' dest=' + dest + ' mode=pull rsync_timeout=1\"',shell=True)

            if host == 'node0' and data['is_con'] == 1:
                print(host)
                subprocess.call('ansible ' + host + ' -m synchronize -a \"src=' + src_n +' dest=' + dest_n0 + '/gps_info.ini mode=pull rsync_timeout=1\"',shell=True)

            if host == 'node1' and data['is_con'] == 1:
                print(host)
                subprocess.call('ansible ' + host + ' -m synchronize -a \"src=' + src_n +' dest=' + dest_n1 + '/gps_info.ini mode=pull rsync_timeout=1\"',shell=True)

            if host == 'node2' and data['is_con'] == 1:
                print(host)
                subprocess.call('ansible ' + host + ' -m synchronize -a \"src=' + src_n +' dest=' + dest_n2 + '/gps_info.ini mode=pull rsync_timeout=1\"',shell=True)

        time.sleep(image_poll_rate)
    except KeyboardInterrupt:
        print('Exit Key!')
        sys.exit(0)


