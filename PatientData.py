import numpy as np
from scipy.optimize import curve_fit

class Patient:
    def __init__(self):  # makes a Patient object.  Other variables are 0 here but they get filled in in other methods.
        #self.number = 0
        self.data = np.array([],dtype = float)
        self.baseline = 0 #baseline HU of blood (baseline i/p)
        self.shift = 0 #time shift to shift patient data to fit GV function best
        #self.timeInterval = 0
        self.A = 0
        self.alpha = 0
        self.beta = 0
        self.times = 0 #xdata for curve_fit function.
        self.shiftedTime = 0
        self.shiftedData = 0
        self.fitdata = 0
        self.R2 = 0
        self.contTimes = 0 #This holds 'continuous', i.e. higher res times for smooth curve plot
        self.contData = 0 #This holds 'continuous' GV curve data for smooth curve plotting.
        self.AUC = 0
        self.CO = 0
        self.TTP = 0
        self.MTT = 0
        #self.resids = np.array([], dtype = float)

    def gammaFunc(self, tau, A, alpha, beta):  # evaluates the gamma variate function.
        return A * tau ** alpha * np.exp(-tau / beta)

    def GVCurveFit(self, shift, times, data):  # uses the curvefit function to get coeffs.
        popt, pcov = curve_fit(self.gammaFunc, times, data, maxfev=50000)
        return popt

    def getContData(self):  # uses the coeffs to make a more continuous dataset
        self.contTimes = np.arange(0, 50, .01)
        self.contData = self.A * (self.contTimes ** self.alpha) * np.exp(-self.contTimes / self.beta)

    def getStats(self):  # uses the continous data for AUC and CO, prints out stats
        self.AUC = np.trapz(self.contData, self.contTimes)
        Imass = 0.3 * 350 * 75
        self.CO = Imass / self.AUC * 24 * 60 / 1000
        self.TTP = self.alpha*self.beta
        self.MTT = self.AUC/24/(self.TTP)

    def getCoeffs(self):  # uses the curvefit function to get coeffs.  Takes in the time shift as parameter (0 for now)
        self.findOffset()
        self.times = np.arange(-self.shift, -self.shift + len(self.data) * 2, 2) #shouldn't timeInterval replace '2'?
        #self.times = np.concatenate(([0],self.times))
        #self.data = np.concatenate(([0], self.data))
        index = np.where(self.times >= 0)
        temp = index[0][0]
        self.shiftedTime = self.times[temp:]
        self.shiftedData = self.data[temp:]
        popt, pcov = curve_fit(self.gammaFunc, self.shiftedTime, self.shiftedData, p0 = [2, 2, 2]) #maxfev=50000
        #popt- optimal values for parameters (array), pcov- estimated covariance of popt (2D array)
        self.A, self.alpha, self.beta = popt[0], popt[1], popt[2]  # popt is the coeff array.

    def getR2(self):  # calculates the R2
        length = self.data.size
        self.fitData = self.A * (self.times ** self.alpha) * np.exp(-self.times / self.beta)
        dataMean = sum(self.data) / length
        SStot = sum((self.data - dataMean) ** 2)
        SSres = sum((self.data - self.fitData) ** 2)
        self.R2 = 1 - (SSres / SStot)

    def findOffset(self): #Find the best offset time for the given data
        self.shift = 0
        # NEED to do some checking on the data to make sure that there are values available
        # someting like IF(self.data.len() =0) then exit
        #if (self.data.len() = 0):
        #    exit () #or return()?
        #else:



