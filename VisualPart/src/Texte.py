import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

app = QApplication(sys.argv)

label = QLabel("Introduction")
label.show()

app.exec_()