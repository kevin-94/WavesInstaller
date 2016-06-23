import sys
from PyQt4 import QtGui,QtCore
import urllib
#from time import sleep

config={}
config["tomcat"]=unicode("http://apache.trisect.eu/tomcat/tomcat-9/v9.0.0.M8/bin/apache-tomcat-9.0.0.M8.zip")
config["redis"]=unicode("http://download.redis.io/releases/redis-3.2.1.tar.gz")
config["kafka"]=unicode("https://www.apache.org/dyn/closer.cgi?path=/kafka/0.10.0.0/kafka_2.10-0.10.0.0.tgz")
config["storm"]=unicode("http://www.apache.org/dyn/closer.lua/storm/apache-storm-1.0.1/apache-storm-1.0.1.tar.gz")
config["grafana"]=unicode("https://grafanarel.s3.amazonaws.com/winbuilds/dist/grafana-3.0.4.windows-x64.zip")
config["influx"]=unicode("https://dl.influxdata.com/influxdb/releases/influxdb-0.13.0_linux_amd64.tar.gz")

#############################################################################
class Abort(Exception):
    """classe who stop the download before the end"""
    pass
 
#############################################################################
class Telecharger(QtCore.QThread):
    """Thread of download"""
 
    #========================================================================
    def __init__(self, source, destination, parent=None):
        super(Telecharger,self).__init__(parent)
        
        # Importation of the download
        self.source = source
        
        # Destination of the download
        self.destination = destination
        
        
        self.stop = False
 
    #========================================================================
    def run(self):
        # launching of download
        try:
            filename, msg = urllib.urlretrieve(self.source, self.destination, 
                                                     reporthook=self.infotelech)
            messagefin = u"Download complete Telechargement termine\n\n" + unicode(msg)
        except Abort:
            messagefin = u"Download avort"
            
        # End of the download: message of download
        self.emit(QtCore.SIGNAL("fintelech(PyQt_PyObject)"), messagefin)
 
    #========================================================================
    def infotelech(self, telechbloc, taillebloc, totalblocs):
        """ receive informations about progression of the download"""
        
        # important for stop the download before the end
        if self.stop:
            raise Abort
        # send information about progression to the graphic window
        self.emit(QtCore.SIGNAL("infotelech(PyQt_PyObject)"), 
                                          [telechbloc, taillebloc, totalblocs])
 
    #========================================================================
    def stoptelech(self):
        # permet l'arret du telechargement avant la fin
        self.stop = True


class MainWindow(QtGui.QWidget):
 
    #========================================================================
    def __init__(self, parent=None):  # Constructor of the new window/ Initialization
        super(MainWindow,self).__init__(parent)    # self: Convention
        
    # Characteristic of the main window
    
        self.setGeometry(400,150,500,300)
        self.setFixedSize(500,300) 
        self.setWindowTitle("Waves Installer")
        self.setWindowIcon(QtGui.QIcon ('images/Waves.png'))
    
    # Colors
        
        palette.setColor(QtGui.QPalette.Background,QtCore.Qt.white)
        self.setPalette(palette)
        
 
    # Text
        
        self.configGroup = QtGui.QLabel("Welcome to Waves Installer",self)
        self.qf = QtGui.QFont("",14)
        self.configGroup.setFont(self.qf)
  
        self.label1 = QtGui.QLabel(self)
        self.qf = QtGui.QFont("", 10)
        self.label1.setFont(self.qf)
        #self.label1.setMinimumHeight(5)
        
        
        self.label2 = QtGui.QLabel(u"", self)
        self.qf = QtGui.QFont("", 12, QtGui.QFont.Bold)
        self.label2.setFont(self.qf)
        self.label2.setGeometry(10,100,200,10)
        self.label3= QtGui.QLabel(self)
        self.label3.setPixmap(QtGui.QPixmap('images/Waves.png'))
        
        
    # Buttons
        
        self.next = QtGui.QPushButton("Next", self) 
        self.next.setFixedWidth(100)
        self.next.clicked.connect(self.wrapNext)
 

        self.cancel = QtGui.QPushButton("Cancel", self)
        self.cancel.setFixedWidth(100)
        
        self.cancel.clicked.connect(self.wrapCancel)
        

 
    # Position
        
        posit = QtGui.QGridLayout()
        posit.addWidget(self.configGroup,0,0)
        
        posit.addWidget(self.label1,1,0)
        posit.addWidget(self.label3,2,0,3,2)
        posit.addWidget(self.next, 3,4,)
        posit.addWidget(self.cancel,4,4)
        self.setLayout(posit)        
        
    def wrapNext(self):
        self.win2=SecWindow()
        self.win2.show()
        
    def MessageBox(self,a):
        self.msg= QtGui.QMessageBox()
        self.msg.setIcon(QtGui.QMessageBox.Critical)
        self.msg.setText(a)
        self.msg.setWindowTitle("Waves")
        self.msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
        ret = self.msg.exec_()
        if ret == QtGui.QMessageBox.Yes :
            self.destroy()
            
    def wrapCancel(self):
        self.MessageBox(u"Would you really quit ?")
    
    #========================================================================
    
    def copyFile(self) :
        self.download2.setDisabled( True )
        for i in range( 0, 100 ) :
        # File Copy Code
        # sleep( 0.1 ) is instead of the file copy code
            #self.sleep( 0.1 )
            self.barre.setValue( i + 1 )
            self.qApp.processEvents()

            self.download2.setEnabled( True )
            self.barre.reset()

 


