from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QScrollBar, QWidget, QPushButton
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from PySide6.QtCore import Qt, QTimer
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

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.graphWidget = RestrictedPlotWidget()
        self.plotItem = self.graphWidget.getPlotItem()
        self.viewBox = self.plotItem.getViewBox()
        self.scrollBar = QScrollBar(Qt.Orientation.Horizontal)
        self.toggleButton = QPushButton("Unlock Graph")
        self.container = QWidget()
        self.layout = QVBoxLayout()
        self.locked = True
        self.legend = pg.LegendItem(labelTextSize="12pt", offset=(40, 40))

        self.scrollBar.setMinimum(0)
        self.scrollBar.setMaximum(1)
        self.toggleButton.setCheckable(True)
        self.toggleButton.setChecked(True)
        self.toggleButton.toggled.connect(self.changeState)

        self.layout.addWidget(self.graphWidget)
        self.layout.addWidget(self.scrollBar)
        self.layout.addWidget(self.toggleButton)

        self.hour = [0, 1, 2, 3, 4, 5]
        self.temp1 = [0, 10, 5, -3, 5, 2]
        self.temp2 = [25, 2, 6, 12, 4, -5]
        pen1 = pg.mkPen(color=(255, 0, 0))
        pen2 = pg.mkPen(color=(0, 0, 255))

        self.graphWidget.setBackground("w")
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.setTitle("Temperature Sensors")
        self.graphWidget.setLabel("left", "Temperature (°F)")
        self.graphWidget.setLabel("bottom", "Time (seconds)")
        self.legend.setParentItem(self.plotItem)

        self.line1 = self.graphWidget.plot(self.hour, self.temp1, name="Sensor 1", pen=pen1, symbol='+', symbolSize=10)
        self.line2 = self.graphWidget.plot(self.hour, self.temp2, name="Sensor 2", pen=pen2, symbol='+', symbolSize=10)
        self.legend.addItem(self.line1, "Sensor 1")
        self.legend.addItem(self.line2, "Sensor 2")

        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        self.scrollBar.valueChanged.connect(self.valueChanged)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def plot(self, x, y, plotName, color, symbol):
        pen = pg.mkPen(color=color)
        line = self.graphWidget.plot(x, y, pen=pen, name=plotName, symbol=symbol, symbolSize=10)
        return line

    def changeState(self):
        self.locked = self.toggleButton.isChecked()

        if (self.toggleButton.isChecked()):
            self.toggleButton.setText("Unlock Graph")
        else:
            self.toggleButton.setText("Lock Graph")

    def update_plot_data(self):
        self.hour.append(self.hour[-1] + 1)
        self.temp1.append(randint(-50, 50))
        self.temp2.append(randint(-50, 50))

        self.line1.setData(self.hour, self.temp1)
        self.line2.setData(self.hour, self.temp2)

        self.scrollBar.setMaximum(self.hour[-1])

        if (self.locked == True):
            self.viewBox.setRange(xRange=(max(self.hour)-6, max(self.hour)+1))

    def valueChanged(self):
        currentValue = self.scrollBar.value()

        if (self.locked == False):
            self.viewBox.setRange(xRange=(currentValue - 5, currentValue + 5))

