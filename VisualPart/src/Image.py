import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


def Image():
    app= QApplication(sys.argv)
    fenetre= QWidget()
    l1=QLabel()
    l1.setPixmap(QPixmap("Waves.png"))
    l1.setWindowIcon(QIcon())

    fenetre.show()
    sys.exit(app.exec_())
    

    
if __name__ == '__main__':
    Image()