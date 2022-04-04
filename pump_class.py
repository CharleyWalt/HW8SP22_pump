import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# this file was created from a modified version of professor Smay's Wing_Class file

class pump:
    def __init__(self,):
        '''
        Constructor for the pump class.
        '''
        self.name = None
        self.flow_unit = None
        self.head_unit = None
        self.head = []
        self.flow = []
        self.efficiency = []
        self.head_coeff = []
        self.eff_coeff = []


    def processPumpData(self,data):
        '''
        data is a list of strings (i.e., the lines read from a file)
        :param data:
        :return:
        '''

        l = 0  # iterator for the line number in the loop
        #  work on the assumption that line 0 is name, line 1 is the data types, line 2 is units, and remaining are data
        #  not making assumptions about which data is in which columns
        for line in data:  # loop over all the lines
            line = line.strip()  # first, strip all leading and trailing blank spaces
            if l == 0:
                self.name = line  # always assign first line as name of pump
            elif l == 1:  # this line always assumes to have the data column headers
                cells = line.split()  # split using a whitespace delimiter
                col = 0
                for cell in cells:  # iterating through each item in line 1
                    if cell == 'flow' or cell == 'flowrate':  # accounting for some slight variability in terminology
                        flow_col = col  # assigning column numbers to an identifying variable for use on following lines
                    elif cell == 'head':
                        head_col = col
                    elif cell == 'efficiency' or cell == 'eff':
                        eff_col = col
                    col += 1
            elif l == 2:  # this line always assumes to have the data units
                cells = line.split()
                self.flow_unit = cells[flow_col]
                self.head_unit = cells[head_col]
            else:  # always assuming that lines greater than 2 only contain data corresponding to the known headers
                cells = line.split()
                self.head.append(float(cells[head_col]))
                self.flow.append(float(cells[flow_col]))
                self.efficiency.append(float(cells[eff_col]))
            l += 1

        # calculate polynomial coefficients
        print(self.head)
        print(self.flow)
        print(self.efficiency)
        self.head_coeff = np.polyfit(self.flow, self.head, 2)
        self.eff_coeff = np.polyfit(self.flow, self.efficiency, 3)
        print(self.head_coeff)
        print(self.eff_coeff)
