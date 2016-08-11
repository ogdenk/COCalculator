from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import QtWidgets
import ui_COcalc
import ctypes
import PatientData
import numpy as np
import sys

class myTableWidget(QtGui.QTableWidget):

   def keyPressEvent(self,event):
       if(event.key() == QtCore.Qt.Key_Enter):
          self.setCurrentCell(currentRow()+1,currentColumn()) #also currentItem
       else:
           QTableWidget.keyPressEvent(self,event)

#1) create a subclass of QTableWidget that includes your event code
#2) from within Designer, promote your existing QTableWidgets to the new class. All promoted widgets will use
#the subclass's event code, and will still have their properties set correctly as specified by Designer.
#http://stackoverflow.com/questions/5747304/event-catch-only-qt-key-delete

class COcalcDialog(QDialog, ui_COcalc.Ui_CO_Calculator):
    def __init__(self, parent=None):
        super(COcalcDialog, self).__init__(parent)
        self.setupUi(self)
        self.timeInterval.setPlainText("2") #this will always be 2? or will user possibly change it?
        self.HUtoIodineConversion.setPlainText("24")
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.Apply)
        self.buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.Reset)
        self.patient = PatientData.Patient # this is the object that holds the data and does the calculations
        self.HUvalues = myTableWidget(CO_Calculator)
        self.HUvalues.setGeometry(QtCore.QRect(40, 20, 141, 571))
        self.HUvalues.setMouseTracking(True)
        self.HUvalues.setRowCount(20)
        self.HUvalues.setColumnCount(1)
        self.HUvalues.setObjectName(_fromUtf8("HUvalues"))
        self.HUvalues.horizontalHeader().setVisible(False)
        self.HUvalues.horizontalHeader().setCascadingSectionResizes(False)
        self.HUvalues.verticalHeader().setVisible(True)
        self.HUvalues.verticalHeader().setCascadingSectionResizes(False)
        self.HUvalues.verticalHeader().setSortIndicatorShown(False)
        self.Reset

    def Apply(self, parent=None):
        a = []
        allRows = self.HUvalues.rowCount()
        for i in np.arange(0, allRows+1, 1):
            temp = self.HUvalues.item(i,0)
            if (temp):
                a.append(eval(str(temp.text())))
        a = np.array(a)
        #ctypes.windll.user32.MessageBoxA(0, "Hello!", "test", 1)


        self.patient.data = a
        self.patient.offset = b #error: b not defined. offset = t0
        self.patient.data = a - b #if offset is a value, do we need to make 'b' an array of the same size as 'a' to subtract?
        self.patient.getCoeffs(0)
        self.patient.getR2()
        self.patient.tpeak = self.patient.alpha * self.patient.beta
        self.patient.getContData()
        self.patient.calcCO()

        self.ui.widget.canvas.ax.clear()
        self.ui.widget.canvas.ax.plot(#self.patient.contTimes, self.patient.contData, self.patient.times, self.patient.data, 'bs')
        self.ui.widget.canvas.draw()
        #self.ui.lineEdit_24.setText("%.7s" % str(self.patient.CO))
        #self.ui.lineEdit_23.setText("%.7s" % str(self.patient.AUC))
        #self.ui.lineEdit_25.setText("%.7s" % str(self.patient.R2))

        #print(self.patient.CO)

    def Reset(self, parent=None):
        self.plotwidget.axes.clear()#ax gives error. changed to axes. reset works ok now
        self.HUvalues.clear()
        self.alpha.clear()
        self.beta.clear()
        self.t0.clear()
        self.rsquared.clear()
        self.AUC.clear()
        self.cardiacOutput.clear()
        self.peakTime.clear()
        self.MTT.clear()
        self.standardError.clear()
        self.baselineInput.clear()

        self.patient.number = 0
        self.patient.data = 0
        self.patient.offset = 0
        self.patient.shift = 0
        self.patient.A = 0
        self.patient.alpha = 0
        self.patient.Beta = 0
        self.patient.times = 0
        self.patient.fitdata = 0
        self.patient.R2 = 0
        self.patient.contTimes = 0
        self.patient.contData = 0
        self.patient.AUC = 0
        self.patient.CO = 0




