from PySide6.QtWidgets import QVBoxLayout, QScrollBar, QWidget, QPushButton, QMainWindow
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from PySide6.QtCore import Qt, QTimer, Signal, QObject
from random import randint

class RestrictedPlotWidget(PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLimits(xMin=0)  # Set the minimum x-axis limit to 0

    def mouseDragEvent(self, ev):
        if ev.button() == pg.QtCore.Qt.LeftButton:
            if ev.lastPos() is not None:
                # Get the difference in mouse position during dragging
                diff = ev.pos() - ev.lastPos()

                # Check if the new x-axis range will go below the minimum x-axis limit
                if self.getViewBox().viewRange()[0][0] - diff.x() < 0:
                    diff.setX(0)  # Restrict panning to the left of the y-axis

                # Call the original mouseDragEvent with the adjusted position
                ev.accept()
                super().mouseDragEvent(ev.translated(diff))
        else:
            super().mouseDragEvent(ev)

# Functions that may be useful
# graphWidget.setTitle()
# graphWidget.setLabel()

class DataGraph(QObject):
    popOutClicked = Signal(int)

    def __init__(self, numberLines, sensorType, leftAxisName, bottomAxisName, titleName, num, poppedOut=False):
        super().__init__()

        self.graphWidget = RestrictedPlotWidget()
        self.plotItem = self.graphWidget.getPlotItem()
        self.viewBox = self.plotItem.getViewBox()
        self.scrollBar = QScrollBar(Qt.Orientation.Horizontal)
        self.toggleButton = QPushButton("Unlock Graph")
        self.layout = QVBoxLayout()
        self.locked = True
        self.legend = pg.LegendItem(labelTextSize="12pt")
        self.numberLine = numberLines
        self.plots = []
        self.sensorReadings = []
        self.sensorType = sensorType
        self.colors = [(0, 0, 0), (51, 102, 204), (204, 51, 51),
                       (153, 51, 153), (51, 153, 102), (255, 128, 0), (204, 204, 0)]
        self.time = [0]
        self.menu = self.viewBox.getMenu(self)
        self.id = num
        self.popOutAction = None
        self.titleName = titleName
        self.poppedOut = poppedOut

        self.popOutAction = self.menu.addAction("Pop Out")
        self.popOutAction.triggered.connect(self.popOutGraph)
        print (self.poppedOut)

        self.scrollBar.setMinimum(0)
        self.scrollBar.setMaximum(1)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(True)
        self.toggleButton.toggled.connect(self.changeState)

        self.layout.addWidget(self.graphWidget)
        self.layout.addWidget(self.scrollBar)
        self.layout.addWidget(self.toggleButton)

        # I guess better hope we don't have more than 8 sensors because I only coded
        # enough colors for 8
        for i in range(numberLines):
            sensorName = "{} #{}".format(sensorType, i)
            self.sensorReadings.append([0])
            self.plot = self.createPlot(self.time, self.sensorReadings[-1], sensorName, self.colors[i])
            self.legend.addItem(self.plot, sensorName)
            self.plots.append(self.plot)

        self.graphWidget.setBackground("w")
        self.graphWidget.showGrid(x=True, y=True)

        self.graphWidget.setTitle(self.titleName)
        self.graphWidget.setLabel("left", leftAxisName)
        self.graphWidget.setLabel("bottom", bottomAxisName)
        self.legend.setParentItem(self.plotItem)
        self.legend.anchor(itemPos=(1,0), parentPos=(1,0), offset=(-10,10))

        self.scrollBar.valueChanged.connect(self.valueChanged)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def createPlot(self, x, y, plotName, color, symbol="+"):
        pen = pg.mkPen(color=color, width=2)
        line = self.graphWidget.plot(x, y, pen=pen, name=plotName, symbol=symbol, symbolSize=10)
        return line

    def changeState(self):
        self.locked = self.toggleButton.isChecked()

        if (self.toggleButton.isChecked()):
            self.toggleButton.setText("Unlock Graph")
        else:
            self.toggleButton.setText("Lock Graph")

    def update_plot_data(self):
        self.time.append(self.time[-1] + 1)

        for i in range(len(self.plots)):
            self.selectPlot = self.plots[i]
            self.sensorReadings[i].append(randint(-50, 50))
            self.plots[i].setData(self.time, self.sensorReadings[i])

        self.scrollBar.setMaximum(self.time[-1])

        if (self.locked == True):
            self.viewBox.setRange(xRange=(max(self.time)-6, max(self.time)+1))

    def valueChanged(self):
        currentValue = self.scrollBar.value()

        if (self.locked == False):
            self.viewBox.setRange(xRange=(currentValue - 5, currentValue + 5))

    def updateSensorLine(self, sensorNumber, data):
        self.selectPlot = self.plots[sensorNumber]
        self.sensorType[sensorNumber].append(data)
        self.selectPlot.setData(self.time, self.sensorReadings[sensorNumber])

        self.scrollBar.setMaximum(self.time[-1])

        if (self.locked == True):
            self.viewBox.setRange(xRange=(max(self.hour)-6, max(self.hour)+1))

    def popOutGraph(self):
        self.popOutClicked.emit(self.id)

    def switchPopOutAction(self):
        print (self.poppedOut)

        if (self.poppedOut == False):
            self.popOutAction = self.menu.addAction("Pop Out")
            self.popOutAction.triggered.connect(self.popOutGraph)
        else:
            print ("here")
            self.menu.removeAction(self.popOutAction)

    def getLayout(self):
        return self.layout

    def getTitleName(self):
        return self.titleName

class PopOutWindow(QMainWindow):
    sendBackClose = Signal(QWidget)

    def __init__(self, widget, obj):
        super().__init__()

        self.widget = widget
        self.obj = obj
        self.obj.poppedOut = True
        self.obj.switchPopOutAction()

        self.setWindowTitle("Popped Out Graph")
        self.setCentralWidget(self.widget)

    def closeEvent(self, event):
        self.obj.poppedOut = False
        self.obj.switchPopOutAction()
        self.sendBackClose.emit(self.widget)



