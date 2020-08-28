import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from src import BasePath


class MainWindow(QMainWindow):
    mainWindowButtonClickedEvent = pyqtSignal(str, str)

    def __init__(self, i_application_version_no):
        super().__init__()

        self._rootWidget = uic.loadUi(BasePath.get_mainWindow_ui_file_path(), self)
        self.set_title(i_application_version_no)

    def get_rootWidget(self):
        return self._rootWidget


    def set_title(self, version):
        self.setWindowTitle('Straßennamen - Dresden - ' + 'v' + str(version))

