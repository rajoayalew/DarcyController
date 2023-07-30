from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSplitter, QLabel
from PySide6.QtCore import QTimer, Qt
from graph import DataGraph

class ControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.connect is initially set to None but at some point will be set to be a PortController()
        self.portConnect = None
        self.setWindowTitle("Control Window")

        self.loadGraph = DataGraph(3, "LC", "Mass (kilograms)", "Time (sec)", "Load Cell Graph")
        self.tempGraph = DataGraph(6, "TC", "Temperature (°F)", "Time (sec)", "Thermocouple Graph")
        self.pressureGraph = DataGraph(6, "PT", "Pressure (atm)", "Time (sec)", "Pressure Transducer Graph")

        # Defines containers and layouts for the ControlWindow
        self.loadContainer = QWidget()
        self.tempContainer = QWidget()
        self.pressureContainer = QWidget()
        self.b1container = QWidget()
        self.b2container = QWidget()
        self.b3container = QWidget()
        self.graphContainer = QWidget()

        self.VBoxGraph = QVBoxLayout()
        self.VBoxButton1 = QVBoxLayout()
        self.VBoxButton2 = QVBoxLayout()
        self.VBoxButton3 = QVBoxLayout()

        # Button used to toggle solenoids, linecutters, and the servos
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

        # Adds all the layouts, charts, and buttons to the application so it can be displayed
        self.loadContainer.setLayout(self.loadGraph.getLayout())
        self.tempContainer.setLayout(self.tempGraph.getLayout())
        self.pressureContainer.setLayout(self.pressureGraph.getLayout())

        self.VBoxButton1.addWidget(solenoid1)
        self.VBoxButton1.addWidget(solenoid2)
        self.VBoxButton1.addWidget(solenoid3)
        self.VBoxButton1.addWidget(solenoid4)
        self.VBoxButton1.addWidget(solenoid5)

        self.VBoxButton2.addWidget(solenoid6)
        self.VBoxButton2.addWidget(solenoid7)
        self.VBoxButton2.addWidget(solenoid8)
        self.VBoxButton2.addWidget(linecutter1)
        self.VBoxButton2.addWidget(linecutter2)

        self.VBoxButton3.addWidget(igniter1)
        self.VBoxButton3.addWidget(servo1)
        self.VBoxButton3.addWidget(servo2)
        self.VBoxButton3.addWidget(servo3)
        self.VBoxButton3.addWidget(servo4)

        self.VBoxGraph.addWidget(self.loadContainer)
        self.VBoxGraph.addWidget(self.tempContainer)
        self.VBoxGraph.addWidget(self.pressureContainer)

        self.b1container.setLayout(self.VBoxButton1)
        self.b2container.setLayout(self.VBoxButton2)
        self.b3container.setLayout(self.VBoxButton3)
        self.graphContainer.setLayout(self.VBoxGraph)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.graphContainer)
        splitter.addWidget(self.b1container)
        splitter.addWidget(self.b2container)
        splitter.addWidget(self.b3container)

        self.setCentralWidget(splitter)

    def setConnect(self, arduino):
        self.portConnect = arduino
        #self.main()

    def readData(self):
        if self.portConnect is not None:
            arduino = self.portConnect.arduino
            data = arduino.readline()
            data = data.decode('utf-8').rstrip('\n')
            print (data)

    def main(self):

        dataTimer = QTimer(self)
        dataTimer.timeout.connect(self.readData)
        dataTimer.start(1000)

