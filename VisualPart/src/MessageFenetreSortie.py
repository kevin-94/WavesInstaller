import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


def MessageBox(a):
    app= QApplication(sys.argv)
    fenetre= QWidget()
    msg= QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(a)
    msg.setWindowTitle("Waves")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
    msg.exec_()


   
if __name__ == '__main__':
    MessageBox("Are you sure you went to quit ?")