import numpy as np
from COUtilities import gammaFunc, getR2, getContData, getStats, GVCurveFit
from scipy.optimize import curve_fit

class Patient:
    def __init__(self):  # makes a Patient object.  Other variables are 0 here but they get filled in in other methods.
        #self.number = 0
        self.data = []
        self.offset = 0 #is this t0?
        self.shift = 0 # what is 'shift'? user input? or time offset calculated from findoffset?
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

    def getCoeffs(self):  # uses the curvefit function to get coeffs.  Takes in the time shift as parameter
        self.times = np.arange(self.shift, self.shift + len(self.data) * 2, 2)
        popt, pcov = curve_fit(gammaFunc, self.times, self.data, maxfev=50000)
        self.A, self.alpha, self.beta = popt[0], popt[1], popt[2]  # popt is the coeff array.

    def getR2(self):  # calculates the R2
        self.fitData = self.A * (self.times ** self.alpha) * np.exp(-self.times / self.beta)
        dataMean = sum(self.data) / len(self.data)
        SStot = sum((self.data - dataMean) ** 2)
        SSres = sum((self.data - self.fitData) ** 2)
        self.R2 = 1 - (SSres / SStot)

    def findOffset(self): #Find the best offset time for the given data
        temp=0
        # NEED to do some checking on the data to make sure that there are values available
        # someting like IF(self.data.len() =0) then exit
        #if (self.data.len() = 0):
        #    exit () #or return()?
        #else:




    def calcCO(self):  #Do the actual CO calculation after the curve fitting is done
        temp=0



