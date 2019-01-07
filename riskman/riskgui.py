
'''
A utility to display share sizes for a given risk amount in a trade

@author: Mike Petersen
@creation_date: January 5, 2019
 '''


import sys


from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit, QRadioButton,
                             QPushButton, QApplication, QMainWindow, QInputDialog, 
                             QAction, QErrorMessage, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from riskman.rr import RiskMan
# pylint: disable=C0103


class Example(QMainWindow):
    '''A mini app thing'''

    def __init__(self):
        super().__init__()
        self.rm = RiskMan()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.initUI()

    def initUI(self):
        '''GUI Constructor'''

        changeStops = QAction(QIcon('stop-train.png'), 'Change Stops', self)
        changeStops.setShortcut('Ctrl+t')
        changeStops.setStatusTip('Change the stop amounts to view.')
        changeStops.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        settingsMenu = menubar.addMenu('&Settings')
        settingsMenu.addAction(changeStops)

        

        self.explainString = 'Keep Risk Man on top? (Yes or No) \n(Risk Man is currently on top)'

        font = QFont()
        font.setPointSize(12)
        font.setFamily('Arial')

        self.explainLbl = QLabel(self.explainString)
        self.explainLbl.setFont(font)
        self.stayOnTop = QRadioButton('Yes')
        self.notOnTop = QRadioButton('No')
        self.topBtn = QPushButton('Select')

        self.explain = QLabel('Enter the amount you wish to risk.')
        self.explain.setFont(font)
        self.risk = QLineEdit('50.00')
        self.risk.setFont(font)

        riskString = self.rm.getrisk(50.00)
        self.display = QLabel(riskString)

        font.setPointSize(16)
        self.display.setFont(font)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.explainLbl, 1, 0, 3, 1)
        grid.addWidget(self.stayOnTop, 1, 1)
        grid.addWidget(self.notOnTop, 2, 1)
        grid.addWidget(self.topBtn, 3, 1)
        grid.addWidget(self.explain, 4, 0)
        grid.addWidget(self.risk, 5, 0)
        grid.addWidget(self.display, 6, 0, 10, 1)

        container = QWidget()
        # self.setLayout(grid)

        container.setLayout(grid)
        self.setCentralWidget(container)




        self.setGeometry(300, 300, 550, 300)
        self.setWindowTitle('Risk Man')

        self.topBtn.clicked.connect(lambda: self.btn_clk(
            self.stayOnTop.isChecked(), self.explainLbl))
        self.risk.textChanged.connect(self.changeValue)

        self.show()

    def btn_clk(self, chk, exlbl):
        '''
        Callback from isChecked signal from topBtn
        '''
        if chk:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            exlbl.setText(
                'Choose yes or no  to keep Risk Mon on top?\n(Risk Man is currently on top)')
            self.show()
        else:
            self.setWindowFlags(Qt.WindowStaysOnBottomHint)
            exlbl.setText(
                'Choose yes or no  to keep Risk Mon on top?\n(Risk Man is not currently on top)')
            self.show()

    def changeValue(self, value):
        '''
        Callback from textChanged signal from risk widget
        '''
        print(f"Got it at {value}, {type(value)}")
        try:
            fval = float(value)
            self.display.setText(self.rm.getrisk(fval))

        except ValueError:
            pass

    def showDialog(self):
        '''
        Using QInputDialog. If more user interaction of any kind is required, have
        to create our own Widget. This dialog presents an edit box containing the current
        list of stops. User can edit the list to change which stops are displayed.
        '''
        rm = self.rm
        stopList = rm.getStops()

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)

        inputD = QInputDialog()
        inputD.setInputMode(QInputDialog.TextInput)
        inputD.setWindowTitle('Change Stops')
        inputD.setLabelText('Enter a comma seperated list of stop loss amounts:')
        inputD.setTextValue(stopList)
        inputD.setFont(font)

        ok = inputD.exec_()
        text = inputD.textValue()
        # text, ok = inputD.getText(self);



        # text, ok = inputD.getText(self, "Change Stops",
        #                           'Enter a comma seperated list of stop loss amounts',
        #                           QLineEdit.Normal,
        #                           stopList);

        if ok:
            print('so far got', text)
            ret = self.rm.setStopLimits(text)
            if ret:
                #Cannot seem to pop up a error dialog- gets closed when InputDialog goes
                message = ''
                for msg in ret:
                    message = message + msg + '\n'
                print("now\n", message)
                print("And the result is\n", self.rm.stops)
            if not rm.stops:
                return
            self.changeValue(self.risk.text())

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

    
