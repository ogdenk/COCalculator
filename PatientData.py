import numpy as np
from COUtilities import gammaFunc, getR2, getContData, getStats, GVCurveFit
from scipy.optimize import curve_fit

class Patient:
    def __init__(self):  # makes a 'person' object.  Other variables are 0 here but they get filled in in other methods.
        #self.number = 0
        self.data = 0
        self.offset = 0
        self.shift = 0
        self.A = 0
        self.alpha = 0
        self.beta = 0
        self.times = 0
        self.fitdata = 0
        self.R2 = 0
        self.contTimes = 0 #This holds 'continuous', i.e. higher res times for smooth curve plot
        self.contData = 0 #This holds 'continuous' GV curve data for smooth curve plotting.
        self.AUC = 0
        self.CO = 0
        self.TTP = 0
        self.MTT = 0

    def getCoeffs(self, shift):  # uses the curvefit function to get coeffs.  Takes in the time shift as parameter
        self.shift = shift
        self.times = np.arange(self.shift, self.shift + len(self.data) * 2, 2)
        popt, pcov = curve_fit(self.gammaFunc, self.times, self.data, maxfev=50000)
        self.A, self.alpha, self.B = popt[0], popt[1], popt[2]  # popt is the coeff array

    def getR2(self):  # calculates the R2
        self.fitData = self.A * (self.times ** self.alpha) * np.exp(-self.times / self.B)
        dataMean = sum(self.data) / len(self.data)
        SStot = sum((self.data - dataMean) ** 2)
        SSres = sum((self.data - self.fitData) ** 2)
        self.R2 = 1 - (SSres / SStot)
        # the R2 comparison is just the 11 data points plus 11 new ones,
        # not the 11 old and all the 100's recreated ones right?

    def getContData(self):  # uses the coeffs to make a more continuous dataset
        self.contTimes = np.arange(0, 50, .01)
        self.contData = self.A * (self.contTimes ** self.alpha) * np.exp(-self.contTimes / self.B)

    def getStats(self):  # uses the continous data for AUC and CO, prints out stats
        self.AUC = np.trapz(self.contData, self.contTimes)
        Imass = 0.3 * 350 * 75
        self.CO = Imass / self.AUC * 24 * 60 / 1000

        #print("Patient=%i,offset=%i, A=%.9f, alpha=%f, B=%f,R^2=%f, shift=%f, AUC=%f, CO=%f" % (
        #self.number, self.offset, self.A, self.alpha, self.B, self.R2, self.shift, self.AUC, self.CO))

