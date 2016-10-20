from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
#import QWidget
import ui_COcalc
import ctypes
import PatientData
import COUtilities

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
#from matplotlib import rcParams

import numpy as np
import sys

"""class myTableWidget(QtGui.QTableWidget):

   def keyPressEvent(self,event):
       if(event.key() == QtCore.Qt.Key_Enter):
          self.setCurrentCell(currentRow()+1,currentColumn()) #also currentItem
       else:
           QTableWidget.keyPressEvent(self,event)

#1) create a subclass of QTableWidget that includes your event code
#2) from within Designer, promote your existing QTableWidgets to the new class. All promoted widgets will use
#the subclass's event code, and will still have their properties set correctly as specified by Designer.
#http://stackoverflow.com/questions/5747304/event-catch-only-qt-key-delete
"""
class COcalcDialog(QDialog, ui_COcalc.Ui_CO_Calculator):
    def __init__(self, parent=None):
        super(COcalcDialog, self).__init__(parent)
        self.setupUi(self)
        self.timeInterval.setPlainText("2") #want to allow user the option to change this value
        self.HUtoIodineConversion.setPlainText("24")
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.Apply)
        self.buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.Reset)
        self.patient = PatientData.Patient # this is the object that holds the data and does the calculations
        self.utilities = COUtilities
        """
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
        """
        self.Reset

    def Apply(self, parent=None):
        a = ([])
        allRows = self.HUvalues.rowCount()
        for i in np.arange(0, allRows+1, 1):
            temp = self.HUvalues.item(i,0)
            if (temp):
                a.append([eval(str(temp.text()))])
        a = np.array(a) #type int32

        b = int(self.baselineInput.toPlainText())

        self.patient.offset = b
        self.patient.data = a - b
        self.patient.getCoeffs(0)#TypeError:unbound method getCoeffs() must be called with Patient instance as first argument(got int instance instead)
        self.utilities.getR2(self.utilities)
        self.patient.tpeak = self.patient.alpha * self.patient.beta
        self.utilities.getContData()
        self.patient.calcCO()

        self.alpha.setPlainText(str(self.patient.alpha))
        self.beta.setPlainText(str(self.patient.beta))
        #self.t0.setPlainText(str(self.patient.)
        self.cardiacOutput.setPlainText(str(self.patient.CO))
        self.AUC.setPlainText(str(self.patient.AUC))
        self.rsquared.setPlainText(str(self.patient.R2))
        self.peakTime.setPlainText(str(self.patient.tpeak))
        #print(self.patient.CO)

        self.plotwidget.axes.clear()
        self.plotwidget.axes.autoscale(enable = True, axis = 'both', tight = None)

        #print(self.patient.data.dtype) type int32
        #s = self.patient.data.size #type int
        t = self.timeInterval.toPlainText() #type str
        x = np.arange(0, 100, int(t), np.dtype(np.int32)) #makes x-axis in terms of entered time intervals.(int i/p)
        # have to turn all items into int first (is int ok? if not, linspace is better than arange)
        xvalues = ([])
        includedx = self.patient.data.size
        for j in np.arange(0, includedx+1, 1):
            temp2 = x.item(j)
            if(temp2):
                xvalues.append(temp2)
        xvalues = np.array(xvalues)
        #print(xvalues)

        line1 = self.plotwidget.axes.plot(xvalues, self.patient.data)
        self.plotwidget.axes.legend((line1), ['Patient data'])
        line2 = self.plotwidget.axes.plot(self.patient.contTimes, self.patient.contData, self.patient.times, self.patient.data)
        self.plotwidget.axes.legend((line2), ['Curve Fit'])

        self.plotwidget.axes.set_title([''])
        self.plotwidget.axes.set_xlabel(['Time (s)'])
        self.plotwidget.axes.set_ylabel(['Concentration (Cmg)/I'])
        self.plotwidget.axes.set_xticklabels(t) #range(0,xvalues)
        #self.plotwidget.axes.set_yticklabels()
        self.plotwidget.draw()

    def Reset(self, parent=None):
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

        #self.plotwidget.plt.delaxes()
        clearx = []
        cleary = []
        clearline = self.plotwidget.axes.plot(clearx, cleary)
        self.plotwidget.axes.set_title('')
        self.plotwidget.axes.set_xlabel('')
        self.plotwidget.axes.set_ylabel('')
        self.plotwidget.draw()








