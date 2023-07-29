from PySide6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QToolBar
from PySide6.QtCore import Qt, QTimer
from controlwindow import ControlWindow

class MainWindow(QMainWindow):
    def __init__(self, app, connection):
        super().__init__()

        # connect is an instance of the PortController class defined in communications.py
        self.app = app
        self.portConnect = connection
        self.setWindowTitle("Rocketify")
        self.controlWindow = ControlWindow()

        # Menu bar and sub menus
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")

        # All possible actions as part of the file menu
        refreshAction = fileMenu.addAction("Refresh")
        disconnectAction = fileMenu.addAction("Disconnect")
        aboutAction = fileMenu.addAction("About")
        quitAction = fileMenu.addAction("Quit")

        # Links the act of clicking on the action to functions
        quitAction.triggered.connect(self.quitApp)
        refreshAction.triggered.connect(self.refreshPorts)
        disconnectAction.triggered.connect(self.disconnectArduino)
        aboutAction.triggered.connect(self.aboutMe)

        # Initial label on start up
        self.label = QLabel("<font color=gray size=40>Attempting to connect to Arduino!</font>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.label)

        # Checks for ports
        self.refreshPorts()

    def disconnectArduino(self):
        if (self.portConnect.getArduino() == None):
            return

        if (self.portConnect.getArduino().is_open):
            self.portConnect.getArduino().close()
            self.label.setText("<font color=red size=40>Disconnected successfully</font>")
        else:
            pass

    def quitApp(self):
        self.app.quit()

    def refreshPorts(self):
        # PortCode is a function that returns a number indicating connection status
        # PortCode is defined in communications.py
        status = self.portConnect.connectToPortCode()

        match status:
            case 0:
                portName = self.portConnect.getPortName()
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
        self.controlWindow.setConnect(self.portConnect)
        self.close()
        self.controlWindow.show()

