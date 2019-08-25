
import datetime
from io import StringIO
import sys
import signal
import time
import os
import configparser
from subprocess import call
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from threading import Thread
import sys, getopt
import subprocess
import ast
import re
from shutil import copyfile
from suitable import Api
from getpass import getpass

from suitable import Api
from getpass import getpass

from PyQt5 import Qt, QtWidgets, QtCore, QtGui, QtWebEngine, QtWebEngineWidgets, QtWebEngineWidgets

class Worker(QtCore.QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                        kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    #@pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)

class Plot():
    def __init__(self):
        self.name = 'Quickview Plot'

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args,**kwargs)

        gui_ini = 'gui_cfg.ini'
        config = configparser.ConfigParser()
        config.read(gui_ini)
        self.stdout_result = StringIO()

        self.nextrad_ini = config.get('Files','nextrad_header')
        self.connections_ini = config.get('Files','connection')
        self.cnc_header_loc = config.get('HeaderDirects','cnc')
        self.experiment_log_file = config.get('Files','log_file')
        self.node_header_dir = config.get('HeaderDirects','nodes')
        self.pentek_header_dir = config.get('HeaderDirects','penteks')
        self.rhino_header_dir = config.get('HeaderDirects','rhinos')
        self.gpsdo_header_dir = config.get('HeaderDirects','gpsdos')

        print('NeXtRAD Header: ' + self.nextrad_ini)

        #State Flags
        self.current_time = 0
        self.stop_timer = 0
        self.ansi_running = 0
        self.time_running = 0
        self.remaining_time = 0
        self.experiment_running = 0
        self.time_remaining = 0
        self.plot_is_active = 0
        self.save_scene_check = 0
        self.num_pri = 0
        self.pent_zero_include = 0
        self.rhino_zero_include = 0
        self.node_zero_include = 0
        self.pent_one_include = 0
        self.rhino_one_include = 0
        self.node_one_include = 0
        self.pent_two_include = 0
        self.rhino_two_include = 0
        self.node_two_include = 0
        #Initialisers
        self.node_1_latlong = '0,0'
        self.node_2_latlong = '0,0'
        self.node_0_latlong = '0,0'
        self.target_latlong = '0,0'
        self.target_name = ''
        #nodes
        self.node0_location_name = ''
        self.node0_location_name = ''
        self.node0_location_name = ''
        self.experiment_name = ''
        self.target_description = ''

        self.create_host_dict()

        #Radar Parameters
        self.start_time = 0
        self.pri = 0
        self.num_pri = 0
        self.bands = ''
        self.pols = ''

        #Start the Threadpool
        self.threadpool = QtCore.QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


        layout = QtWidgets.QGridLayout()

        #GUI Text
        self.lbl_experi_name = QtWidgets.QLabel('Experiment Description:')
        self.lbl_trgt_latlong = QtWidgets.QLabel('Target (Lat,Long):')
        self.lbl_scene = QtWidgets.QLabel('Scene Notes:')
        self.lbl_timer = QtWidgets.QLabel('0')
        self.lbl_cnc = QtWidgets.QLabel('CNC')
        self.pent_zero = QtWidgets.QLabel('Pentek 0')
        self.pent_one = QtWidgets.QLabel('Pentek 1')
        self.pent_two = QtWidgets.QLabel('Pentek 2')
        self.rhino_zero = QtWidgets.QLabel('Rhino 0')
        self.rhino_one = QtWidgets.QLabel('Rhino 1')
        self.rhino_two = QtWidgets.QLabel('Rhino 2')
        self.node_zero = QtWidgets.QLabel('Node 0')
        self.node_one = QtWidgets.QLabel('Node 1')
        self.node_two = QtWidgets.QLabel('Node 2')
        self.lbl_cnc = QtWidgets.QLabel('CNC')
        self.lbl_ntp = QtWidgets.QLabel('NTP')

        #Pushbuttons
        self.run_button = QtWidgets.QPushButton('Run')
        self.abort_button = QtWidgets.QPushButton('Quickview')
        self.run_button.clicked.connect(self.run_experiment)
        self.abort_button.clicked.connect(self.run_quickview)
        self.target_accept = QtWidgets.QPushButton('Enter Details')
        self.description_accept = QtWidgets.QPushButton('Enter Details')
        self.scene_accept = QtWidgets.QPushButton('Enter Details')
        self.target_accept.clicked.connect(self.enter_target_details)
        self.description_accept.clicked.connect(self.enter_description)
        self.pulses_button = QtWidgets.QPushButton('Pulses')
        #Textboxes
        self.target_details = QtWidgets.QLineEdit(self)
        self.target_details.editingFinished.connect(self.enter_target_details)
        self.experiment_name_edit = QtWidgets.QLineEdit(self)
        self.experiment_name_edit.editingFinished.connect(self.enter_scene)
        self.scene_edit = QtWidgets.QLineEdit(self)
        #self.scene_edit.editingFinished.connect(self.enter_scene)

        #Checkboxes
        self.node_0_disable = QtWidgets.QCheckBox("Node 0",self)
        self.node_0_disable.stateChanged.connect(self.disable_node0)
        self.node_1_disable = QtWidgets.QCheckBox("Node 1",self)
        self.node_1_disable.stateChanged.connect(self.disable_node1)
        self.node_2_disable = QtWidgets.QCheckBox("Node 2",self)
        self.node_2_disable.stateChanged.connect(self.disable_node2)
        #Connection Stats
        #Penteks
        # self.pent_1 = QLabel('Pentek 0')
        # self.pent_2 = QLabel('Pentek 0')

        #Layout Setup

        self.view = QtWebEngineWidgets.QWebEngineView()

