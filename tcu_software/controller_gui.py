# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'controller_gui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(637, 522)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_6 = QtWidgets.QFrame(self.centralwidget)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_5 = QtWidgets.QFrame(self.frame_6)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.but_read = QtWidgets.QPushButton(self.frame_5)
        self.but_read.setObjectName("but_read")
        self.gridLayout_2.addWidget(self.but_read, 0, 0, 1, 1)
        self.but_override = QtWidgets.QPushButton(self.frame_5)
        self.but_override.setObjectName("but_override")
        self.gridLayout_2.addWidget(self.but_override, 1, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.frame_5)
        spacerItem = QtWidgets.QSpacerItem(271, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.frame_2 = QtWidgets.QFrame(self.frame_6)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.but_arm_disarm = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.but_arm_disarm.sizePolicy().hasHeightForWidth())
        self.but_arm_disarm.setSizePolicy(sizePolicy)
        self.but_arm_disarm.setMinimumSize(QtCore.QSize(100, 85))
        self.but_arm_disarm.setMaximumSize(QtCore.QSize(85, 16777215))
        self.but_arm_disarm.setObjectName("but_arm_disarm")
        self.gridLayout.addWidget(self.but_arm_disarm, 0, 0, 1, 1)
        self.but_fire_abort = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.but_fire_abort.sizePolicy().hasHeightForWidth())
        self.but_fire_abort.setSizePolicy(sizePolicy)
        self.but_fire_abort.setMinimumSize(QtCore.QSize(100, 85))
        self.but_fire_abort.setAutoFillBackground(False)
        self.but_fire_abort.setObjectName("but_fire_abort")
        self.gridLayout.addWidget(self.but_fire_abort, 0, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.gridLayout_3.addWidget(self.frame_6, 4, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 1, 0, 1, 1)
        self.frame_7 = QtWidgets.QFrame(self.centralwidget)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_7)
        font = QtGui.QFont()
        font.setFamily("DejaVu Sans")
        font.setPointSize(64)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.frame_3 = QtWidgets.QFrame(self.frame_7)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.formLayout_2 = QtWidgets.QFormLayout(self.frame_3)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txt_state = QtWidgets.QLineEdit(self.frame_3)
        self.txt_state.setReadOnly(True)
        self.txt_state.setObjectName("txt_state")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_state)
        self.txt_connection = QtWidgets.QLineEdit(self.frame_3)
        self.txt_connection.setReadOnly(True)
        self.txt_connection.setObjectName("txt_connection")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_connection)
        self.label_17 = QtWidgets.QLabel(self.frame_3)
        self.label_17.setObjectName("label_17")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.txt_ipaddress = QtWidgets.QLineEdit(self.frame_3)
        self.txt_ipaddress.setReadOnly(True)
        self.txt_ipaddress.setObjectName("txt_ipaddress")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_ipaddress)
        self.label_16 = QtWidgets.QLabel(self.frame_3)
        self.label_16.setObjectName("label_16")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.horizontalLayout_3.addWidget(self.frame_3)
        self.frame = QtWidgets.QFrame(self.frame_7)
        self.frame.setMaximumSize(QtCore.QSize(105, 101))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.but_connect = QtWidgets.QPushButton(self.frame)
        self.but_connect.setGeometry(QtCore.QRect(10, 10, 85, 26))
        self.but_connect.setObjectName("but_connect")
        self.but_refresh = QtWidgets.QPushButton(self.frame)
        self.but_refresh.setGeometry(QtCore.QRect(10, 40, 85, 26))
        self.but_refresh.setObjectName("but_refresh")
        self.but_initialise = QtWidgets.QPushButton(self.frame)
        self.but_initialise.setGeometry(QtCore.QRect(10, 70, 85, 26))
        self.but_initialise.setObjectName("but_initialise")
        self.horizontalLayout_3.addWidget(self.frame)
        self.gridLayout_3.addWidget(self.frame_7, 0, 0, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame1 = QtWidgets.QFrame(self.frame_4)
        self.frame1.setMaximumSize(QtCore.QSize(226, 16777215))
        self.frame1.setObjectName("frame1")
        self.formLayout = QtWidgets.QFormLayout(self.frame1)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.frame1)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.txt_pulses = QtWidgets.QLineEdit(self.frame1)
        self.txt_pulses.setMinimumSize(QtCore.QSize(55, 0))
        self.txt_pulses.setReadOnly(True)
        self.txt_pulses.setObjectName("txt_pulses")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_pulses)
        self.label_6 = QtWidgets.QLabel(self.frame1)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.txt_repeats = QtWidgets.QLineEdit(self.frame1)
        self.txt_repeats.setMinimumSize(QtCore.QSize(55, 0))
        self.txt_repeats.setReadOnly(True)
        self.txt_repeats.setObjectName("txt_repeats")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_repeats)
        self.label_8 = QtWidgets.QLabel(self.frame1)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.txt_pri_pw = QtWidgets.QLineEdit(self.frame1)
        self.txt_pri_pw.setMinimumSize(QtCore.QSize(55, 0))
        self.txt_pri_pw.setReadOnly(True)
        self.txt_pri_pw.setObjectName("txt_pri_pw")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_pri_pw)
        self.label_10 = QtWidgets.QLabel(self.frame1)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.txt_prepulse = QtWidgets.QLineEdit(self.frame1)
        self.txt_prepulse.setMinimumSize(QtCore.QSize(55, 0))
        self.txt_prepulse.setReadOnly(True)
        self.txt_prepulse.setObjectName("txt_prepulse")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.txt_prepulse)
        self.label_12 = QtWidgets.QLabel(self.frame1)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.txt_x_amp_delay = QtWidgets.QLineEdit(self.frame1)
        self.txt_x_amp_delay.setMinimumSize(QtCore.QSize(55, 0))
        self.txt_x_amp_delay.setReadOnly(True)
        self.txt_x_amp_delay.setObjectName("txt_x_amp_delay")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.txt_x_amp_delay)
        self.label_14 = QtWidgets.QLabel(self.frame1)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.txt_l_amp_delay = QtWidgets.QLineEdit(self.frame1)
        self.txt_l_amp_delay.setMinimumSize(QtCore.QSize(55, 0))
        self.txt_l_amp_delay.setReadOnly(True)
        self.txt_l_amp_delay.setObjectName("txt_l_amp_delay")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.txt_l_amp_delay)
        self.label_15 = QtWidgets.QLabel(self.frame1)
        self.label_15.setObjectName("label_15")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.txt_rex_delay = QtWidgets.QLineEdit(self.frame1)
        self.txt_rex_delay.setMinimumSize(QtCore.QSize(55, 0))
        self.txt_rex_delay.setReadOnly(True)
        self.txt_rex_delay.setObjectName("txt_rex_delay")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.txt_rex_delay)
        self.horizontalLayout.addWidget(self.frame1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.table_pulse_params = QtWidgets.QTableWidget(self.frame_4)
        self.table_pulse_params.setMinimumSize(QtCore.QSize(390, 0))
        self.table_pulse_params.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_pulse_params.setAutoScroll(True)
        self.table_pulse_params.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_pulse_params.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_pulse_params.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.table_pulse_params.setObjectName("table_pulse_params")
        self.table_pulse_params.setColumnCount(4)
        self.table_pulse_params.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_pulse_params.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_pulse_params.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_pulse_params.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_pulse_params.setHorizontalHeaderItem(3, item)
        self.table_pulse_params.horizontalHeader().setDefaultSectionSize(97)
        self.horizontalLayout.addWidget(self.table_pulse_params)
        self.gridLayout_3.addWidget(self.frame_4, 2, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_3.addWidget(self.line_2, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.but_read.setText(_translate("MainWindow", "READ"))
        self.but_override.setText(_translate("MainWindow", "OVERRIDE"))
        self.but_arm_disarm.setText(_translate("MainWindow", "ARM/DISARM"))
        self.but_fire_abort.setText(_translate("MainWindow", "FIRE/ABORT"))
        self.label_2.setText(_translate("MainWindow", "TCU #"))
        self.label.setText(_translate("MainWindow", "STATE"))
        self.label_17.setText(_translate("MainWindow", "ADDRESS"))
        self.label_16.setText(_translate("MainWindow", "CONNECTION"))
        self.but_connect.setText(_translate("MainWindow", "CONNECT"))
        self.but_refresh.setText(_translate("MainWindow", "REFRESH"))
        self.but_initialise.setText(_translate("MainWindow", "INITIALISE"))
        self.label_4.setText(_translate("MainWindow", "PULSES"))
        self.label_6.setText(_translate("MainWindow", "REPEATS"))
        self.label_8.setText(_translate("MainWindow", "PRI PW [μs]"))
        self.label_10.setText(_translate("MainWindow", "PREPULSE [μs]"))
        self.label_12.setText(_translate("MainWindow", "X AMP DELAY [μs]"))
        self.label_14.setText(_translate("MainWindow", "L AMP DELAY [μs]"))
        self.label_15.setText(_translate("MainWindow", "REX DELAY [μs]"))
        item = self.table_pulse_params.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Pulse Width"))
        item = self.table_pulse_params.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "PRI"))
        item = self.table_pulse_params.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Mode"))
        item = self.table_pulse_params.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Frequency"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

