import numpy as np
import matplotlib.pyplot as plt

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from pump_GUI import Ui_Dialog
from pump_class import pump

# this file was created from a modified version of professor Smay's Aero_main_GUI file

class main_window(QDialog, Ui_Dialog):
    def __init__(self):
        '''
        Constructor for main_window.  This is a little different than inheriting from
        QWidgit, though QDialog inherits from QWidgit.
        '''
        super(main_window,self).__init__()
        self.setupUi(self)
        # signals and slots are assigned in this function
        self.assign_widgets()
        self.pump = None  # the primary data element for this program

        # this is part of my failed attempt to get the plot to appear in the main window
        # FigureCanvas = FigureCanvasQTAgg
        # static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        # main_window.addWidget(static_canvas)
        self.show()

    def assign_widgets(self):
        '''
        connect signals and slots
        :return:
        '''
        self.pushButton_exit.clicked.connect(self.ExitApp)
        self.pushButton_readandcalculate.clicked.connect(self.get_pump)

    def get_pump(self):
        # get the filename using the OPEN dialog
        filename = QFileDialog.getOpenFileName()[0]
        if len(filename)==0: 
            no_file()
            return
        self.textEdit_filename.setText(filename)
        # do this in case it takes a long time to read the file
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        # Read the file
        f1 = open(filename, 'r')  # open the file for reading
        data = f1.readlines()  # read the entire file as a list of strings
        f1.close()  # close the file  ... very important

        self.pump = pump()  # create a pump instance (object)

        try:  # attempt execution of operations
            self.pump.processPumpData(data)
            self.lineEdit_pumpname.setText(self.pump.name)
            self.lineEdit_flowunits.setText(self.pump.flow_unit)
            self.lineEdit_headunits.setText(self.pump.head_unit)
            self.lineEdit_headcoeff.setText(np.array2string(self.pump.head_coeff))
            self.lineEdit_efficiencycoeff.setText(np.array2string(self.pump.eff_coeff))
            self.PlotSomething()

            QApplication.restoreOverrideCursor()
        except:
            QApplication.restoreOverrideCursor()
            bad_file()

    def PlotSomething(self):
        # plot given data points for head and efficiency
        plt.scatter(self.pump.flow, self.pump.head, marker='o', color='white', edgecolors='k', label='Head')
        plt.scatter(self.pump.flow, self.pump.efficiency, marker='^', color='white', edgecolors='k', label='Efficiency')

        # data to plot for interpolation functions
        flow_x = np.linspace(self.pump.flow[0], self.pump.flow[-1], num=100)
        head_y = []
        eff_y = []
        for f in flow_x:  # evaluating the 2nd and 3rd order polynomials at flow values in range
            head_y.append(np.polyval(self.pump.head_coeff, f))
            eff_y.append(np.polyval(self.pump.eff_coeff, f))
        plt.plot(flow_x, head_y, linestyle='dashed', color='k', label='Head - Quadratic Fit')  # plotting the two functions
        plt.plot(flow_x, eff_y, linestyle=':', color='k', label='Efficiency - Cubic Fit')

        plt.xlabel('Flow Rate (%s)' %self.pump.flow_unit)
        plt.ylabel('Head (%s)' %self.pump.head_unit)
        plt.legend()
        plt.title('%s' %self.pump.name)

        # plt.tight_layout()
        plt.show()

        # was unable to get the plot to successfully appear inside the main window, so I opted to display it normally
        # as a second window

        return

    def ExitApp(self):
        app.exit()

def no_file():
    msg = QMessageBox()
    msg.setText('There was no file selected')
    msg.setWindowTitle("No File")
    retval = msg.exec_()
    return None

def bad_file():
    msg = QMessageBox()
    msg.setText('Unable to process the selected file')
    msg.setWindowTitle("Bad File")
    retval = msg.exec_()
    return

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main_win = main_window()
    sys.exit(app.exec_())
