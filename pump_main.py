import numpy as np
import matplotlib.pyplot as plt

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures

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

        try:  # an example of handling an error
            self.pump.processPumpData(data)
            self.lineEdit_pumpname.setText(self.pump.name)
            self.lineEdit_flowunits.setText(self.pump.flow_unit)
            self.lineEdit_headunits.setText(self.pump.head_unit)
            # self.lineEdit_headcoeff.setText(self.pump.head_coeff)
            # self.lineEdit_efficiencycoeff.setText(self.pump.eff_coeff)
            self.PlotSomething()

            QApplication.restoreOverrideCursor()
        except:
            QApplication.restoreOverrideCursor()
            bad_file()

    def PlotSomething(self):
        y = self.pump.head
        X_lin = self.pump.flow

        rg = LinearRegression()

        # Create quadratic features
        quadratic = PolynomialFeatures(degree=2)
        cubic = PolynomialFeatures(degree=3)
        X_quad = quadratic.fit_transform(X_lin)
        X_cubic = cubic.fit_transform(X_lin)

        # Fit features
        lin_rg = LinearRegression()
        lin_rg.fit(X_lin, y)
        linear_r2 = r2_score(y, lin_rg.predict(X_lin))

        quad_rg = LinearRegression()
        quad_rg.fit(X_quad, y)
        quadratic_r2 = r2_score(y, quad_rg.predict(X_quad))

        cubic_rg = LinearRegression()
        cubic_rg.fit(X_cubic, y)
        cubic_r2 = r2_score(y, cubic_rg.predict(X_cubic))

        # Plot results
        X_range = np.arange(X_lin.min(), X_lin.max(), 1)[:, np.newaxis]
        y_lin_pred = lin_rg.predict(X_range)
        y_quad_pred = quad_rg.predict(quadratic.fit_transform(X_range))
        y_cubic_pred = cubic_rg.predict(cubic.fit_transform(X_range))

        plt.scatter(X_lin, y, label='Training points', color='lightgray')

        plt.plot(X_range, y_lin_pred, label='Linear (d=1), $R^2=%.2f$' % linear_r2, color='blue', lw=2, linestyle=':')

        plt.plot(X_range, y_quad_pred, label='Quadratic (d=2), $R^2=%.2f$' % quadratic_r2, color='red', lw=2,
                 linestyle='-')

        plt.plot(X_range, y_cubic_pred, label='Cubic (d=3), $R^2=%.2f$' % cubic_r2, color='green', lw=2, linestyle='--')

        plt.xlabel('X-Axis')
        plt.ylabel('Y-Axis')
        plt.legend(loc='upper right')
        plt.title("Happy Chart")

        plt.tight_layout()
        plt.show()




        # x=np.linspace(0,6*np.pi,300)
        # y=np.zeros_like(x)
        # for i in range(300):
        #     y[i]=np.exp(-x[i]/5)*np.sin(x[i])
        # plt.plot(x,y)
        # plt.show()
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
