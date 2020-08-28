import traceback

from PyQt5 import QtWidgets
import sys

from src import ApplicationController

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        appCtrl = ApplicationController.AppController('0.1')

        sys.exit(app.exec_())
    except:
        traceback.print_exc()