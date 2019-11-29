
import datetime
from io import StringIO
import sys
import signal
import time
import os
import configparser
from configobj import ConfigObj
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
from shutil import copyfile, copy
import shutil
from suitable import Api
from getpass import getpass

from suitable import Api
from getpass import getpass

from PyQt5 import Qt, QtWidgets, QtCore, QtGui, QtWebEngine, QtWebEngineWidgets, QtWebEngineWidgets
from PyQt5.QtCore import pyqtSlot

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

    @pyqtSlot()
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
        config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        config.optionxform = lambda option: option  # preserve case for letters
        config.read(gui_ini)
        self.stdout_result = StringIO()

        self.nextrad_ini = config.get('Files','nextrad_header')
        self.connections_ini = config.get('Files','connection')
        self.cnc_header_loc = config.get('HeaderDirects','cnc')
        self.experiment_log_file = config.get('Files','log_file')
        self.save_directory = config.get('Files','save_folder')
        self.node_header_dir = config.get('HeaderDirects','nodes')
        self.image_directory = config.get('HeaderDirects','save_imgs')
        self.pentek_header_dir = config.get('HeaderDirects','penteks')
        self.rhino_header_dir = config.get('HeaderDirects','rhinos')
        self.gpsdo_header_dir = config.get('HeaderDirects','gpsdos')
        self.local_copy_delay = config.get('Config','local_copy_delay')
        self.tcu_pulse_editor = config.get('Files','tcu_pulse_editor')
        self.gps0_ini = config.get('HeaderDirects','gps0') + '/gps_info.ini'
        self.gps1_ini = config.get('HeaderDirects','gps1') + '/gps_info.ini'
        self.gps2_ini = config.get('HeaderDirects','gps2') + '/gps_info.ini'
        self.autosaving = int(config.get('Config','auto_save_default'))
        self.map_style = int(config.get('Config','map_style_default'))
        self.node_0_on = int(config.get('Config','node_0_default'))
        self.node_1_on = int(config.get('Config','node_1_default'))
        self.node_2_on = int(config.get('Config','node_2_default'))

        print('NeXtRAD Header: ' + self.nextrad_ini)

        #State Flags
        #self.autosaving = 0 #Autosaving feature off by default
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
        self.cam0_include = 0
        self.cam1_include = 0
        self.cam2_include = 0
        self.abort_flag = 0
        #self.map_style = 0


        #Initialisers
        self.node_1_latlong = '0,0'
        self.node_2_latlong = '0,0'
        self.node_0_latlong = '0,0'
        self.target_latlong = '0,0'
        self.node_0_ht = '0'
        self.node_0_ht = '0'
        self.node_0_ht = '0'
        self.target_ht = '0'
        self.target_name = ''
        #nodes
        self.node0_location_name = ''
        self.node0_location_name = ''
        self.node0_location_name = ''
        self.experiment_name = ''
        self.target_description = ''
        self.start_time = ''
        self.experiment_start_string = ''

        self.create_host_dict()

        #Radar Parameters
        self.start_time = 0
        self.pri = []
        self.num_pri = 0
        self.bands = []
        self.pols = []
        self.pulse_width = []

        #Start the Threadpool
        self.threadpool = QtCore.QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        layout = QtWidgets.QGridLayout()

        #GUI Text
        self.lbl_experi_name = QtWidgets.QLabel('Experiment Description:')
        self.lbl_trgt_latlong = QtWidgets.QLabel('Target (Lat,Long):')
        self.lbl_scene = QtWidgets.QLabel('Scene Notes:')
        self.lbl_timer = QtWidgets.QLabel('0') 
        timer_font = QtGui.QFont('Open Sans',20, QtGui.QFont.Bold)
        self.lbl_timer.setFont(timer_font)
        self.lbl_timer.setAlignment(Qt.Qt.AlignCenter)
        #self.lbl_timer.setFont(18)
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
        self.lbl_bullet_0_tx = QtWidgets.QLabel('Bullet 0 TX     ')
        self.lbl_bullet_1_tx = QtWidgets.QLabel('Bullet 1 TX     ')
        self.lbl_bullet_2_tx = QtWidgets.QLabel('Bullet 2 TX     ')
        self.lbl_bullet_0_rx = QtWidgets.QLabel('Bullet 0 RX     ')
        self.lbl_bullet_1_rx = QtWidgets.QLabel('Bullet 1 RX     ')
        self.lbl_bullet_2_rx = QtWidgets.QLabel('Bullet 2 RX     ')


        # - Pulse Parameters
        self.lbl_rt = QtWidgets.QLabel('Length: ' + str(self.time_remaining) + 's')
        self.lbl_fc = QtWidgets.QLabel('Freq: ' + str(self.bands))
        self.lbl_pw = QtWidgets.QLabel('PW: ' + str(self.pulse_width))
        self.lbl_pol = QtWidgets.QLabel('Pols: ' + str(self.pols))
        self.lbl_pri = QtWidgets.QLabel('PRI: ' + str(self.pri))

        #Pushbuttons
        self.map_style_button = QtWidgets.QPushButton('Map Style')
        self.run_button = QtWidgets.QPushButton('Run')
        self.abort_button = QtWidgets.QPushButton('Quickview')
        self.save_button = QtWidgets.QPushButton('Save ADC Data')
        self.map_style_button.clicked.connect(self.change_map_style)
        self.save_button.clicked.connect(self.save_adc_data)
        self.run_button.clicked.connect(self.run_experiment)
        self.abort_button.clicked.connect(self.run_quickview)
        self.target_accept = QtWidgets.QPushButton('Enter Details')
        self.description_accept = QtWidgets.QPushButton('Enter Details')
        self.scene_accept = QtWidgets.QPushButton('Enter Details')
        self.target_accept.clicked.connect(self.enter_target_details)
        self.description_accept.clicked.connect(self.enter_description)
        self.pulses_button = QtWidgets.QPushButton('Pulses')
        self.pulses_button.clicked.connect(self.run_pulse_editor)
        #Textboxes
        self.target_details = QtWidgets.QLineEdit(self)
        self.target_details.editingFinished.connect(self.enter_target_details)
        self.experiment_name_edit = QtWidgets.QLineEdit(self)
        self.experiment_name_edit.editingFinished.connect(self.enter_description)
        self.scene_edit = QtWidgets.QLineEdit(self)
        #self.scene_edit.editingFinished.connect(self.enter_scene)

        #Checkboxes
        self.node_0_disable = QtWidgets.QCheckBox("Node 0",self)
        self.node_0_disable.stateChanged.connect(self.disable_node0)
        if self.node_0_on == 1:
            self.node_0_disable.setChecked(True)
        self.node_1_disable = QtWidgets.QCheckBox("Node 1",self)
        self.node_1_disable.stateChanged.connect(self.disable_node1)
        if self.node_1_on == 1:
            self.node_1_disable.setChecked(True)
        self.node_2_disable = QtWidgets.QCheckBox("Node 2",self)
        self.node_2_disable.stateChanged.connect(self.disable_node2)
        if self.node_2_on == 1:
            self.node_2_disable.setChecked(True)
        self.auto_save = QtWidgets.QCheckBox("Autosave",self)
        self.auto_save.stateChanged.connect(self.auto_saver)
        if self.autosaving == 1:
            self.auto_save.setChecked(True)
        #Connection Stats
        #Penteks
        # self.pent_1 = QLabel('Pentek 0')
        # self.pent_2 = QLabel('Pentek 0')

        #images
        self.quickview_image_refresh()

        self.view = QtWebEngineWidgets.QWebEngineView()

