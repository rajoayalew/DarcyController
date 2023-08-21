from PySide6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QToolBar
from PySide6.QtCore import Qt, QTimer, Slot, Signal
from controlwindow import ControlWindow
from communications import PortController

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        # connect is an instance of the PortController class defined in communications.py
        self.app = app
        self.portConnect = PortController()
        self.setWindowTitle("Rocketify")

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
        self.portConnect.statusCodeReceived.connect(self.receiveCode)
        self.refreshPorts()

        #tempTimer = QTimer(self)
        #tempTimer.timeout.connect(lambda: self.portConnect.readLine())
        #tempTimer.start(3000)

    def disconnectArduino(self):
        if (self.portConnect.getArduino() == None):
            return

        if (self.portConnect.getArduino().is_open):
            self.portConnect.getArduino().close()
            self.label.setText("<font color=red size=40>Disconnected successfully</font>")
        else:
            pass

    def quitApp(self):

        if (self.portConnect.arduino.isOpen()):
            self.portConnect.arduino.close()

        self.app.quit()

    def refreshPorts(self):
        # PortCode is a function that returns a number indicating connection status
        # PortCode is defined in communications.py
        self.portConnect.connectToPortCode()

        #tempTimer = QTimer(self)
        #tempTimer.timeout.connect(lambda: self.portConnect.writeLine())
        #tempTimer.start(2000)

    @Slot(int)
    def receiveCode(self, code):
        match code:
            case 0:
                portName = self.portConnect.getPortName()
                string = "Successfully connected to Arduino on port " + portName + "."
                self.label.setText("<font color=green size=40>{}</font>".format(string))

                delayTimer = QTimer(self)
                delayTimer.setSingleShot(True)
                delayTimer.timeout.connect(self.connectControlWindow)
                delayTimer.start(2000)
            case 1:
                self.label.setText("<font color=red size=40>Arduino is not capable of Darcy communication" +
                                   " standard. Please upload the correct program to Arduino</font>")
            case 2:
                self.label.setText("<font color=red size=40>Failed to connect to Arduino" +
                                   " as selected port doesn't exist.</font>")
            case 3:
                self.label.setText("<font color=red size=40>Unknown error.</font>")
            case 4:
                self.label.setText("<font color=red size=40>Get off MacOS.</font>")
            case 5:
                self.label.setText("<font color=red size=40>Unsupported OS</font>")
            case 6:
                self.label.setText("<font color=red size=40>No Arduino detected. Try unplugging" +
                                   " and replugging Arduino into computer</font>")

    def aboutMe(self):
        print ("not done")

    def connectControlWindow(self):
        self.controlWindow = ControlWindow(self.portConnect)
        self.close()
        self.controlWindow.show()

