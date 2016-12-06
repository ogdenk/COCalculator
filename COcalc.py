import COcalcDialog
import COcalcMainWindow
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
import sys

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    #window = COcalcDialog.COcalcDialog()
    window = COcalcMainWindow.COcalcMain()
    window.show()
    app.exec_()
