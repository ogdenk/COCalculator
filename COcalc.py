from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
import pyqtgraph as pqg
from pyqtgraph import *
from COcalcMainWindow import COcalcMain
import ui_COcalcMain

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = COcalcMain()
    window.show()
    sys.exit(app.exec_())