# load .html file
        self.view.load(QtCore.QUrl.fromLocalFile(os.path.abspath('map.html')))


        layout.addWidget(self.lbl_timer,0,1,1,3)
        #layout.addWidget(self.text,0,0,1,2)

        layout.addWidget(self.run_button,2,0)
        layout.addWidget(self.abort_button,3,0)
        layout.addWidget(self.pulses_button,4,0)

        layout.addWidget(self.lbl_experi_name,1,1)
        layout.addWidget(self.experiment_name_edit,1,2)
        layout.addWidget(self.description_accept,1,3)

        layout.addWidget(self.view,2,1,15,3)

        layout.addWidget(self.target_details,17,2)
        layout.addWidget(self.lbl_trgt_latlong,17,1)
        layout.addWidget(self.target_accept,17,3)

        layout.addWidget(self.lbl_scene,18,1)
        layout.addWidget(self.scene_edit,18,2,1,2)
        #layout.addWidget(self.scene_accept,18,3)

        layout.addWidget(self.lbl_cnc,1,4)
        layout.addWidget(self.lbl_ntp,2,4)

        layout.addWidget(self.node_0_disable,3,4)
        layout.addWidget(self.pent_zero,4,4)
        layout.addWidget(self.node_zero,5,4)
        layout.addWidget(self.rhino_zero,6,4)

        layout.addWidget(self.node_1_disable,7,4)
        layout.addWidget(self.pent_one,8,4)
        layout.addWidget(self.node_one,9,4)
        layout.addWidget(self.rhino_one,10,4)

        layout.addWidget(self.node_2_disable,11,4)
        layout.addWidget(self.pent_two,12,4)
        layout.addWidget(self.node_two,13,4)
        layout.addWidget(self.rhino_two,14,4)


        w = QtWidgets.QWidget()
        w.setLayout(layout)

        state_update = Worker(self.check_state)
        self.threadpool.start(state_update)

        self.setCentralWidget(w)
        self.init_nextheader_values()
        self.init_map()
        self.target_details.setText(self.target_latlong)
        self.experiment_name_edit.setText(self.experiment_name)

        self.show()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_state)
        self.timer.start(500)

    def init_nextheader_values(self):
        config = configparser.ConfigParser()
        config.read(self.nextrad_ini)
        self.node_0_latlong = config.get('GeometrySettings','node0_location_lat')+','+config.get('GeometrySettings','node0_location_lon')
        self.node_1_latlong = config.get('GeometrySettings','node1_location_lat')+','+config.get('GeometrySettings','node1_location_lon')
        self.node_2_latlong = config.get('GeometrySettings','node2_location_lat')+','+config.get('GeometrySettings','node2_location_lon')
        self.target_latlong = config.get('TargetSettings','tgt_location_lat')+','+config.get('TargetSettings','tgt_location_lon')

        self.experiment_name = config.get('Notes','experiment_name')
        self.target_description = config.get('Notes','experiment_notes')

        self.num_pri = int(config.get('PulseParameters','num_pris'))
        self.pulses = config.get('PulseParameters','pulses')
        pulses = self.pulses.split(',')
        self.pri = float(pulses[1])
        self.time_remaining = self.pri*self.num_pri #In microseconds
        self.pols = int(pulses[2])
        self.bands = float(pulses[3].replace('\"',''))
        self.pulse_width = float(pulses[0].replace('\"',''))

    def init_map(self):
        self.update_map('var n0 = ','var n0 = [' + self.node_0_latlong + '];\n')
        self.update_map('var n1 = ','var n1 = [' + self.node_1_latlong + '];\n')
        self.update_map('var n2 = ','var n2 = [' + self.node_2_latlong + '];\n')

    def create_valid_hosts(self):
        self.valid_hosts = {}
        self.valid_nodes = {}
        self.valid_penteks = {}
        self.valid_rhinos = {}
        self.valid_runnable_nodes = {}

        for h,d in self.host_dict.items():
            if d['is_con'] == 1:
                self.valid_hosts.update({h:d})

        for k,v in self.valid_hosts.items():
            if (k == 'node0') and (self.node_zero_include == 1):
                self.valid_nodes.update({k:v})
            if (k == 'node1') and (self.node_one_include == 1):
                self.valid_nodes.update({k:v})
            if (k == 'node2') and (self.node_two_include == 1):
                self.valid_nodes.update({k:v})

            if (k == 'pentek0') and (self.pent_zero_include == 1):
                self.valid_penteks.update({k:v})
            if (k == 'pentek1') and (self.pent_one_include == 1):
                self.valid_penteks.update({k:v})
            if (k == 'pentek2') and (self.pent_two_include == 1):
                self.valid_penteks.update({k:v})

            if (k == 'rhino0') and (self.rhino_zero_include == 1):
                self.valid_rhinos.update({k:v})
            if (k == 'rhino1') and (self.rhino_one_include == 1):
                self.valid_rhinos.update({k:v})
            if (k == 'rhino2') and (self.rhino_two_include == 1):
                self.valid_rhinos.update({k:v})

            self.valid_runnable_nodes = {}
            #print(self.valid_nodes, self.valid_penteks, self.valid_rhinos)

    def disable_node0(self,state):
        if self.node_0_disable.isChecked():
            self.pent_zero_include = 1
            self.rhino_zero_include = 1
            self.node_zero_include = 1

        else:
            self.pent_zero_include = 0
            self.rhino_zero_include = 0
            self.node_zero_include = 0

    def disable_node1(self,state):
        if self.node_1_disable.isChecked():
            self.pent_one_include = 1
            self.rhino_one_include = 1
            self.node_one_include = 1
        else:
            self.pent_one_include = 0
            self.rhino_one_include = 0
            self.node_one_include = 0

    def disable_node2(self,state):
        if self.node_2_disable.isChecked():
            self.pent_two_include = 1
            self.rhino_two_include = 1
            self.node_two_include = 1

        else:
            self.pent_two_include = 0
            self.rhino_two_include = 0
            self.node_two_include = 0

    def create_host_dict(self):
        config = configparser.ConfigParser()
        config.read(self.connections_ini)

        hosts = config.items('Hosts')

        self.host_dict = {}

        for item in hosts:
            self.host_dict.update({item[0] : item[1]})

        for k,v in self.host_dict.items():
            host_dict = self.host_dict
            host_dict[k] = v.split(',')
            host_dict[k][0] = '{\'user\':' + host_dict[k][0]
            host_dict[k][1] = ',\'ip\':' + host_dict[k][1]
            host_dict[k][2] = ',\'pswd\':' + host_dict[k][2]
            host_dict[k][3] = ',\'is_con\':' + host_dict[k][3]+ '}'
            host_dict[k] = ''.join(host_dict[k])
            host_dict[k] = ast.literal_eval(host_dict[k])
        self.host_dict = host_dict
        self.create_valid_hosts()

    def check_state(self):

        self.create_host_dict()

        if self.time_running == 0 and self.experiment_running == 0:
            self.lbl_timer.setText('Not Running')
            self.lbl_timer.setStyleSheet('color: black')
            self.run_button.setStyleSheet("background-color: green")
        elif self.time_running == 1 and self.experiment_running == 0:
            self.lbl_timer.setStyleSheet('color: red')
            self.run_button.setStyleSheet("background-color: red")
        else:
            self.lbl_timer.setStyleSheet('color: green')
            self.run_button.setStyleSheet("background-color: red")

        try:
            self.lbl_cnc.setText('CNC')
            if self.host_dict['cnc']['is_con'] == 0:
                self.lbl_cnc.setStyleSheet('color: red')
            else:
                self.lbl_cnc.setStyleSheet('color: green')
        except:
            self.lbl_cnc.setStyleSheet('color: gray')
            self.lbl_cnc.setText('Missing config')
        try:
            self.lbl_ntp.setText('NTP')
            if self.host_dict['ntp']['is_con'] == 0:
                self.lbl_ntp.setStyleSheet('color: red')
            else:
                self.lbl_ntp.setStyleSheet('color: green')
        except:
            self.lbl_ntp.setStyleSheet('color: gray')
            self.lbl_ntp.setText('Missing config')
        try:
            self.pent_zero.setText('Pentek 0')
            if self.host_dict['pentek0']['is_con'] == 0 and self.pent_zero_include == 1:
                self.pent_zero.setStyleSheet('color: red')
            elif self.host_dict['pentek0']['is_con'] == 1 and self.pent_zero_include == 1:
                self.pent_zero.setStyleSheet('color: green')
            else:
                self.pent_zero.setStyleSheet('color: gray')
        except:
            self.pent_zero.setStyleSheet('color: gray')
            self.pent_zero.setText('Missing config')
        try:
            self.pent_one.setText('Pentek 1')
            if self.host_dict['pentek1']['is_con'] == 0 and self.pent_one_include == 1:
                self.pent_one.setStyleSheet('color: red')
            elif self.host_dict['pentek1']['is_con'] == 1 and self.pent_one_include == 1:
                self.pent_one.setStyleSheet('color: green')
            else:
                self.pent_one.setStyleSheet('color: gray')
        except:
            self.pent_one.setStyleSheet('color: gray')
            self.pent_one.setText('Missing config')
        try:
            self.pent_two.setText('Pentek 2')
            if self.host_dict['pentek2']['is_con'] == 0 and self.pent_two_include == 1:
                self.pent_two.setStyleSheet('color: red')
            elif self.host_dict['pentek2']['is_con'] == 1 and self.pent_two_include == 1:
                self.pent_two.setStyleSheet('color: green')
            else:
                self.pent_two.setStyleSheet('color: gray')
        except:
            self.pent_two.setStyleSheet('color: gray')
            self.pent_two.setText('Missing config')
        try:
            self.node_zero.setText('Node 0')
            if self.host_dict['node0']['is_con'] == 0 and self.node_zero_include == 1:
                self.node_zero.setStyleSheet('color: red')
            elif self.host_dict['node0']['is_con'] == 1 and self.node_zero_include == 1:
                self.node_zero.setStyleSheet('color: green')
            else:
                self.node_zero.setStyleSheet('color: gray')
        except:
            self.node_zero.setStyleSheet('color: gray')
            self.node_zero.setText('Missing config')

        try:
            self.node_one.setText('Node 1')
            if self.host_dict['node1']['is_con'] == 0 and self.node_one_include == 1:
                self.node_one.setStyleSheet('color: red')
            elif self.host_dict['node1']['is_con'] == 1 and self.node_one_include == 1:
                self.node_one.setStyleSheet('color: green')
            else:
                self.node_one.setStyleSheet('color: gray')
        except:
            self.node_one.setStyleSheet('color: gray')
            self.node_one.setText('Missing config')
        try:
            self.node_two.setText('Node 2')
            if self.host_dict['node2']['is_con'] == 0 and self.node_two_include == 1:
                self.node_two.setStyleSheet('color: red')
            elif self.host_dict['node2']['is_con'] == 1 and self.node_two_include == 1:
                self.node_two.setStyleSheet('color: green')
            else:
                self.node_two.setStyleSheet('color: gray')
        except:
            self.node_two.setStyleSheet('color: gray')
            self.node_two.setText('Missing config')
        try:
            self.rhino_zero.setText('Rhino 0')
            if self.host_dict['rhino0']['is_con'] == 0 and self.rhino_zero_include == 1:
                self.rhino_zero.setStyleSheet('color: red')
            elif self.host_dict['rhino0']['is_con'] == 1 and self.rhino_zero_include == 1:
                self.rhino_zero.setStyleSheet('color: green')
            else:
                self.rhino_zero.setStyleSheet('color: gray')
        except:
            self.rhino_zero.setStyleSheet('color: gray')
            self.rhino_zero.setText('Missing config')
        try:
            self.rhino_one.setText('Rhino 1')
            if self.host_dict['rhino0']['is_con'] == 0 and self.rhino_one_include == 1:
                self.rhino_one.setStyleSheet('color: red')
            elif self.host_dict['rhino0']['is_con'] == 1 and self.rhino_one_include == 1:
                self.rhino_one.setStyleSheet('color: green')
            else:
                self.rhino_one.setStyleSheet('color: gray')
        except:
            self.rhino_one.setStyleSheet('color: gray')
            self.rhino_one.setText('Missing config')
        try:
            self.rhino_two.setText('Rhino 2')
            if self.host_dict['rhino2']['is_con'] == 0 and self.rhino_two_include == 1:
                self.rhino_two.setStyleSheet('color: red')
            elif self.host_dict['rhino2']['is_con'] == 1 and self.rhino_two_include == 1:
                self.rhino_two.setStyleSheet('color: green')
            else:
                self.rhino_two.setStyleSheet('color: gray')
        except:
            self.rhino_two.setStyleSheet('color: gray')
            self.rhino_two.setText('Missing config')

    def run_quickview(self):
        if self.plot_is_active == 1:
            subprocess.call('python3 plottty.py &',shell=True)

    def abort_experiment(self):
        print('Aborting Experiment!')
        self.time_running = 0
        self.time_remaining = 0
        self.experiment_running = 0
        self.ansi_running = 0
        self.ansi_shell_command(self.valid_nodes,'echo did this work')
        self.run_button.setText('Run')

    def enter_target_details(self):
        if self.target_details.text() != '':
            self.target_latlong = self.target_details.text()
            self.update_map('var trgt = ','var trgt = [' + self.target_latlong + '];\n')
            print('Target Details Updated')
        else:
            print('Please Enter Valid Address as Lat, Long')

    def enter_scene(self):
        print('Scene description added to excel file')

    def enter_description(self):
        ini_file = self.nextrad_ini
        config = configparser.ConfigParser()
        config.read(ini_file)

        if self.experiment_name_edit.text() != '':
            config['Notes']['experiment_name'] = self.experiment_name_edit.text()
            print('Description Set')

        else:
            print('Nothing Entered, Using Default \'No Description\'')
            config['Notes']['experiment_name'] = 'No Description'

        with open(self.nextrad_ini,'w') as configfile:
            config.write(configfile)

    def update_map(self,textin,replace):

        copyfile('map.js', 'map_backup.js')
        with open('map.js') as fin, open('map_temp.js', 'w') as fout:
            for line in fin:
                if textin in line:
                    line = replace

                fout.write(line)

        os.rename('map_temp.js', 'map.js')
        self.view.load(QtCore.QUrl.fromLocalFile(os.path.abspath('map.html')))

    def ansi_shell_command(self,host_dict,command):
        for k,v in host_dict.items():
            subprocess.call('ansible '+ k +' -m shell -a \"' + command + '\" &',shell=True)

    def ansi_copy(self,host_dict,file,destination):
        for k,v in host_dict.items():
            subprocess.call('ansible '+ k +' -m copy -a \"src='+ str(file) +' dest=' + str(destination) + '\" &',shell=True)

    def experiment_start(self):
        #send = subprocess.call('ansible cnc -m copy -a \"src='+self.nextrad_ini+' dest=' + self.cnc_header_loc + 'NeXtRAD.ini\"',shell=True)
        print(self.valid_nodes, self.valid_penteks, self.valid_rhinos)
        if self.valid_nodes or self.valid_penteks or self.valid_rhinos != {}:
            print('Starting Experiment')
            self.time_running = 1
            self.ansi_running = 1
            ansi_worker = Worker(self.ansi_play)
            #print(self.valid_hosts)
            self.threadpool.start(ansi_worker)
            countdown_worker = Worker(self.timer_thread)
            self.threadpool.start(countdown_worker)
        else:
            self.run_button.setText('Run')
            print('No valid host to send header to.')

    def ansi_play(self):
        if self.ansi_running == 1:
            #self.ansi_copy(self.valid_hosts,'~/Documents/NeXtRAD.ini')
            self.ansi_copy(self.valid_nodes,self.nextrad_ini,self.node_header_dir)
            self.ansi_copy(self.valid_nodes,self.nextrad_ini,self.gpsdo_header_dir)
            self.ansi_copy(self.valid_rhinos,self.nextrad_ini,self.rhino_header_dir)
            self.ansi_copy(self.valid_penteks,self.nextrad_ini,self.pentek_header_dir)
            self.ansi_running = 0

    def timer_thread(self):
        self.countdown_timer()
        self.remaining_timer()

    def countdown_timer(self):

        delta = int((self.start_time - datetime.datetime.now()).total_seconds())
        print('Experiment Running!')
        while delta>1:
            if self.time_running == 1:
                self.lbl_timer.setText('Countdown: ' + str(delta))
                delta = int((self.start_time - datetime.datetime.now()).total_seconds())
                time.sleep(1)

            else:
                print('Experiment Aborted!')
                self.time_running = 0
                self.experiment_running = 0
                self.run_button.setText('Run')
                return
        self.time_running = 0
        self.experiment_running = 1

    def remaining_timer(self):

        while self.time_remaining>1:
            if self.experiment_running == 1:
                #print(str(self.time_remaining))
                self.lbl_timer.setText('Time Remaining: ' + str(int(self.time_remaining/1000000)))
                self.time_remaining = self.time_remaining - 1000000
                time.sleep(1)
                self.save_scene_check = 1
            else:
                print('Experiment Aborted')
                self.run_button.setText('Run')
                self.time_running = 0
                self.experiment_running = 0
                self.time_remaining = 0
                self.save_scene_check = 0

        self.time_running = 0
        self.experiment_running = 0
        self.time_remaining = 0
        self.run_button.setText('Run')
        if self.save_scene_check == 1:
            self.save_scene()

    def save_scene(self):
        if self.scene_edit.text() == '':
            self.scene_edit.setText('No Notes. Change in text file if necessary.')

        experiment_log = str(self.start_time.year)[2:] + '_' + \
        str(self.start_time.month) + '_' + \
        str(self.start_time.day) + '_' + \
        str(self.start_time.hour) + '_' + \
        str(self.start_time.minute) + '_' + \
        str(self.start_time.second) + ';' + \
        str(self.bands) + ';' + \
        str(self.pols) + ';' + \
        str(self.pulse_width) + ';' + \
        str(self.pri) + ';' + \
        str(self.num_pri) + ';' + \
        str(self.scene_edit.text())

        with open(self.experiment_log_file,'a') as csvfile:
            if os.path.getsize(self.experiment_log_file):
                print('Log File Appended')
                self.save_scene_check = 0
                self.scene_edit.setText('')
                csvfile.write(experiment_log + '\n')

            else:
                csvfile.write('Timestamp;RF Frequency;Polarisations;Pulse Widths;PRI;Number of PRIs;Scene Description\n')
                print('Log File Appended')
                self.save_scene_check = 0
                self.scene_edit.setText('')
                csvfile.write(experiment_log + '\n')

    def run_experiment(self):
        if  self.time_running == 0 and self.experiment_running == 0:
            self.setup_header()
            self.run_button.setText('Abort')
            self.experiment_start()
        else:
            self.abort_experiment()
            print('Experiment Aborted!')
            self.time_running = 0
            self.run_button.setText('Run')

    def setup_header(self):
        inputfile=self.nextrad_ini
        outputfile='NeXtRAD.ini'

        nextrad_ini = inputfile
        config = configparser.ConfigParser()
        config.optionxform = lambda option: option  # preserve case for letters
        config.read(nextrad_ini)
        delay = config.get('Timing','starttimesecs')

        self.start_time = datetime.datetime.now() + datetime.timedelta(seconds=int(delay))

        config['Timing']['YEAR'] = str(self.start_time.year)
        config['Timing']['MONTH'] = str(self.start_time.month).zfill(2)
        config['Timing']['DAY'] = str(self.start_time.day).zfill(2)
        config['Timing']['HOUR'] = str(self.start_time.hour).zfill(2)
        config['Timing']['MINUTE'] = str(self.start_time.minute).zfill(2)
        config['Timing']['SECOND'] = str(self.start_time.second).zfill(2)

        #print('Experiment Start Time: ', self.start_time)

        with open(outputfile,'w') as configfile:
            config.write(configfile)

        # Target Information

        # Pulse Parameters
        print('Using Header: ', inputfile)
        print('Start Delay set to ', delay, ' seconds')

        self.init_nextheader_values()


#if __name__ == '_main__':
#     class MapViewer(QtWebEngine):
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args,**kwargs)

#             self.node_1_latlong = [0,0]
#             self.node_2_latlong = [0,0]
#             self.node_0_latlong = [0,0]
#             view = QtWebEngineWidgets.QWebEngineView()

# # load .html file
#             view.load(QUrl.fromLocalFile(os.path.abspath('map.html')))

#             layout.addWidget(view)

app = QtWidgets.QApplication([])
window = MainWindow()
#window2 = 
app.exec_()
