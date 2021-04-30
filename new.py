from ruamel.yaml import YAML
import time
import asyncio
import sys
import urllib
import splinter
import discord
import json
import requests
import os
from qasync import QEventLoop, asyncSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from window import Ui_MainWindow

yaml = YAML()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    valueChanged = QtCore.pyqtSignal(int)
    asyncfuncsignal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.valueChanged.connect(self.on_value_changed)
        #self.asyncfuncsignal.connect(self.on_clicked)
        self.run_button.clicked.connect(self.order_function)
        self.close_button.clicked.connect(self.close)
        self.submit_button.setEnabled(False)
        self.discord_channel_line.textChanged.connect(self.disableButton)
        self.submit_button.clicked.connect(self.save_info)

    def order_function(self):
        import order_grabber

    @asyncSlot()
    async def on_clicked(self):
        await self.order_function.start()

    def disableButton(self):
        if len(self.discord_channel_line.text()) > 0:
            self.submit_button.setEnabled(True)

    def save_info(self):
        yaml = YAML()
        data1 = {"TDA_client_ID": (self.TDA_client_ID_line.text()),
        "TDA_account_num": (self.TDA_account_num_line.text()),
        "TDA_username": (self.TDA_username_line.text()),
        "TDA_password": (self.TDA_password_line.text())}
        
        with open("./Config_Files/YAML/config.yml", "w", encoding = "utf-8") as file1:
            yaml.dump(data1, file1)

        data2 = {"Main Channel ID": (self.discord_channel_line.text())}

        with open("./Config_Files/YAML/main_channel_id.yml", "w", encoding = "utf-8") as file2:
            yaml.dump(data2, file2)

    @QtCore.pyqtSlot(int)
    def on_value_changed(self, value):
        self.terminal_box.append("Value: {}".format(value))

    def my_function(self):
        for idx in range(10):
            self.valueChanged.emit(idx)
            print("Executing iteration " + str(idx) + " ...")
            time.sleep(1)  # replaces time-consuming task
        print("Finished!")

def windowLauncher():
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    win = MainWindow()
    win.show()
    loop.run_forever()

if __name__ == "__main__":
    windowLauncher()