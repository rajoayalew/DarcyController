from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QTimer, Qt
from PySide6.QtCharts import QChart, QLineSeries, QChartView, QValueAxis
from PySide6.QtGui import QColor

class ControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.connect is initially set to None but at some point will be set to be a PortController()
        self.portConnect = None
        self.setWindowTitle("Control Window")

        # Defines containers and layouts for the ControlWindow
        self.container = QWidget()
        self.HBox = QHBoxLayout()
        self.VBoxGraph = QVBoxLayout()
        self.VBoxButton1 = QVBoxLayout()
        self.VBoxButton2 = QVBoxLayout()
        self.VBoxButton3 = QVBoxLayout()

        self.HBox.addLayout(self.VBoxGraph)
        self.HBox.addLayout(self.VBoxButton1)
        self.HBox.addLayout(self.VBoxButton2)
        self.HBox.addLayout(self.VBoxButton3)

        # Initializes the charts
        LoadChart = QChart()
        PressureChart = QChart()
        TempChart = QChart()

        # Initialize the X-Axis and the Y-Axis to be put onto the QCharts
        LoadChartXAxis = QValueAxis()
        LoadChartYAxis = QValueAxis()
        LoadChartXAxis.setRange(0, 10)
        LoadChartYAxis.setRange(0, 10)
        LoadChartXAxis.setTickCount(10)
        LoadChartYAxis.setTickCount(10)

        LoadChart.addAxis(LoadChartXAxis, Qt.AlignmentFlag.AlignBottom)
        LoadChart.addAxis(LoadChartYAxis, Qt.AlignmentFlag.AlignLeft)

        # Displays the QChart
        LoadChartView = QChartView(LoadChart)
        PressureChartView = QChartView(PressureChart)
        TempChartView = QChartView(TempChart)

        # Initializing QLineSeries objects which will the ones that take in all the data from the sensors
        engineLoad = QLineSeries()
        tankLoad1 = QLineSeries()
        tankLoad2 = QLineSeries()

        pressureTank1 = QLineSeries()
        pressureTank2 = QLineSeries()
        pressureSys = QLineSeries()
        pressureInject1 = QLineSeries()
        pressureInject2 = QLineSeries()
        pressureChamber = QLineSeries()

        thermoTank = QLineSeries()
        thermoEngine1 = QLineSeries()
        thermoEngine2 = QLineSeries()
        thermoEngine3 = QLineSeries()
        thermoEngine4 = QLineSeries()
        thermoEngine5 = QLineSeries()

        # Set the color of the resulting line
        engineLoad.setColor(QColor("blue"))
        tankLoad1.setColor(QColor("red"))

        # Appends a data point to the QLineSeries
        engineLoad.append(0, 6)
        engineLoad.append(1, 4)
        tankLoad1.append(0, 2)
        tankLoad1.append(1, 5)

        # Attaches Series objects to the QChart instances
        LoadChart.addSeries(engineLoad)
        LoadChart.addSeries(tankLoad1)

        #engineLoad.attachAxis(LoadChartYAxis)
        #engineLoad.attachAxis(LoadChartYAxis)

        #tankLoad1.attachAxis(LoadChartXAxis)
        #tankLoad1.attachAxis(LoadChartYAxis)

        PressureChart.addSeries(pressureTank1)

        TempChart.addSeries(thermoTank)

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

        self.VBoxGraph.addWidget(LoadChartView)
        self.VBoxGraph.addWidget(PressureChartView)
        self.VBoxGraph.addWidget(TempChartView)

        self.container.setLayout(self.HBox)
        self.setCentralWidget(self.container)

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