# load .html file
        self.view.load(QtCore.QUrl.fromLocalFile(os.path.abspath('map.html')))

        self.columna = QtWidgets.QGroupBox()
        #groupbox.setCheckable(True)
        layout.addWidget(self.columna,0,0)
        self.abox = QtWidgets.QVBoxLayout()
        self.columna.setLayout(self.abox)



        self.columnb = QtWidgets.QGroupBox()
        #groupbox.setCheckable(True)
        layout.addWidget(self.columnb,0,1)
        self.bbox = QtWidgets.QVBoxLayout()
        self.columnb.setLayout(self.bbox)

        self.mid = QtWidgets.QGroupBox('Target and Geometry')
        #groupbox.setCheckable(True)
        self.bbox.addWidget(self.mid)
        self.midbox = QtWidgets.QGridLayout()
        self.mid.setLayout(self.midbox)

        self.columnd = QtWidgets.QGroupBox()
        #groupbox.setCheckable(True)
        layout.addWidget(self.columnd,0,0)
        self.dbox = QtWidgets.QVBoxLayout()
        self.columnd.setLayout(self.dbox)

        self.vids = QtWidgets.QGroupBox("Cameras")
        #groupbox.setCheckable(True)
        self.dbox.addWidget(self.vids)
        self.vidbox = QtWidgets.QGridLayout()
        #self.vidbox.addStretch(1)
        self.vids.setLayout(self.vidbox)

        self.columnc = QtWidgets.QGroupBox()
        #groupbox.setCheckable(True)
        layout.addWidget(self.columnc,0,2)
        self.cbox = QtWidgets.QVBoxLayout()

        self.columnc.setLayout(self.cbox)


        self.runs = QtWidgets.QGroupBox("Run Experiment")
        #groupbox.setCheckable(True)
        self.cbox.addWidget(self.runs)
        self.veepbox = QtWidgets.QVBoxLayout()
        self.veepbox.addStretch(1)
        self.runs.setLayout(self.veepbox)

        self.groupbox = QtWidgets.QGroupBox("Radar Control")
        #groupbox.setCheckable(True)
        self.cbox.addWidget(self.groupbox)
        self.vbox = QtWidgets.QVBoxLayout()
        self.groupbox.setLayout(self.vbox)

        self.pps = QtWidgets.QGroupBox("Pulse Parameters")
        #groupbox.setCheckable(True)
        self.cbox.addWidget(self.pps)
        self.veebox = QtWidgets.QVBoxLayout()
        self.pps.setLayout(self.veebox)





        self.veepbox.addWidget(self.lbl_timer)
        self.veepbox.addWidget(self.run_button)

        self.vbox.addWidget(self.abort_button)
        self.vbox.addWidget(self.pulses_button)
        self.vbox.addWidget(self.save_button)
        self.vbox.addWidget(self.auto_save)

        self.cam0 = QtWebEngineWidgets.QWebEngineView()
        self.cam0.setUrl(QtCore.QUrl('https://www.youtube.com/watch?v=avaSdC0QOUM'))
        self.vidbox.addWidget(self.cam0,0,0)

        self.cam1 = QtWebEngineWidgets.QWebEngineView()
        self.cam1.setUrl(QtCore.QUrl('https://www.youtube.com/watch?v=6fr87wPvNIs'))
        self.vidbox.addWidget(self.cam1,1,0)

        self.cam2 = QtWebEngineWidgets.QWebEngineView()
        self.cam2.setUrl(QtCore.QUrl('https://www.youtube.com/watch?v=6UgDdOh--W4'))
        self.vidbox.addWidget(self.cam2,2,0)

        self.veebox.addWidget(self.lbl_rt)
        self.veebox.addWidget(self.lbl_fc)
        self.veebox.addWidget(self.lbl_pri)
        self.veebox.addWidget(self.lbl_pw)
        self.veebox.addWidget(self.lbl_pol)





        #layout.addWidget(self.lbl_timer,0,1)

        #layout.addWidget(self.text,0,0,1,2)

        #layout.addWidget(self.run_button,2,0)


        self.midbox.addWidget(self.lbl_experi_name,0,0)
        self.midbox.addWidget(self.experiment_name_edit,0,1)
        self.midbox.addWidget(self.description_accept,0,2)

        self.midbox.addWidget(self.view,1,0,10,3)
        self.midbox.addWidget(self.map_style_button,10,0)

        self.midbox.addWidget(self.lbl_trgt_latlong,11,0)
        self.midbox.addWidget(self.target_details,11,1)
        self.midbox.addWidget(self.target_accept,11,2)

        self.midbox.addWidget(self.lbl_scene,12,0)
        self.midbox.addWidget(self.scene_edit,12,1,1,2)
        #layout.addWidget(self.scene_accept,18,3)

        self.connects = QtWidgets.QGroupBox('Network')
        #groupbox.setCheckable(True)
        self.cbox.addWidget(self.connects)
        self.conbox = QtWidgets.QGridLayout()
        self.connects.setLayout(self.conbox)

        self.conbox.addWidget(self.lbl_cnc,0,0)
        self.conbox.addWidget(self.lbl_ntp,0,1)

        self.conbox.addWidget(self.lbl_bullet_0_tx,1,0)
        self.conbox.addWidget(self.lbl_bullet_0_rx,2,0)

        self.conbox.addWidget(self.lbl_bullet_1_tx,1,1)
        self.conbox.addWidget(self.lbl_bullet_1_rx,2,1)

        self.conbox.addWidget(self.lbl_bullet_2_tx,1,2)
        self.conbox.addWidget(self.lbl_bullet_2_rx,2,2)

        self.conbox.addWidget(self.node_0_disable,3,0)
        self.conbox.addWidget(self.pent_zero,4,0)
        self.conbox.addWidget(self.node_zero,5,0)
        self.conbox.addWidget(self.rhino_zero,6,0)

        # layout.addWidget(self.n0ch0,7,4,1,1)
        # layout.addWidget(self.n0ch1,8,4,1,1)
        # layout.addWidget(self.n0ch2,9,4,1,1)

        self.conbox.addWidget(self.node_1_disable,3,1)
        self.conbox.addWidget(self.pent_one,4,1)
        self.conbox.addWidget(self.node_one,5,1)
        self.conbox.addWidget(self.rhino_one,6,1)

        # layout.addWidget(self.n1ch0,7,5,1,1)
        # layout.addWidget(self.n1ch1,8,5,1,1)
        # layout.addWidget(self.n1ch2,9,5,1,1)

        self.conbox.addWidget(self.node_2_disable,3,2)
        self.conbox.addWidget(self.pent_two,4,2)
        self.conbox.addWidget(self.node_two,5,2)
        self.conbox.addWidget(self.rhino_two,6,2)

        # layout.addWidget(self.n2ch0,7,6,1,1)
        # layout.addWidget(self.n2ch1,8,6,1,1)
        # layout.addWidget(self.n2ch2,9,6,1,1)

        self.ims = QtWidgets.QGroupBox('Quickviews')
        #groupbox.setCheckable(True)
        self.cbox.addWidget(self.ims)
        self.imbox = QtWidgets.QGridLayout()
        self.ims.setLayout(self.imbox)

        self.lbl_ims_node0 = QtWidgets.QLabel('Node0')
        self.lbl_ims_node1 = QtWidgets.QLabel('Node1')
        self.lbl_ims_node2 = QtWidgets.QLabel('Node2')
        self.lbl_ims_ch0 = QtWidgets.QLabel('L')
        self.lbl_ims_ch1 = QtWidgets.QLabel('XV')
        self.lbl_ims_ch2 = QtWidgets.QLabel('XH')

        self.lbl_ims_node0.setAlignment(Qt.Qt.AlignCenter)
        self.lbl_ims_node1.setAlignment(Qt.Qt.AlignCenter)
        self.lbl_ims_node2.setAlignment(Qt.Qt.AlignCenter)
        self.lbl_ims_ch0.setAlignment(Qt.Qt.AlignCenter)
        self.lbl_ims_ch1.setAlignment(Qt.Qt.AlignCenter)
        self.lbl_ims_ch2.setAlignment(Qt.Qt.AlignCenter)

        self.update_quickview_ims()

        self.abox.addStretch(1)
        self.cbox.addStretch(1)
 




        w = QtWidgets.QWidget()
        w.setLayout(layout)
        self.init_nextheader_values()
        state_update = Worker(self.check_state)
        self.threadpool.start(state_update)

        self.setCentralWidget(w)
        self.init_map()
        self.target_details.setText(self.target_latlong)
        self.change_map_style()
        self.experiment_name_edit.setText(self.experiment_name)

        self.show()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_state)
        self.timer.timeout.connect(self.quickview_image_refresh)
        self.timer.timeout.connect(self.update_quickview_ims)
        self.timer.timeout.connect(self.update_video_stream)
        self.timer.start(500)

    def update_quickview_ims(self):

        self.imbox.addWidget(self.lbl_ims_node0,0,0)
        self.imbox.addWidget(self.lbl_ims_node1,0,1)
        self.imbox.addWidget(self.lbl_ims_node2,0,2)
        self.imbox.addWidget(self.lbl_ims_ch0,1,3)
        self.imbox.addWidget(self.lbl_ims_ch1,2,3)
        self.imbox.addWidget(self.lbl_ims_ch2,3,3)

        self.imbox.addWidget(self.n0ch0,1,0)
        self.imbox.addWidget(self.n0ch1,2,0)
        self.imbox.addWidget(self.n0ch2,3,0)
        self.imbox.addWidget(self.n1ch0,1,1)
        self.imbox.addWidget(self.n1ch1,2,1)
        self.imbox.addWidget(self.n1ch2,3,1)
        self.imbox.addWidget(self.n2ch0,1,2)
        self.imbox.addWidget(self.n2ch1,2,2)
        self.imbox.addWidget(self.n2ch2,3,2)

    def update_video_stream(self):
        if self.host_dict['ipcam0']['is_con'] == 0:
            self.vidbox.addWidget(self.n1ch2,0,0)
        else:
            self.cam0 = QtWebEngineWidgets.QWebEngineView()
            self.cam0.setUrl(QtCore.QUrl('https://www.youtube.com/watch?v=avaSdC0QOUM'))
            self.vidbox.addWidget(self.cam0,0,0)

    def quickview_image_refresh(self):
        self.n0ch0 = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('./quickview_images/Range-Time-Intensity-ch0-n0.jpg')
        pixmap = pixmap.scaled(70, 70, QtCore.Qt.KeepAspectRatio)
        self.n0ch0.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())


        self.n0ch1 = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('./quickview_images/Range-Time-Intensity-ch1-n0.jpg')
        pixmap = pixmap.scaled(70, 70, QtCore.Qt.KeepAspectRatio)
        self.n0ch1.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())
    
        self.n0ch2 = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('./quickview_images/Range-Time-Intensity-ch2-n0.jpg')
        pixmap = pixmap.scaled(70, 70, QtCore.Qt.KeepAspectRatio)
        self.n0ch2.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())

        self.n1ch0 = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('./quickview_images/Range-Time-Intensity-ch0-n1.jpg')
        pixmap = pixmap.scaled(70, 70, QtCore.Qt.KeepAspectRatio)
        self.n1ch0.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())

        self.n1ch1 = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('./quickview_images/Range-Time-Intensity-ch1-n1.jpg')
        pixmap = pixmap.scaled(70, 70, QtCore.Qt.KeepAspectRatio)
        self.n1ch1.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())
    
        self.n1ch2 = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('./quickview_images/Range-Time-Intensity-ch2-n1.jpg')
        pixmap = pixmap.scaled(70, 70, QtCore.Qt.KeepAspectRatio)
        self.n1ch2.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())

        self.n2ch0 = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('./quickview_images/Range-Time-Intensity-ch0-n2.jpg')
        pixmap = pixmap.scaled(70, 70, QtCore.Qt.KeepAspectRatio)
        self.n2ch0.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())

        self.n2ch1 = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('./quickview_images/Range-Time-Intensity-ch1-n2.jpg')
        pixmap = pixmap.scaled(70, 70, QtCore.Qt.KeepAspectRatio)
        self.n2ch1.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())

        self.n2ch2 = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('./quickview_images/Range-Time-Intensity-ch2-n2.jpg')
        pixmap = pixmap.scaled(70, 70, QtCore.Qt.KeepAspectRatio)
        self.n2ch2.setPixmap(pixmap)
        #self.resize(pixmap.width(), pixmap.height())

        
        # #Layout Setup

    def init_nextheader_values(self):

        config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        config.optionxform = lambda option: option  # preserve case for letters
        config.read(self.nextrad_ini)
        self.node_0_latlong = config.get('GeometrySettings','NODE0_LOCATION_LAT')+','+config.get('GeometrySettings','NODE0_LOCATION_LON')
        self.node_1_latlong = config.get('GeometrySettings','NODE1_LOCATION_LAT')+','+config.get('GeometrySettings','NODE1_LOCATION_LON')
        self.node_2_latlong = config.get('GeometrySettings','NODE2_LOCATION_LAT')+','+config.get('GeometrySettings','NODE2_LOCATION_LON')
        self.node_0_ht = config.get('GeometrySettings','NODE0_LOCATION_HT')
        self.node_1_ht = config.get('GeometrySettings','NODE1_LOCATION_HT')
        self.node_2_ht = config.get('GeometrySettings','NODE2_LOCATION_HT')
        self.target_latlong = config.get('TargetSettings','TGT_LOCATION_LAT')+','+config.get('TargetSettings','TGT_LOCATION_LON')
        self.target_ht = config.get('TargetSettings','TGT_LOCATION_HT')

        self.experiment_name = config.get('Notes','EXPERIMENT_NAME')
        self.target_description = config.get('Notes','EXPERIMENT_NOTES')

        self.num_pri = int(config.get('PulseParameters','NUM_PRIS'))
        self.pulses = config.get('PulseParameters','PULSES')
        self.pri = []
        self.bands = []
        self.pols = []
        self.pulse_width = []

        pulses = []
        pulses_arr = self.pulses.split('|')

        for pulse in range(len(pulses_arr)):
            pulses_arr[pulse]=pulses_arr[pulse].replace('\"','')
            #print(pulse)
            pulses.append(pulses_arr[pulse].split(','))
            #print(pulses[pulse])
            self.pri.append(float(pulses[pulse][1]))
            self.pols.append(int(pulses[pulse][2]))
            self.bands.append(float(pulses[pulse][3].replace('\"','')))
            self.pulse_width.append(float(pulses[pulse][0].replace('\"','')))

        self.time_remaining = self.pri[0]*self.num_pri #In microseconds

        self.lbl_fc.setText('Freq: ' + str(self.bands))
        self.lbl_rt.setText('Length: ' + str(self.time_remaining/1000000) + 's')
        self.lbl_pw.setText('PW: ' + str(self.pulse_width))
        self.lbl_pol.setText('Pols: ' + str(self.pols))
        self.lbl_pri.setText('PRI: ' + str(self.pri))

    def init_map(self):
        self.update_map('var n0 = ','var n0 = [' + self.node_0_latlong + '];\n')
        self.update_map('var n1 = ','var n1 = [' + self.node_1_latlong + '];\n')
        self.update_map('var n2 = ','var n2 = [' + self.node_2_latlong + '];\n')

    def auto_saver(self):
        if self.auto_save.isChecked():
            self.autosaving = 1
            print('Autosaving On')
        else:
            self.autosaving = 0
            print('Autosaving Off')

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
        config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        config.optionxform = lambda option: option  # preserve case for letters
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
            self.lbl_timer.setText('  Not Running  ')
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
            if self.host_dict['rhino1']['is_con'] == 0 and self.rhino_one_include == 1:
                self.rhino_one.setStyleSheet('color: red')
            elif self.host_dict['rhino1']['is_con'] == 1 and self.rhino_one_include == 1:
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

        try:
            if self.host_dict['tx_bullet0']['is_con'] == 0:
                self.lbl_bullet_0_tx.setStyleSheet('color: red')
            else:
                self.lbl_bullet_0_tx.setStyleSheet('color: green')
        except:
            self.lbl_bullet_0_tx.setStyleSheet('color: gray')
            self.lbl_bullet_0_tx.setText('Missing config')

        try:
            if self.host_dict['rx_bullet0']['is_con'] == 0:
                self.lbl_bullet_0_rx.setStyleSheet('color: red')
            else:
                self.lbl_bullet_0_rx.setStyleSheet('color: green')
        except:
            self.lbl_bullet_0_rx.setStyleSheet('color: gray')
            self.lbl_bullet_0_rx.setText('Missing config')

        try:
            if self.host_dict['tx_bullet1']['is_con'] == 0:
                self.lbl_bullet_1_tx.setStyleSheet('color: red')
            else:
                self.lbl_bullet_1_tx.setStyleSheet('color: green')
        except:
            self.lbl_bullet_1_tx.setStyleSheet('color: gray')
            self.lbl_bullet_1_tx.setText('Missing config')

        try:
            if self.host_dict['rx_bullet0']['is_con'] == 0:
                self.lbl_bullet_1_rx.setStyleSheet('color: red')
            else:
                self.lbl_bullet_1_rx.setStyleSheet('color: green')
        except:
            self.lbl_bullet_1_rx.setStyleSheet('color: gray')
            self.lbl_bullet_1_rx.setText('Missing config')

        try:
            if self.host_dict['tx_bullet2']['is_con'] == 0:
                self.lbl_bullet_2_tx.setStyleSheet('color: red')
            else:
                self.lbl_bullet_2_tx.setStyleSheet('color: green')
        except:
            self.lbl_bullet_2_tx.setStyleSheet('color: gray')
            self.lbl_bullet_2_tx.setText('Missing config')

        try:
            if self.host_dict['rx_bullet2']['is_con'] == 0:
                self.lbl_bullet_2_rx.setStyleSheet('color: red')
            else:
                self.lbl_bullet_2_rx.setStyleSheet('color: green')
        except:
            self.lbl_bullet_2_rx.setStyleSheet('color: gray')
            self.lbl_bullet_2_rx.setText('Missing config')

    def run_quickview(self):
        #if self.plot_is_active == 1:
        subprocess.call('python3 plottty.py &',shell=True)

    def run_pulse_editor(self):
        subprocess.call('cd ' + self.tcu_pulse_editor + ' && python3 creator.py -f ' + self.nextrad_ini + ' -o ' + self.nextrad_ini + ' &',shell=True)

    def abort_experiment(self):
        print('Aborting Experiment!')
        self.abort_flag = 1
        self.time_running = 0
        self.time_remaining = 0
        self.experiment_running = 0
        self.ansi_running = 0
        self.ansi_shell_command(self.valid_penteks,'cd ' + self.pentek_header_dir + ' && ./killscript.sh &' )
        self.ansi_shell_command(self.valid_nodes,'export PYTHONPATH=/home/nextrad/Documents/tcu_stuff/harpoon/ && cd ' + self.node_header_dir + ' && nohup ./tcu_abort_script.sh' )
        self.run_button.setText('Run')

    def save_folder(self):
        print('temp')

    def enter_target_details(self):
        if self.target_details.text() != '':
            self.target_latlong = self.target_details.text()
            self.init_map()
            self.update_map('var trgt = ','var trgt = [' + self.target_latlong + '];\n')
            print('Target Details Updated')
        else:
            print('Please Enter Valid Address as Lat, Long')

    def change_map_style(self):
        if self.map_style == 0:
            self.update_map('id: \'mapbox.','    id: \'mapbox.outdoors\',\n')
            self.map_style = 1
        else:
            self.update_map('id: \'mapbox.','    id: \'mapbox.satellite\',\n')
            self.map_style = 0

    def enter_scene(self):
        print('Scene description added to excel file')

    def enter_description(self):
        ini_file = self.nextrad_ini
        config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        config.optionxform = lambda option: option  # preserve case for letters
        config.read(ini_file)

        if self.experiment_name_edit.text() != '':
            config['Notes']['EXPERIMENT_NAME'] = self.experiment_name_edit.text()
            print('Description Set')

        else:
            print('Nothing Entered, Using Default \'No Description\'')
            config['Notes']['EXPERIMENT_NAME'] = 'No Description'

        with open(self.nextrad_ini,'w') as configfile:
            config.write(configfile)

    def update_map(self,textin,replace):

        self.update_gps_positions(self.valid_nodes)

        copyfile('map.js', 'map_backup.js')
        with open('map.js') as fin, open('map_temp.js', 'w') as fout:
            for line in fin:
                if textin in line:
                    line = replace

                fout.write(line)

        os.rename('map_temp.js', 'map.js')
        self.view.load(QtCore.QUrl.fromLocalFile(os.path.abspath('map.html')))

    def update_gps_positions(self, host_dict):
        for k,v in host_dict.items():
            if k == 'node0' and v['is_con'] == 1:
                with open(self.gps0_ini) as f0:
                    file_content0 = '[dummy_section]\n' + f0.read()

                config0 = configparser.RawConfigParser(comment_prefixes=';', allow_no_value=True)
                config0.optionxform = lambda option: option  # preserve case for letters
                config0.read_string(file_content0)
                x = (config0.get('dummy_section','LATITUDE'))
                y = (config0.get('dummy_section','LONGITUDE'))
                #  x = int(config0.get('dummy_section','LATITUDE'))
                # y = int(config0.get('dummy_section','LONGITUDE'))
                # if x > 2**31 - 1 :
                #     x = (2**32 - x)*(-1)
                # else:
                #     x = x
                # if y > 2**31 - 1 :
                #     y = (2**32 - y)*(-1)
                # else:
                #     y = y

                # self.node_0_latlong = str(x*90/324e6) +',' + str(y*90/324e6)
                self.node_0_latlong = x + ',' + y
                self.node_0_ht = str(config0.get('dummy_section','ALTITUDE'))

                print('GPS0 Data: ' + self.node_0_latlong + ', ' + self.node_0_ht )
            
            if k == 'node1' and v['is_con'] == 1:
                with open(self.gps1_ini) as f1:
                    file_content1 = '[dummy_section]\n' + f1.read()

                config1 = configparser.RawConfigParser(comment_prefixes=';', allow_no_value=True)
                config1.optionxform = lambda option: option  # preserve case for letters
                config1.read_string(file_content1)
                x = (config1.get('dummy_section','LATITUDE'))
                y = (config1.get('dummy_section','LONGITUDE'))
                # x = int(config1.get('dummy_section','LATITUDE'))
                # y = int(config1.get('dummy_section','LONGITUDE'))
                # if x > 2**31 - 1 :
                #     x = (2**32 - x)*(-1)
                # else:
                #     x = x
                # if y > 2**31 - 1 :
                #     y = (2**32 - y)*(-1)
                # else:
                #     y = y

                # self.node_1_latlong = str(x*90/324e6) +',' + str(y*90/324e6)
                self.node_1_latlong = x + ',' + y
                self.node_1_ht = str(config1.get('dummy_section','ALTITUDE'))

                print('GPS1 Data: ' + self.node_1_latlong + ', ' + self.node_1_ht )

            if k == 'node2' and v['is_con'] == 1:
                with open(self.gps2_ini) as f2:
                    file_content2 = '[dummy_section]\n' + f2.read()

                config2 = configparser.RawConfigParser(comment_prefixes=';', allow_no_value=True)
                config2.optionxform = lambda option: option  # preserve case for letters
                config2.read_string(file_content2)
                x = (config2.get('dummy_section','LATITUDE'))
                y = (config2.get('dummy_section','LONGITUDE'))
                # x = int(config2.get('dummy_section','LATITUDE'))
                # y = int(config2.get('dummy_section','LONGITUDE'))
                # if x > 2**31 - 1 :
                #     x = (2**32 - x)*(-1)
                # else:
                #     x = x
                # if y > 2**31 - 1 :
                #     y = (2**32 - y)*(-1)
                # else:
                #     y = y

                # self.node_2_latlong = str(x*90/324e6) +',' + str(y*90/324e6)
                self.node_2_latlong = x + ',' + y
                self.node_2_ht = str(config2.get('dummy_section','ALTITUDE'))

                print('GPS2 Data: ' + self.node_2_latlong + ', ' + self.node_2_ht )


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
            self.ansi_copy(self.valid_penteks,self.nextrad_ini,self.pentek_header_dir)
            #self.ansi_copy(self.valid_hosts,'~/Documents/NeXtRAD.ini')

            self.ansi_copy(self.valid_nodes,self.nextrad_ini,self.gpsdo_header_dir)
            #self.ansi_copy(self.valid_rhinos,self.nextrad_ini,self.rhino_header_dir)
            self.ansi_shell_command(self.valid_penteks,'cd ' + self.pentek_header_dir + ' && ./run-cobalt.sh')
            self.ansi_running = 0
            self.ansi_shell_command(self.valid_nodes,'cd ' + self.node_header_dir + ' && rm NeXtRAD.ini')
            time.sleep(int(self.local_copy_delay))
            copy('NeXtRAD.ini', self.cnc_header_loc + '/NeXtRAD.ini')

            self.ansi_copy(self.valid_nodes,self.nextrad_ini,self.node_header_dir)

    def timer_thread(self):
        self.countdown_timer()
        self.remaining_timer()

    def countdown_timer(self):

        delta = int((self.start_time - datetime.datetime.now()).total_seconds())
        print('Experiment Running!')
        while delta>1:
            if self.time_running == 1:
                self.lbl_timer.setText(' Countdown: ' + str(delta) + '  ')
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
                self.lbl_timer.setText(' Running: ' + str(int(self.time_remaining/1000000)) + ' ')
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
        self.ansi_shell_command(self.valid_penteks,'cd ' + self.pentek_header_dir + ' && ./killscript.sh &' )
        self.run_button.setText('Run')
        #if self.save_scene_check == 1:
            #self.save_scene()
        if self.autosaving == 1 and self.abort_flag == 0:
            time.sleep(1)
            self.save_adc_data()
        self.abort_flag = 0

    def save_adc_data(self):
        print('Saving ADC Files to External Hardrive/s')
        if self.pent_zero_include:
            subprocess.call('ansible pentek0 -m shell -a \"' + 'cd /home/transceiversystem/Documents/nextlook/build && nextlook -n 0 -x 0 -b' + '\" &',shell=True)
        if self.pent_one_include:
            subprocess.call('ansible pentek1 -m shell -a \"' + 'cd /home/transceiversystem/Documents/nextlook/build && nextlook -n 1 -x 0 -b' + '\" &',shell=True)
        if self.pent_two_include:
            subprocess.call('ansible pentek2 -m shell -a \"' + 'cd /home/transceiversystem/Documents/nextlook/build && nextlook -n 2 -x 0 -b' + '\" &',shell=True)

        self.save_scene()

    def save_scene(self):

        if self.scene_edit.text() == '':
            self.scene_edit.setText('No Notes. Change in text file if necessary.')

        if (self.start_time) == 0:
            self.experiment_start_string = 'SeeHeader' + str(datetime.datetime.now())

        experiment_log = self.experiment_start_string + ';' + \
        str(self.bands) + ';' + \
        str(self.pols) + ';' + \
        str(self.pulse_width) + ';' + \
        str(self.pri) + ';' + \
        str(self.num_pri) + ';' + \
        str(self.experiment_name) + ';' + \
        str(self.scene_edit.text())

        with open(self.experiment_log_file,'a') as csvfile:
            if os.path.getsize(self.experiment_log_file):
                print('Log File Appended')
                self.save_scene_check = 0
                self.scene_edit.setText('')
                csvfile.write(experiment_log + '\n')

            else:
                csvfile.write('Timestamp;RF Frequency;Polarisations;Pulse Widths;PRI;Number of PRIs;Experiment;Notes\n')
                print('Log File Appended')
                self.save_scene_check = 0
                self.scene_edit.setText('')
                csvfile.write(experiment_log + '\n')

        copy(self.experiment_log_file, self.save_directory)

        directory = self.save_directory + '/' + self.experiment_start_string
        image_directory = directory + '/quicklook_images'
        os.mkdir(directory)
        os.mkdir(image_directory)
        self.copytree(self.image_directory, image_directory)

        copy(self.nextrad_ini,directory)

        print('Save Folder: ' + self.experiment_start_string)

    def copytree(self,src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

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
        config = configparser.ConfigParser(comment_prefixes='/', allow_no_value=True)
        config.optionxform = lambda option: option  # preserve case for letters
        config.read(nextrad_ini)
        delay = config.get('Timing','STARTTIMESECS')

        self.start_time = datetime.datetime.now() + datetime.timedelta(seconds=int(delay))
        self.experiment_start_string = str(self.start_time.year)[2:] + '_' + \
            str(self.start_time.month) + '_' + \
            str(self.start_time.day) + '_' + \
            str(self.start_time.hour) + '_' + \
            str(self.start_time.minute) + '_' + \
            str(self.start_time.second)


        config['Timing']['YEAR'] = str(self.start_time.year)
        config['Timing']['MONTH'] = str(self.start_time.month).zfill(2)
        config['Timing']['DAY'] = str(self.start_time.day).zfill(2)
        config['Timing']['HOUR'] = str(self.start_time.hour).zfill(2)
        config['Timing']['MINUTE'] = str(self.start_time.minute).zfill(2)
        config['Timing']['SECOND'] = str(self.start_time.second).zfill(2)

        config['GeometrySettings']['NODE0_LOCATION_LAT'] = str(eval(self.node_0_latlong)[0])
        config['GeometrySettings']['NODE0_LOCATION_LON'] = str(eval(self.node_0_latlong)[1])
        config['GeometrySettings']['NODE0_LOCATION_HT'] = self.node_0_ht
        config['GeometrySettings']['NODE1_LOCATION_LAT'] = str(eval(self.node_1_latlong)[0])
        config['GeometrySettings']['NODE1_LOCATION_LON'] = str(eval(self.node_1_latlong)[1])
        config['GeometrySettings']['NODE1_LOCATION_HT'] = self.node_1_ht
        config['GeometrySettings']['NODE2_LOCATION_LAT'] = str(eval(self.node_2_latlong)[0])
        config['GeometrySettings']['NODE2_LOCATION_LON'] = str(eval(self.node_2_latlong)[1])
        config['GeometrySettings']['NODE2_LOCATION_HT'] = self.node_2_ht
        config['TargetSettings']['TGT_LOCATION_LAT'] = str(eval(self.target_latlong)[0])
        config['TargetSettings']['TGT_LOCATION_LON'] = str(eval(self.target_latlong)[1])
        config['TargetSettings']['TGT_LOCATION_HT'] = self.target_ht


        #print('Experiment Start Time: ', self.start_time)

        with open(outputfile,'w') as configfile:
            config.write(configfile)

        # Target Information

        # Pulse Parameters
        print('Using Header: ', inputfile)
        print('Start Delay set to ', delay, ' seconds')

        self.init_nextheader_values()


app = QtWidgets.QApplication([])
window = MainWindow()
window.setWindowIcon(QtGui.QIcon('icon.png'))
app.exec_()
