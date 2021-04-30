from ruamel.yaml import YAML
import threading
import time
import asyncio
from qasync import QEventLoop, asyncSlot

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setGeometry(400, 400, 1000, 1300)
        MainWindow.setStyleSheet("color: white; background-color:rgb(7, 14, 36)")
        MainWindow.setWindowIcon(QtGui.QIcon("./Resources/StockOut_logo_whitebg.png"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        
        #######################
        # TDA Client ID Input #
        #######################
        self.TDA_client_ID_label = QtWidgets.QLabel(self.centralwidget)
        self.TDA_client_ID_label.setObjectName("TDA_client_ID_label")
        self.TDA_client_ID_label.setText("Enter TD Ameritrade API Client ID here: ")
        self.TDA_client_ID_label.setFont(QFont("Calibri", 14))
        self.TDA_client_ID_label.setStyleSheet("color: white")
        self.TDA_client_ID_label.adjustSize()
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.TDA_client_ID_label)

        self.TDA_client_ID_line = QtWidgets.QLineEdit(self.centralwidget)
        self.TDA_client_ID_line.setObjectName("TDA_client_ID_line")
        self.TDA_client_ID_line.setFixedWidth(600)
        self.TDA_client_ID_line.setFont(QFont("Calibri", 12))
        self.TDA_client_ID_line.setStyleSheet("color: white; background-color:rgb(1, 4, 15)")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.TDA_client_ID_line)

        ######################################
        # TD Ameritrade Account Number Input #
        ######################################
        self.TDA_account_num_label = QtWidgets.QLabel(self.centralwidget)
        self.TDA_account_num_label.setObjectName("TDA_account_num_label")
        self.TDA_account_num_label.setText("Enter your TD Ameritrade Account Number here: ")
        self.TDA_account_num_label.setFont(QFont("Calibri", 14))
        self.TDA_account_num_label.setStyleSheet("color: white")
        self.TDA_account_num_label.adjustSize()
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.TDA_account_num_label)

        self.TDA_account_num_line = QtWidgets.QLineEdit(self.centralwidget)
        self.TDA_account_num_line.setObjectName("TDA_account_num_line")
        self.TDA_account_num_line.setFixedWidth(600)
        self.TDA_account_num_line.setFont(QFont("Calibri", 12))
        self.TDA_account_num_line.setStyleSheet("color: white; background-color:rgb(1, 4, 15)")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.TDA_account_num_line)

        ##########################
        # TD Ameritrade Username #
        ##########################
        self.TDA_username_label = QtWidgets.QLabel(self.centralwidget)
        self.TDA_username_label.setObjectName("TDA_username_label")
        self.TDA_username_label.setText("Enter your TD Ameritrade Username here: ")
        self.TDA_username_label.setFont(QFont("Calibri", 14))
        self.TDA_username_label.setStyleSheet("color: white")
        self.TDA_username_label.adjustSize()
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.TDA_username_label)

        self.TDA_username_line = QtWidgets.QLineEdit(self.centralwidget)
        self.TDA_username_line.setObjectName("TDA_username_line")
        self.TDA_username_line.setFixedWidth(600)
        self.TDA_username_line.setFont(QFont("Calibri", 12))
        self.TDA_username_line.setStyleSheet("color: white; background-color:rgb(1, 4, 15)")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.TDA_username_line)

        ##########################
        # TD Ameritrade Password #
        ##########################
        self.TDA_password_label = QtWidgets.QLabel(self.centralwidget)
        self.TDA_password_label.setObjectName("TDA_password_label")
        self.TDA_password_label.setText("Enter your TD Ameritrade Password here: ")
        self.TDA_password_label.setFont(QFont("Calibri", 14))
        self.TDA_password_label.setStyleSheet("color: white")
        self.TDA_password_label.adjustSize()
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.TDA_password_label)

        self.TDA_password_line = QtWidgets.QLineEdit(self.centralwidget)
        self.TDA_password_line.setObjectName("TDA_password_line")
        self.TDA_password_line.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.TDA_password_line.setFixedWidth(600)
        self.TDA_password_line.setFont(QFont("Calibri", 12))
        self.TDA_password_line.setStyleSheet("color: white; background-color:rgb(1, 4, 15)")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.TDA_password_line)

        ######################
        # Discord Channel ID #
        ######################
        self.discord_channel_label = QtWidgets.QLabel(self.centralwidget)
        self.discord_channel_label.setObjectName("discord_channel_label")
        self.discord_channel_label.setText("Enter your Discord Channel ID here: ")
        self.discord_channel_label.setFont(QFont("Calibri", 14))
        self.discord_channel_label.setStyleSheet("color: white")
        self.discord_channel_label.adjustSize()
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.discord_channel_label)

        self.discord_channel_line = QtWidgets.QLineEdit(self.centralwidget)
        self.discord_channel_line.setObjectName("discord_channel_line")
        self.discord_channel_line.setFixedWidth(600)
        self.discord_channel_line.setFont(QFont("Calibri", 12))
        self.discord_channel_line.setStyleSheet("color: white; background-color:rgb(1, 4, 15)")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.discord_channel_line)

        #################
        # Submit Button #
        #################
        self.submit_button = QtWidgets.QPushButton(self.centralwidget)
        self.setObjectName("submit_button")
        self.submit_button.setText("Submit")
        self.submit_button.setFont(QFont("Calibri", 10))
        self.submit_button.setStyleSheet("color: white; background-color:rgb(1, 4, 15)")
        self.submit_button.adjustSize()
        #self.submit_button.clicked.connect(save_info)
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.submit_button)

        ##############
        # Run Button #
        ##############
        self.run_button = QtWidgets.QPushButton(self.centralwidget)
        self.run_button.setObjectName("run_button")
        self.run_button.setFont(QFont("Calibri", 10))
        self.run_button.setStyleSheet("background-color:rgb(1, 4, 15)")
        self.run_button.adjustSize()
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.run_button)
        
        ################
        # Terminal Box #
        ################
        self.terminal_box = QtWidgets.QTextEdit(self.centralwidget)
        self.terminal_box.setObjectName("textEdit")
        self.terminal_box.setStyleSheet("color: white; background-color: black")
        self.terminal_box.setFont(QFont("Consolas", 11))
        self.terminal_box.moveCursor(QtGui.QTextCursor.Start)
        self.terminal_box.ensureCursorVisible()
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.SpanningRole, self.terminal_box)

        ###############
        # Quit Button #
        ###############
        self.close_button = QtWidgets.QPushButton(self.centralwidget)
        self.close_button.setObjectName("close_button")
        self.close_button.setText("Quit")
        self.close_button.setFont(QFont("Calibri", 10))
        self.close_button.setStyleSheet("color: white; background-color:rgb(1, 4, 15)")
        self.close_button.adjustSize()
        self.close_button.move(850, 1230)
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.close_button)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 163, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("StockOut Setup", "StockOut Setup"))
        self.run_button.setText(_translate("StockOut Setup", "Run"))