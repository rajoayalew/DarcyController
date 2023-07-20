import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCharts import QChart, QLineSeries, QChartView, QValueAxis
from PySide6.QtCore import QPointF, Qt, QTimer
from PySide6.QtGui import QPainter
import random

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide6 Chart Example")
        self.setGeometry(100, 100, 680, 500)

        self.show()

        self.create_linechart()

    def create_linechart(self):
        self.series = QLineSeries()
        self.series.append(0, 6)
        self.series.append(2, 4)
        self.series.append(3, 8)
        self.series.append(7, 4)
        self.series.append(10, 5)

        self.series << QPointF(11, 1) << QPointF(13, 3) << QPointF(17, 6) << QPointF(18, 3) << QPointF(20, 2)
        self.series.append(30, 54)

        chart = QChart()
        self.XAxis = QValueAxis()
        self.YAxis = QValueAxis()

        chart.addAxis(self.XAxis, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(self.YAxis, Qt.AlignmentFlag.AlignLeft)

        chart.addSeries(self.series)

        self.series.attachAxis(self.XAxis)
        self.series.attachAxis(self.YAxis)

        #chart.createDefaultAxes()
        chart.setTitle("Line Chart Example")

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartview)

        self.timer = QTimer()
        self.timer.timeout.connect(self.addPoint)
        self.timer.start(5000)

    def addPoint(self):
        maxX = self.XAxis.max()
        maxY = self.YAxis.max()

        x = random.randint(1 + maxX, 100 + maxX)
        y = random.randint(0, 100)

        self.XAxis.setMax(x)

        if (y > maxY):
            self.YAxis.setMax(y)

        self.series.append(x, y)
        print ("Appened values")
        print (x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())