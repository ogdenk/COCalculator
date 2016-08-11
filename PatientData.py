import numpy as np
from COUtilities import gammaFunc, getR2, getContData, getStats, GVCurveFit
from scipy.optimize import curve_fit

class Patient:
    def __init__(self):  # makes a Patient object.  Other variables are 0 here but they get filled in in other methods.
        #self.number = 0
        self.data = 0
        self.offset = 0
        self.shift = 0 # what is 'shift'?
        self.A = 0
        self.alpha = 0
        self.Beta = 0
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
        popt, pcov = curve_fit(gammaFunc, self.times, self.data, maxfev=50000) #removed self. in front of gammaFunc
        self.A, self.alpha, self.Beta = popt[0], popt[1], popt[2]  # popt is the coeff array. changed B's to betas to match line13

    def findOffset(self): #Find the best offset time for the given data
        temp=0
        # NEED to do some checking on the data to make sure that there are values available
        # someting like IF(self.data.len() =0) then exit
        #if (self.data.len() = 0):
        #    exit () #or return()?
        #else:




    def calcCO(self):  #Do the actual CO calculation after the curve fitting is done
        temp=0



