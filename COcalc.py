import COcalcDialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
import sys
#Kent's comment
#test
#another comment
#yet another comment

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = COcalcDialog.COcalcDialog()
    window.show()
    app.exec_()