#################################################################################################
class SecWindow(QtGui.QWidget):
    def __init__(self, parent=None):  # Constructor of the new window/ Initialization
        super(SecWindow,self).__init__(parent)    # self: Convention   
    # Main Characteristics
    
        self.setGeometry(400,200,800,400)
        self.setFixedSize(800,400)
        self.setWindowTitle("Waves Installer")
        self.setWindowIcon(QtGui.QIcon ('images/Waves.png'))
        
    # Color 
        palette.setColor(QtGui.QPalette.Background,QtCore.Qt.white)
        self.setPalette(palette)
        
    
    # Button        
        self.download= QtGui.QPushButton("Download",self)
        self.download.setFixedWidth(100)
        self.download.clicked.connect(self.depart_m)
        
        self.finish= QtGui.QPushButton("Finish",self)
        self.finish.setFixedWidth(100)
        self.finish.clicked.connect(self.wrapNext2)
        
        self.back= QtGui.QPushButton("Back",self)
        self.back.setFixedWidth(100)
        self.back.clicked.connect(self.wrapBack)
        
        self.cancel= QtGui.QPushButton("Cancel",self)
        self.cancel.setFixedWidth(100)
        self.cancel.clicked.connect(self.wrapCancel)
        
        
        
        self.TomBtn= QtGui.QPushButton(self)
        self.TomBtn.setFixedWidth(20)
        self.TomBtn.clicked.connect(self.get_dir1)
        self.connect(self.TomBtn, QtCore.SIGNAL("clicked()"),self, QtCore.SLOT("get_dir(1)"))        
        
        self.RedBtn= QtGui.QPushButton(self)
        self.RedBtn.setFixedWidth(20)
        self.RedBtn.clicked.connect(self.get_dir2)
        self.connect(self.RedBtn, QtCore.SIGNAL("clicked()"),self, QtCore.SLOT("get_dir(2)"))
            
        self.KafkaBtn= QtGui.QPushButton(self)
        self.KafkaBtn.setFixedWidth(20)
        self.KafkaBtn.clicked.connect(self.get_dir3)
        self.connect(self.KafkaBtn, QtCore.SIGNAL("clicked()"),self, QtCore.SLOT("get_dir(3)"))
        
        self.StormBtn= QtGui.QPushButton(self)
        self.StormBtn.setFixedWidth(20)
        self.StormBtn.clicked.connect(self.get_dir4)
        self.connect(self.StormBtn, QtCore.SIGNAL("clicked()"),self, QtCore.SLOT("get_dir(4)"))
        
        self.GrafBtn= QtGui.QPushButton(self)
        self.GrafBtn.setFixedWidth(20)
        self.GrafBtn.clicked.connect(self.get_dir5)
        self.connect(self.GrafBtn, QtCore.SIGNAL("clicked()"),self, QtCore.SLOT("get_dir(5)"))
        
        self.InBtn= QtGui.QPushButton(self)
        self.InBtn.setFixedWidth(20)
        self.InBtn.clicked.connect(self.get_dir6)
        self.connect(self.InBtn, QtCore.SIGNAL("clicked()"),self, QtCore.SLOT("get_dir(6)"))
        
    # Label
    
        self.text=QtGui.QLabel(self)
        self.text.setText(" Add to the directory :\ name of file")
        self.qf = QtGui.QFont("", 10)
        self.text.setFont(self.qf)
        
    # CheckBox
        
        self.c1=QtGui.QCheckBox("Tomcat",self)
        self.c2=QtGui.QCheckBox("Redis",self)
        self.c3=QtGui.QCheckBox("Kafka",self)
        self.c4=QtGui.QCheckBox("Apache Storm",self)
        self.c5=QtGui.QCheckBox("Grafana",self)
        self.c6=QtGui.QCheckBox("InfluxDb",self)
        
        
    # QLineEdit
        
        self.l1= QtGui.QLineEdit(self)
        self.l1.setMaximumWidth(500)   
        
        self.l2= QtGui.QLineEdit(self)
        self.l2.setMaximumWidth(500)
        
        
        self.l3= QtGui.QLineEdit(self)
        self.l3.setMaximumWidth(500)
        
        
        self.l4= QtGui.QLineEdit(self)
        self.l4.setMaximumWidth(500)
        
        
        self.l5= QtGui.QLineEdit(self)
        self.l5.setMaximumWidth(500)
        
        
        self.l6= QtGui.QLineEdit(self)
        self.l6.setMaximumWidth(500)
        #
        
    # Progress Bar
    
        self.b1 = QtGui.QProgressBar()
        self.b1.setMinimumWidth( 400 )
        self.b1.setRange( 0, 100 )
        self.b1.setValue(0)
        
        #self.b2 = QtGui.QProgressBar()
        #self.b2.setMinimumWidth( 300 )
        #self.b2.setRange( 0, 100 )
        
        #self.b3 = QtGui.QProgressBar()
        #self.b3.setMinimumWidth( 300 )
        #self.b3.setRange( 0, 100 )
        
        #self.b4 = QtGui.QProgressBar()
        #self.b4.setMinimumWidth( 300 )
        #self.b4.setRange( 0, 100 )
        
        #self.b5 = QtGui.QProgressBar()
        #self.b5.setMinimumWidth( 300 )
        #self.b5.setRange( 0, 100 )
        
        #self.b6 = QtGui.QProgressBar()
        #self.b6.setMinimumWidth( 300 )
        #self.b6.setRange( 0, 100 )
        
        
    # Position
        
        posit = QtGui.QGridLayout()

        
        # Buttons Positions
        
        posit.addWidget(self.download, 2,9)
        posit.addWidget(self.finish,11,11)
        posit.addWidget(self.back,11,8)
        posit.addWidget(self.cancel,11,10)
        

        
        posit.addWidget(self.TomBtn, 1,3)
        posit.addWidget(self.RedBtn, 2,3)
        posit.addWidget(self.KafkaBtn,3,3)
        posit.addWidget(self.StormBtn, 4,3)
        posit.addWidget(self.GrafBtn, 5,3)
        posit.addWidget(self.InBtn, 6,3)
        
        # Label
        
        posit.addWidget(self.text,3,9)
        
        
        # CheckBox Positions
        
        posit.addWidget(self.c1, 1,1)
        posit.addWidget(self.c2,2,1)
        posit.addWidget(self.c3,3,1)
        posit.addWidget(self.c4,4,1)
        posit.addWidget(self.c5,5,1)
        posit.addWidget(self.c6,6,1)
        
        
        # QLineEdit
        
        posit.addWidget(self.l1,1,2)
        posit.addWidget(self.l2,2,2)
        posit.addWidget(self.l3,3,2)
        posit.addWidget(self.l4,4,2)
        posit.addWidget(self.l5,5,2)
        posit.addWidget(self.l6,6,2)  
        
        # Progress Bar
        
        posit.addWidget(self.b1,1,9)
        #posit.addWidget(self.b2,2,5)
        #posit.addWidget(self.b3,3,5)
        #posit.addWidget(self.b4,4,5)
        #posit.addWidget(self.b5,5,5)
        #posit.addWidget(self.b6,6,5)
        
    #layout
        self.setLayout(posit)
        self.setPalette(palette)
    
    
        self.telech = None
        
    def wrapBack(self):
        self.b= MainWindow()
        self.b.show()
        
    def depart_m(self):
        if self.telech==None or not self.telech.isRunning():
            if (self.c1.isChecked() and not self.l1.text()==""):
                
                # initialization of the progress bar
                self.b1.reset()
                self.b1.setRange(0, 100)
                self.b1.setValue(0)
                
                # start the download
                source = config["tomcat"]
                destination = unicode(self.l1.text())
                self.telech = Telecharger(source, destination)
                self.connect(self.telech, QtCore.SIGNAL("infotelech(PyQt_PyObject)"),self.infotelech)
                self.connect(self.telech, QtCore.SIGNAL("fintelech(PyQt_PyObject)"), self.fintelech)
                self.telech.start()
                
            elif (self.c2.isChecked() and not self.l2.text()==""):
                # initialisation de la barre de progression
                self.b2.reset()
                self.b2.setRange(0, 100)
                self.b2.setValue(0)
                # demarre le telechargement
                source = config["redis"]
                destination = unicode(self.l2.text())
                self.telech = Telecharger(source, destination)
                self.connect(self.telech, QtCore.SIGNAL("infotelech(PyQt_PyObject)"),self.infotelech)
                self.connect(self.telech, QtCore.SIGNAL("fintelech(PyQt_PyObject)"), self.fintelech)
                self.telech.start()
                
            elif (self.c3.isChecked() and not self.l3.text()==""):
                # initialisation de la barre de progression
                self.b3.reset()
                self.b3.setRange(0, 100)
                self.b3.setValue(0)
                # demarre le telechargement
                source = config["kafka"]
                destination = unicode(self.l3.text())
                self.telech = Telecharger(source, destination)
                self.connect(self.telech, QtCore.SIGNAL("infotelech(PyQt_PyObject)"),self.infotelech)
                self.connect(self.telech, QtCore.SIGNAL("fintelech(PyQt_PyObject)"), self.fintelech)
                self.telech.start()
                
            elif (self.c4.isChecked() and not self.l4.text()==""):
                # initialisation de la barre de progression
                self.b4.reset()
                self.b4.setRange(0, 100)
                self.b4.setValue(0)
                # demarre le telechargement
                source = config["storm"]
                destination = unicode(self.l4.text())
                self.telech = Telecharger(source, destination)
                self.connect(self.telech, QtCore.SIGNAL("infotelech(PyQt_PyObject)"),self.infotelech)
                self.connect(self.telech, QtCore.SIGNAL("fintelech(PyQt_PyObject)"), self.fintelech)
                self.telech.start()
                
            elif (self.c5.isChecked() and not self.l5.text()==""):
                # initialisation de la barre de progression
                self.b5.reset()
                self.b5.setRange(0, 100)
                self.b5.setValue(0)
                # demarre le telechargement
                source = config["influx"]
                destination = unicode(self.l2.text())
                self.telech = Telecharger(source, destination)
                self.connect(self.telech, QtCore.SIGNAL("infotelech(PyQt_PyObject)"),self.infotelech)
                self.connect(self.telech, QtCore.SIGNAL("fintelech(PyQt_PyObject)"), self.fintelech)
                self.telech.start()
                
            elif (self.c6.isChecked() and not self.l6.text()==""):
                # initialisation de la barre de progression
                self.b6.reset()
                self.b6.setRange(0, 100)
                self.b6.setValue(0)
                # demarre le telechargement
                source = config["redis"]
                destination = unicode(self.l2.text())
                self.telech = Telecharger(source, destination)
                self.connect(self.telech, QtCore.SIGNAL("infotelech(PyQt_PyObject)"),self.infotelech)
                self.connect(self.telech, QtCore.SIGNAL("fintelech(PyQt_PyObject)"), self.fintelech)
                self.telech.start()
        
            
    def infotelech(self, msg):
        """lance a chaque reception d'info sur la progression du telechargement"""
        telechbloc, taillebloc, totalblocs = msg
        if totalblocs > 0:
        # on a la taille maxi: on peut mettre a jour la barre de progression
            p = int(telechbloc*taillebloc/totalblocs*100)
            self.b1.setValue(p)
            QtCore.QCoreApplication.processEvents() # force le rafraichissement
        else:
            # taille maxi inconnue: la barre sera une chenille sans progression
            if self.b1.maximum > 0:
                self.b1.reset()
                self.b1.setRange(0, 0)
    
                
        
 
    #========================================================================
      #========================================================================
    def fintelech(self, msg):
        """Lance quand le thread se termine (normalement ou pas)"""
        QtGui.QMessageBox.information(self,
            u"Telechargement",
            msg)
 
    #========================================================================
    def stop_m(self):
        """demande l'arret du telechargement avant la fin"""
        if self.telech!=None and self.telech.isRunning():
            self.telech.stoptelech()
 
    #========================================================================
    def closeEvent(self, event):
        """lance a la fermeture de la fenetre quelle qu'en soit la methode"""
        self.stop_m() # arrete un eventuel telechargement en cours
        
        event.accept()
    def MessageBox(self,a):
        self.msg= QtGui.QMessageBox()
        self.msg.setIcon(QtGui.QMessageBox.Critical)
        self.msg.setText(a)
        self.msg.setWindowTitle("Waves")
        self.msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
        ret = self.msg.exec_()
        if ret == QtGui.QMessageBox.Yes :
            self.destroy()
            
    def wrapCancel(self):
        self.MessageBox(u"Would you really quit ?")
    def get_dir1(self):
        self.name = unicode(QtGui.QFileDialog.getExistingDirectory(self, 
                     u"Ouverture projet",
                     u".",
                     QtGui.QFileDialog.ShowDirsOnly))
        
        self.l1.setText(self.name)
        
    def get_dir2(self):
        self.name = unicode(QtGui.QFileDialog.getExistingDirectory(self, 
                     u"Ouverture projet",
                     u".",
                     QtGui.QFileDialog.ShowDirsOnly))
        
        self.l2.setText(self.name)
    
  
        
    def get_dir3(self):
        self.name = unicode(QtGui.QFileDialog.getExistingDirectory(self, 
                     u"Ouverture projet",
                     u".",
                     QtGui.QFileDialog.ShowDirsOnly))
        
        self.l3.setText(self.name)
        
    def get_dir4(self):
        self.name = unicode(QtGui.QFileDialog.getExistingDirectory(self, 
                     u"Ouverture projet",
                     u".",
                     QtGui.QFileDialog.ShowDirsOnly))
        
        self.l4.setText(self.name)
    
    def get_dir5(self):
        self.name = unicode(QtGui.QFileDialog.getExistingDirectory(self, 
                     u"Ouverture projet",
                     u".",
                     QtGui.QFileDialog.ShowDirsOnly))
        
        self.l5.setText(self.name)
        
    def get_dir6(self):
        self.name = unicode(QtGui.QFileDialog.getExistingDirectory(self, 
                     u"Ouverture projet",
                     u".",
                     QtGui.QFileDialog.ShowDirsOnly))
        
        self.l6.setText(self.name)
    
    
    
    
    def wrapDir1(self):
        self.get_dir1()
        
    def wrapDir2(self):
        self.get_dir2()
    
    def wrapDir3(self):
        self.get_dir3()
    
    def wrapDir4(self):
        self.get_dir4()
        
    def wrapDir5(self):
        self.get_dir5()
        
    def wrapDir6(self):
        self.get_dir6()
