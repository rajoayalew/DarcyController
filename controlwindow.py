from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QSplitter, QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtCore import QTimer, Qt, Slot, Signal
from graph import DataGraph, PopOutWindow

class ControlWindow(QMainWindow):
    def __init__(self, port):
        super().__init__()

        # self.connect is initially set to None but at some point will be set to be a PortController() change later maybe
        self.portConnect = port
        self.setWindowTitle("Control Window")
        self.popOutWindows = {}

        # Creates the DataGraphs with the graph, slider, and button with associated paramters
        self.loadGraph = DataGraph(3, "LC", "Mass (kilograms)", "Time (sec)", "Load Cell Graph", 0)
        self.tempGraph = DataGraph(6, "TC", "Temperature (°F)", "Time (sec)", "Thermocouple Graph", 1)
        self.pressureGraph = DataGraph(6, "PT", "Pressure (atm)", "Time (sec)", "Pressure Transducer Graph", 2)

        # Links the popOutClicked Signal emited by the DataGraph class to handlePopOutClicked method inside this file
        self.loadGraph.popOutClicked.connect(self.handlePopOutClicked)
        self.tempGraph.popOutClicked.connect(self.handlePopOutClicked)
        self.pressureGraph.popOutClicked.connect(self.handlePopOutClicked)

        # Defines containers and layouts for the ControlWindow

        # Each DataGraph must have its own container as layouts cannot be shown by themselves
        # These all are containers or layouts for the graphs
        self.loadContainer = QWidget()
        self.tempContainer = QWidget()
        self.pressureContainer = QWidget()
        self.graphContainer = QWidget()
        self.VBoxGraph = QVBoxLayout()

        # These are the containers/layouts for everything having to do with the buttons
        # Everything will be added to mainButtonBox
        buttonContainer = QWidget()
        mainButtonBox = QVBoxLayout()
        solenoidHBox1 = QHBoxLayout()
        solenoidHBox2 = QHBoxLayout()
        lineIgniteHBox = QHBoxLayout()
        servoHBox = QHBoxLayout()
        abortHBox = QHBoxLayout()

        # These are the labels for each of the button areas controlling a specific thing
        # ex. solenoids/line cutters/etc and are set to None such that we can compensate for
        # how the program looks on different OSes

        solenoidLabel = None
        lineIgniterLabel = None
        servoLabel = None
        abortLabel = None

        if (self.portConnect.getPlatform() == "linux"):
            solenoidLabel = QLabel("<font color=white size=5>Solenoids</font>")
            lineIgniterLabel = QLabel("<font color=white size=5>Line Cutters and Igniters</font>")
            servoLabel = QLabel("<font color=white size=5>Servo Motors</font>")
            abortLabel = QLabel("<font color=white size=5>Aborts and Autosequences</font>")
        elif (self.portConnect.getPlatform() == "win32"):
            solenoidLabel = QLabel("<font color=black size=5>Solenoids</font>")
            lineIgniterLabel = QLabel("<font color=black size=5>Line Cutters and Igniters</font>")
            servoLabel = QLabel("<font color=black size=5>Servo Motors</font>")
            abortLabel = QLabel("<font color=black size=5>Aborts and Autosequences</font>")

        # Sets alignment of the labels to the center of their respective box
        solenoidLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineIgniterLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        servoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        abortLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Creates all the buttons
        solenoid1 = QPushButton("Solenoid 1")
        solenoid2 = QPushButton("Solenoid 2")
        solenoid3 = QPushButton("Solenoid 3")
        solenoid4 = QPushButton("Solenoid 3")
        solenoid5 = QPushButton("Solenoid 5")
        solenoid6 = QPushButton("Solenoid 6")
        solenoid7 = QPushButton("Solenoid 7")
        solenoid8 = QPushButton("Solenoid 8")

        linecutter1 = QPushButton("Line Cutter 1")
        linecutter2 = QPushButton("Line Cutter 1")
        igniter1 = QPushButton("Igniter 1")

        servo1 = QPushButton("Servo 1")
        servo2 = QPushButton("Servo 2")
        servo3 = QPushButton("Servo 3")
        servo4 = QPushButton("Servo 4")

        abortA = QPushButton("Type-A Abort")
        abortB = QPushButton("Type-B Abort")
        autoSequence = QPushButton("Run Autosequence")

        # Adds each button to its respective box
        solenoidHBox1.addWidget(solenoid1)
        solenoidHBox1.addWidget(solenoid2)
        solenoidHBox1.addWidget(solenoid3)
        solenoidHBox1.addWidget(solenoid4)

        solenoidHBox2.addWidget(solenoid5)
        solenoidHBox2.addWidget(solenoid6)
        solenoidHBox2.addWidget(solenoid7)
        solenoidHBox2.addWidget(solenoid8)

        lineIgniteHBox.addWidget(linecutter1)
        lineIgniteHBox.addWidget(linecutter2)
        lineIgniteHBox.addWidget(igniter1)

        servoHBox.addWidget(servo1)
        servoHBox.addWidget(servo2)
        servoHBox.addWidget(servo3)
        servoHBox.addWidget(servo4)

        abortHBox.addWidget(abortA)
        abortHBox.addWidget(abortB)
        abortHBox.addWidget(autoSequence)

        # Final step adds all labels and buttons into one container
        mainButtonBox.addWidget(solenoidLabel)
        mainButtonBox.addLayout(solenoidHBox1)
        mainButtonBox.addLayout(solenoidHBox2)
        mainButtonBox.addWidget(lineIgniterLabel)
        mainButtonBox.addLayout(lineIgniteHBox)
        mainButtonBox.addWidget(servoLabel)
        mainButtonBox.addLayout(servoHBox)
        mainButtonBox.addWidget(abortLabel)
        mainButtonBox.addLayout(abortHBox)
        mainButtonBox.addSpacing(10)

        # Sets the layout of the DataGraph to its respective widget container
        self.loadContainer.setLayout(self.loadGraph.getLayout())
        self.tempContainer.setLayout(self.tempGraph.getLayout())
        self.pressureContainer.setLayout(self.pressureGraph.getLayout())

        # Adds the containers to the main graph layout
        self.VBoxGraph.addWidget(self.loadContainer)
        self.VBoxGraph.addWidget(self.tempContainer)
        self.VBoxGraph.addWidget(self.pressureContainer)

        # Sets the main button/label layout to be the layout of buttonContainer which is a widget container
        buttonContainer.setLayout(mainButtonBox)

        # Does the same thing as above except for graphs
        self.graphContainer.setLayout(self.VBoxGraph)

        # Adds the main graph container and the main button container to the splitter which allows us to
        # resize the amount of the space the graphs and the buttons have
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.graphContainer)
        splitter.addWidget(buttonContainer)

        self.setCentralWidget(splitter)

    @Slot(int)
    def handlePopOutClicked(self, num):
        obj = None
        widget = None

        if (num == 0):
            obj = self.loadGraph
            widget = self.loadContainer
        elif (num == 1):
            obj = self.tempGraph
            widget = self.tempContainer
        elif (num == 2):
            obj = self.pressureGraph
            widget = self.pressureContainer

        self.VBoxGraph.removeWidget(widget)

        if widget not in self.popOutWindows.values():
            self.popOutWindows[num] = PopOutWindow(widget, obj)
            self.popOutWindows[num].sendBackClose.connect(self.handleSendBackWidget)
            self.popOutWindows[num].show()

    @Slot(QWidget)
    def handleSendBackWidget(self, widget):
        self.VBoxGraph.addWidget(widget)

    def setConnect(self, arduino):
        self.portConnect = arduino

    def readData(self):
        if self.portConnect is not None:
            arduino = self.portConnect.arduino
            data = arduino.readline()
            data = data.decode('utf-8').rstrip('\n')
            print (data)
        else:
            print ("Not connect")

    def closeEvent(self, event):
        numOfOpenWindows = len(self.popOutWindows.values())

        if (numOfOpenWindows != 0):
            for i in range(0, numOfOpenWindows):
                self.popOutWindows[i].close()

    def main(self):

        dataTimer = QTimer(self)
        dataTimer.timeout.connect(self.readData)
        dataTimer.start(1000)


