from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6 import QtCharts
from controlwindow import ControlWindow

class MainWindow(QMainWindow):
    def __init__(self, app, connection):
        super().__init__()
        
        self.app = app
        self.connect = connection
        self.setWindowTitle("Rocketify")
        self.controlWindow = ControlWindow()

        # Menu bar and sub menus
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")

        refreshAction = fileMenu.addAction("Refresh")
        quitAction = fileMenu.addAction("Quit")
        disconnectAction = fileMenu.addAction("Disconnect")
        aboutAction = fileMenu.addAction("About")

        quitAction.triggered.connect(self.quitApp)
        refreshAction.triggered.connect(self.refreshPorts)
        disconnectAction.triggered.connect(self.disconnectArduino)
        aboutAction.triggered.connect(self.aboutMe)

        self.label = QLabel("<font color=gray size=40>Attempting to connect to Arduino!</font>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.label)

        self.refreshPorts()

    def disconnectArduino(self):
        if (self.connect.getArduino().is_open):
            self.connect.getArduino().close()
            self.label.setText("<font color=red size=40>Disconnected successfully</font>")
        else:
            pass

    def quitApp(self):
        self.app.quit()

    def refreshPorts(self):
        status = self.connect.connectToPortCode()

        match status:
            case 0:
                portName = self.connect.getPortName()
                string = "Successfully connected to Arduino on port " + portName + "."
                self.label.setText("<font color=green size=40>{}</font>".format(string))

                delayTimer = QTimer(self)
                delayTimer.setSingleShot(True)
                delayTimer.timeout.connect(self.connectControlWindow)
                delayTimer.start(2000)

            case 1:
                self.label.setText("<font color=red size=40>Failed to connect to Arduino" +
                                   " as selected port doesn't exist</font>")
            case 2:
                self.label.setText("<font color=red size=40>Unknown error.</font>")
            case 3:
                self.label.setText("<font color=red size=40>There are no open" +
                                    " ports to connect to.</font>")
            case 4:
                self.label.setText("<font color=red size=40>There are more than one open port." +
                                    " Make sure you only have one Arduino plugged in.</font>")
            case 5:
                self.label.setText("<font color=red size=40>You really fucked" +
                                    " up to get this error.</font>")

    def aboutMe(self):
        print ("not done")

    def connectControlWindow(self):
        self.controlWindow.setConnect(self.connect)
        self.close()
        self.controlWindow.show()

