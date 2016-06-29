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

        for i in np.arange(1, 21, 1):
            temp = self.HUvalues.item(i, 1)

            if (temp.text()):
                a.append(int(temp.text()))
        a = np.array(a)
        print(a)

        ctypes.windll.user32.MessageBoxA(0, "Hello!", "test", 1)

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

        patient.number = 0
        patient.data = 0
        patient.offset = 0
        patient.shift = 0
        patient.A = 0
        patient.alpha = 0
        patient.B = 0
        patient.times = 0
        patient.fitdata = 0
        patient.R2 = 0
        patient.contTimes = 0
        patient.contData = 0
        patient.AUC = 0
        patient.CO = 0




