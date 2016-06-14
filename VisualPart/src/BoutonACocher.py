import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


def Bouton_a_cocher():
    
    app= QApplication(sys.argv)
    
    
    #Creation de la case a cocher
    a=QCheckBox("Tomcat")
    
      
    a.show()
    sys.exit(app.exec_())
    

    
if __name__ == '__main__':
    Bouton_a_cocher()
    
        