from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import ui_COcalc
import ctypes
import PatientData
import numpy as np
import sys


class COcalcDialog(QDialog, ui_COcalc.Ui_CO_Calculator):
    def __init__(self, parent=None):
        super(COcalcDialog, self).__init__(parent)
        self.setupUi(self)
        self.timeInterval.setPlainText("2")
        self.HUtoIodineConversion.setPlainText("24")
        self.buttonBox.button(QtGui.QDialogButtonBox.Apply).clicked.connect(self.Apply)
        self.buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.Reset)
        self.patient = PatientData.Patient
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
        self.patient.offset = b
        self.patient.data = a - b
        self.patient.getCoeffs(0)
        self.patient.getR2()
        self.patient.tpeak = self.patient.alpha * self.patient.B
        self.patient.getContData()
        self.patient.getStats()

        self.ui.widget.canvas.ax.clear()
        self.ui.widget.canvas.ax.plot(self.patient.contTimes, self.patient.contData, self.patient.times, self.patient.data, 'bs')
        self.ui.widget.canvas.draw()
        self.ui.lineEdit_24.setText("%.7s" % str(person1.CO))
        self.ui.lineEdit_23.setText("%.7s" % str(person1.AUC))
        self.ui.lineEdit_25.setText("%.7s" % str(person1.R2))

        print(person1.CO)

    def Reset(self, parent=None):
        self.HUvalues.clearContents()
        self.AUC.clear()
        self.alpha.clear()
        self.beta.clear()
        self.t0.clear()
        self.rsquared.clear()
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
        self.patient.B = 0
        self.patient.times = 0
        self.patient.fitdata = 0
        self.patient.R2 = 0
        self.patient.contTimes = 0
        self.patient.contData = 0
        self.patient.AUC = 0
        self.patient.CO = 0




