import numpy as np
from scipy.optimize import curve_fit
import PatientData

#took gammaFunc, GVCurveFit, getContData, getStats and moved to PatientData.py


"""
def getContData(self):  # uses the coeffs to make a more continuous dataset
    PatientData.Patient.contTimes = np.arange(0, 50, .01)
    PatientData.Patient.contData = PatientData.Patient.A * (self.contTimes ** self.alpha) * np.exp(-self.contTimes / self.beta)
    #not sure if we should be calling Patient, PatientData, or making new instance of Patient, patient/patient2

def getStats(self):  # uses the continous data for AUC and CO, prints out stats
    PatientData.Patient.AUC = np.trapz(self.contData, self.contTimes)
    Imass = 0.3 * 350 * 75
    PatientData.Patient.CO = Imass / self.AUC * 24 * 60 / 1000

    print("Patient=%i,offset=%i, A=%.9f, alpha=%f, beta=%f,R^2=%f, shift=%f, AUC=%f, CO=%f" % (
    self.number, self.offset, self.A, self.alpha, self.beta, self.R2, self.shift, self.AUC, self.CO))
"""
