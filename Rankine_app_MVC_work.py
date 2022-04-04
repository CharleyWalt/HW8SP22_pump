import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from Rankine_GUI import Ui_Form
from Rankine_Classes_work import rankineController
from Calc_state import SatPropsIsobar
from Calc_state import UnitConverter as UC

#these imports are necessary for drawing a matplot lib graph on my GUI
#no simple widget for this exists in QT Designer, so I have to add the widget in code.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MainWindow(qtw.QWidget, Ui_Form):
    def __init__(self):
        """
        MainWindow constructor
        """
        super().__init__()  #if you inherit, you generally should run the parent constructor first.
        # Main UI code goes here
        self.setupUi(self)
        self.AssignSlots()
        self.MakeCanvas()
        #A tuple containing the widgets that get updated in the View
        self.widgets = (self.le_H1, self.le_H2, self.le_H3, self.le_H4, self.le_TurbineWork, self.le_PumpWork, self.le_HeatAdded, self.le_Efficiency, self.lbl_SatPropHigh, self.lbl_SatPropLow, self.ax, self.canvas)
        self.otherwidgets = (self.le_PHigh, self.le_PLow, self.le_TurbineInletCondition, self.lbl_PHigh, self.lbl_PLow, self.lbl_H1Units, self.lbl_H2Units, self.lbl_H3Units, self.lbl_H4Units, self.lbl_TurbineWorkUnits, self.lbl_PumpWorkUnits, self.lbl_HeatAddedUnits)
        self.RC=rankineController(self.widgets)  # instantiate a rankineController object
        self.Calculate()
        # a place to store coordinates from last position on graph

        self.oldXData=0.0
        self.oldYData=0.0
        # End main ui code
        self.show()

    def AssignSlots(self):
        """
        Setup signals and slots for my program
        :return:
        """
        self.rb_SI.clicked.connect(self.SetUnits) #edit
        self.rb_English.clicked.connect(self.SetUnits) #edit
        self.btn_Calculate.clicked.connect(self.Calculate)
        self.rdo_Quality.clicked.connect(self.SelectQualityOrTHigh)
        self.rdo_THigh.clicked.connect(self.SelectQualityOrTHigh)
        self.le_PHigh

    def MakeCanvas(self):
        """
        Create a place to make graph of Rankine cycle
        Step 1:  create a Figure object called self.figure
        Step 2:  create a FigureCanvasQTAgg object called self.canvas
        Step 3:  create an axes object for making plot
        Step 4:  add self.canvas to self.gb_Output.layout() which is a grid layout
        :return:
        """
        #Step 1.
        self.figure=Figure(figsize=(4,4),tight_layout=True, frameon=True)
        #Step 2.
        self.canvas=FigureCanvasQTAgg(self.figure)
        #Step 3.
        self.ax = self.figure.add_subplot()
        #Step 4.
        self.widgetsVerticalLayout.addWidget(self.canvas)
        self.canvas.mpl_connect("motion_notify_event", self.mouseMoveEvent)

    #since my main window is a widget, I can customize its events by overriding the default event
    def mouseMoveEvent(self, event):
        self.oldXData=event.xdata if event.xdata is not None else self.oldXData
        self.oldYData=event.ydata if event.ydata is not None else self.oldYData
        self.setWindowTitle('s:{:0.2f} kJ/(kg*K), T:{:0.2f} C'.format(self.oldXData, self.oldYData))

    def Calculate(self):
        #use rankineController to update the model based on user inputs
        self.RC.updateModel((self.le_PHigh, self.le_PLow, self.rdo_Quality, self.le_TurbineInletCondition, self.le_TurbineEff))
        self.le_PLow.editingFinished.connect(self.enter_pressed) 
        self.le_PHigh.editingFinished.connect(self.enter_pressed) 
        self.le_TurbineInletCondition.editingFinished.connect(self.enter_pressed) if self.rdo_THigh.isChecked() else self.le_TurbineInletCondition.text() # P1.2 edit
        
    def SelectQualityOrTHigh(self):
        TSat = self.lbl_SatPropHigh.text()[25:31]  
        self.lbl_TurbineInletCondition.setText(("Turbine Inlet: {} =".format('x'if self.rdo_Quality.isChecked() else 'THigh')))
        self.le_TurbineInletCondition.setText(TSat) 
   
    def SetUnits(self):
        self.RC.updateUnits(self.widgets, self.otherwidgets, SI=self.rb_SI.isChecked())

    def enter_pressed(self):
        self.RC.updateModel((self.le_PHigh, self.le_PLow, self.rdo_Quality, self.le_TurbineInletCondition, self.le_TurbineEff))

#if this module is being imported, this won't run. If it is the main module, it will run.
if __name__== '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Rankine calculator')
    sys.exit(app.exec())