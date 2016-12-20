from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
#import QWidget
import ui_COcalcMain
import ctypes
import PatientData
from scipy.optimize import curve_fit

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
class COcalcMain(QMainWindow, ui_COcalcMain.Ui_MainWindow):
    def __init__(self, parent=None):
        super(COcalcMain, self).__init__(parent)
        self.setupUi(self)
        self.timeInterval.setPlainText("2") #want to allow user the option to change this value
        self.HUtoIodineConversion.setPlainText("24")
        self.apply.clicked.connect(self.Apply)
        self.reset.clicked.connect(self.Reset)
        self.patient = PatientData.Patient() #object that holds the data and does the calculations

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

    def Apply(self, parent=None):
        a = []
        allRows = self.HUvalues.rowCount()
        for i in np.arange(0, allRows+1, 1):
            temp = self.HUvalues.item(i,0)
            if temp:
                a.append(float(temp.text()))
        a = np.array(a) #type float

        b = float(self.baselineInput.toPlainText())

        self.patient.baseline = b
        self.patient.data = a - b

        self.patient.getCoeffs()
        self.patient.getR2()
        self.patient.getContData()
        self.patient.getStats()

        self.alpha.setPlainText(str(round(self.patient.alpha, 3)))
        self.beta.setPlainText(str(round(self.patient.beta, 3)))
        #self.t0.setPlainText(str(self.patient.)
        self.cardiacOutput.setPlainText(str(round(self.patient.CO, 3)))
        self.AUC.setPlainText(str(round(self.patient.AUC, 0)))
        self.rsquared.setPlainText(str(round(self.patient.R2, 3)))
        self.peakTime.setPlainText(str(round(self.patient.TTP,3)))
        self.MTT.setPlainText(str(round(self.patient.MTT, 3)))

        # create array of xvalues based on time interval i/p, for plotting later
        t = self.timeInterval.toPlainText()  # type str
        x = np.arange(0, 100, float(t), np.dtype(np.float))  # makes x-axis in terms of entered time intervals.(float i/p)
        xvalues = ([])
        includedx = self.patient.data.size
        for j in np.arange(0, includedx, 1):
            temp2 = x.item(j)
            xvalues.append(temp2)
        xvalues = np.array(xvalues)
        xvalues = xvalues  # + self.patient.shift

        # estimate standard error of CO calculation with monte carlo simulation
        #first calculate residuals & st. dev.
        resids =  np.empty(self.patient.data.size, dtype = float)
        GVvalueDataSet = np.empty(self.patient.data.size, dtype = float)
        for k in np.arange(0, self.patient.data.size, 1):
            #temp3 = self.patient.data.size.item(k)
            GVvalue = self.patient.gammaFunc(xvalues[k], self.patient.A, self.patient.alpha, self.patient.beta)
            GVvalueDataSet[k]=GVvalue
            #GVvalueDataSet.append(GVvalue)
            residValue = self.patient.data[k] - GVvalue
            resids[k] = residValue
        #resids = np.array(resids)
        #GVvalueDataSet = np.array(GVvalue)

        residSD = np.asscalar(np.std(resids, dtype = float))

        #monte carlo
        mcLoops = 100
        fakeDataSet =  np.empty(self.patient.data.size, dtype = float)
        fakeCOs =  np.empty(mcLoops, dtype = float)
        self.times = np.arange(self.patient.shift, self.patient.shift + len(self.patient.data)*2, 2)

        for m in np.arange(0, mcLoops, 1):
            for l in np.arange(0, self.patient.data.size, 1):
                #temp4 = self.patient.data.size.item(l)
                fakeDataPt = np.random.normal(0.0, residSD) + GVvalueDataSet[l]
                fakeDataSet[l] = fakeDataPt
            popt, pcov = curve_fit(self.patient.gammaFunc, self.times, fakeDataSet,maxfev=2000)
            mcA, mcAlpha, mcBeta = popt[0], popt[1], popt[2]
            mcContData = mcA * (self.patient.contTimes ** mcAlpha) * np.exp(-self.patient.contTimes / mcBeta)
            mcAUC = np.trapz([mcContData], x=[self.patient.contTimes])
            Imass = 0.3 * 350 * 75
            fakeCOs[m] = Imass / mcAUC * 24 * 60 / 1000

        fakeDataSD = np.std(fakeCOs)
        self.standardError.setPlainText(str(round(fakeDataSD, 3)))

        #plot patient data and curve fit
        self.plotwidget.axes.clear()
        self.plotwidget.axes.autoscale(enable=True, axis='both', tight=None)
        self.plotwidget.axes.hold(True)
        self.plotwidget.axes.plot(xvalues, self.patient.data, '.', label = 'Patient Data')
        self.plotwidget.axes.plot(self.patient.contTimes, self.patient.contData, '-', label = 'Curve Fit')
        self.plotwidget.axes.legend()

        self.plotwidget.axes.set_title(' ')
        self.plotwidget.axes.set_xlabel('Time (s)')
        self.plotwidget.axes.set_ylabel('Enhancement (HU)')
        #self.plotwidget.axes.set_xticklabels(t) #range(0,xvalues)
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
        self.patient.baseline = 0
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

        self.plotwidget.axes.hold(False)
        clearx = []
        cleary = []
        self.plotwidget.axes.plot(clearx, cleary)
        self.plotwidget.axes.set_title('')
        self.plotwidget.axes.set_xlabel('')
        self.plotwidget.axes.set_ylabel('')
        self.plotwidget.draw()







