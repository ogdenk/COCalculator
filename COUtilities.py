import numpy as np
from scipy.optimize import curve_fit


def gammaFunc(tau, A, alpha, Beta):  # evaluates the gamma variate function.
    return A * tau ** alpha * np.exp(-tau / Beta)


def GVCurveFit(shift, times, data):  # uses the curvefit function to get coeffs.
    times = np.arange(shift, shift + len(data) * 2, 2)
    popt, pcov = curve_fit(gammaFunc, times, data, maxfev=50000)
    return popt
    #self.A, self.alpha, self.B = popt[0], popt[1], popt[2]  # popt is the coeff array


def getR2(self):  # calculates the R2
    self.fitData = self.A * (self.times ** self.alpha) * np.exp(-self.times / self.Beta)
    dataMean = sum(self.data) / len(self.data)
    SStot = sum((self.data - dataMean) ** 2)
    SSres = sum((self.data - self.fitData) ** 2)
    self.R2 = 1 - (SSres / SStot)

def getContData(self):  # uses the coeffs to make a more continuous dataset
    self.contTimes = np.arange(0, 50, .01)
    self.contData = self.A * (self.contTimes ** self.alpha) * np.exp(-self.contTimes / self.Beta)


def getStats(self):  # uses the continous data for AUC and CO, prints out stats
    self.AUC = np.trapz(self.contData, self.contTimes)
    Imass = 0.3 * 350 * 75
    self.CO = Imass / self.AUC * 24 * 60 / 1000

    print("Patient=%i,offset=%i, A=%.9f, alpha=%f, Beta=%f,R^2=%f, shift=%f, AUC=%f, CO=%f" % (
    self.number, self.offset, self.A, self.alpha, self.Beta, self.R2, self.shift, self.AUC, self.CO))