#############################################################################s

    def wrapNext2(self):
        self.win3=ThirdWindow()
        self.win3.show()
        
class ThirdWindow(QtGui.QWidget):

    def __init__(self, parent=None):  
        super(ThirdWindow,self).__init__(parent)   
        
    # Main Characteristics of the Window
        
        self.setGeometry(400,150,600,400)
        self.setFixedSize(600,400)
        self.setWindowTitle("Waves Installer")
        self.setWindowIcon(QtGui.QIcon ('images/Waves.png'))
        
        
    # Color 
        palette.setColor(QtGui.QPalette.Background,QtCore.Qt.white)
        self.setPalette(palette)
        
    # QLabel
    
        self.lab= QtGui.QLabel(self)
        self.lab.setPixmap(QtGui.QPixmap('images/Waves.png'))
        
        
    # Text
    
        self.txt=QtGui.QLabel(self)
        self.txt.setText("")
        self.qf = QtGui.QFont("", 10)
        self.txt.setFont(self.qf)
        
    # Position
    
        posit = QtGui.QGridLayout()
        
        posit.addWidget(self.txt,1,1)
        posit.addWidget(self.lab,3,0)
        
        
    #End
    
        self.setLayout(posit)
        self.setPalette(palette)
        self.show()
    
    
    def MessageBox(self,a):
        self.msg= QtGui.QMessageBox()
        self.msg.setIcon(QtGui.QMessageBox.Critical)
        self.msg.setText(a)
        self.msg.setWindowTitle("Waves")
        self.msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
        ret = self.msg.exec_()
        if ret == QtGui.QMessageBox.Yes :
            self.destroy()
            
    def wrapCancel(self):
        self.MessageBox(u"Would you really quit ?")
                
        
    
        
       
    
if __name__ == "__main__":
    
    # Creation of application object
    app = QtGui.QApplication(sys.argv)
    
    palette = QtGui.QPalette()
    fen = MainWindow()
    fen.show()
    sys.exit(app.exec_())
    
    
