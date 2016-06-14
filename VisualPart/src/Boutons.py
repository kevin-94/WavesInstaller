import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def boutons(a,b,c):
    app= QApplication(sys.argv)
    fenetre= QWidget()
    btn=QPushButton(fenetre)
    btn.setText(a)
    btn.setFont(QFont(" Comic sans Ms ",10))
    btn.move(b,c)
    
    fenetre.show()
    sys.exit(app.exec_())
    

    
if __name__ == '__main__':
    boutons("Hello",50,50)
    