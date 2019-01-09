
'''
A utility to display share sizes for a given risk amount in a trade

@author: Mike Petersen
@creation_date: January 5, 2019
 '''


import os, sys, inspect

from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit, QRadioButton,
                             QPushButton, QApplication, QMainWindow, QInputDialog, 
                             QAction, QErrorMessage, QMessageBox, QFontDialog,
                             QErrorMessage)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from random import randint
from riskman.rr import RiskMan
# pylint: disable=C0103

#!/usr/bin/env python

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)



class RiskManGui(QMainWindow):
    '''A mini app thing'''

    def __init__(self):
        super().__init__()
        self.rm = RiskMan()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.initUI()

    def initUI(self):
        '''GUI Constructor'''

        img='images/riskMask.png'
        x = randint(0,10)
        print(x)
        if x < 8:
            print('setting to money-bag')
            img = 'images/money-bag.png'
        

        self.setWindowIcon(QIcon(img))

        changeStops = QAction(QIcon('images/stop-train.png'), 'Change Stops', self)
        changeStops.setShortcut('Ctrl+t')
        changeStops.setStatusTip('Change the stop amounts to view.')
        changeStops.triggered.connect(self.showDialog)
        
        setFont = QAction(QIcon('images/choose-font.png'),"Set the font", self)
        setFont.setShortcut('Ctrl+f')
        setFont.setStatusTip("Set the font for the main display")
        setFont.triggered.connect(self.showFontDialog)

        menubar = self.menuBar()
        settingsMenu = menubar.addMenu('&Settings')
        settingsMenu.addAction(changeStops)
        settingsMenu.addAction(setFont)

        self.explainString = 'Keep on top?'

        font = QFont()
        font.setPointSize(10)
        font.setFamily('Arial')

        self.explainLbl = QLabel(self.explainString)
        self.explainLbl.setFont(font)

        self.stayOnTop = QRadioButton('Yes')
        self.stayOnTop.setChecked(True)
        self.notOnTop = QRadioButton('No')

        self.explain = QLabel('Risk Amount.')
        self.explain.setFont(font)

        self.risk = QLineEdit('50.00')
        self.risk.setFont(font)
        riskString = self.rm.getrisk(50.00)
        self.display = QLabel(riskString)
        self.display.setFont(font)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.explainLbl, 1, 1)
        grid.addWidget(self.stayOnTop, 2, 1)
        grid.addWidget(self.notOnTop, 3, 1)
        grid.addWidget(self.explain, 4, 1)
        grid.addWidget(self.risk, 5, 1)

        grid.addWidget(self.display, 1, 0, 10, 1)

        container = QWidget()
        container.setLayout(grid)
        self.setCentralWidget(container)

        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Risk Man')

        self.stayOnTop.toggled.connect(lambda: self.btn_clk(
            self.stayOnTop.isChecked(), self.explainLbl))
        self.risk.textChanged.connect(self.changeValue)

        self.show()

    def btn_clk(self, chk, exlbl):
        '''
        Callback from QRadio.isChecked signal from stayOnTop
        '''
        # The Yes button
        if chk:
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(Qt.WindowStaysOnBottomHint)
            self.show()




        # try:
        # # PyInstaller creates a temp folder and stores path in _MEIPASS
        #     base_path = sys._MEIPASS
        # except Exception:
        # base_path = os.path.abspath(".")
        # base_path = os.path.dirname(os.path.abspath(__file__))
        base_path = get_script_dir()

        e = QErrorMessage(self)
        p = os.getcwd()
        pp = os.listdir(p)
        e.showMessage(base_path)


    def changeValue(self, value):
        '''
        Callback from QLineEdit.textChanged signal from risk widget
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
        font.setPointSize(10)

        inputD = QInputDialog()
        inputD.setInputMode(QInputDialog.TextInput)
        inputD.setWindowTitle('Change Stops')
        inputD.setLabelText('Enter a comma seperated list of stop loss amounts:')
        inputD.setTextValue(stopList)
        inputD.setFont(font)

        ok = inputD.exec_()
        text = inputD.textValue()

        if ok:
            ret = self.rm.setStopLimits(text)
            if ret:
                # Cannot seem to pop up a error dialog from here- gets closed 
                # when InputDialog goes
                message = ''
                for msg in ret:
                    message = message + msg + '\n'
                print("now\n", message)
                print("And the result is\n", self.rm.stops)
            if not rm.stops:
                return
            self.changeValue(self.risk.text())

    def showFontDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.display.setFont(font)
            self.explainLbl.setFont(font)
            self.explain.setFont(font)
            self.risk.setFont(font)
            print(font)



def main():
    app = QApplication(sys.argv)
    ex = RiskManGui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

    
