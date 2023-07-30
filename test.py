import pyqtgraph as pg
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LegendItem Example")

        # Create a PlotWidget
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.showGrid(x=True, y=True)

        # Add some data to the plot
        self.plot = self.plotWidget.plot([1, 2, 3, 4], [1, 2, 3, 4], pen='b', symbol='o', symbolSize=10)

        # Create a LegendItem and set its anchor position to top-right with an offset of (10, 10) pixels
        self.legend = pg.LegendItem(offset=(10, 10))
        self.plotWidget.addItem(self.legend, anchor=(1, 1), row=0, col=1)

        # Add an item to the legend
        self.legend.addItem(self.plot, "Data")

        # Create a layout and set the plotWidget as the central widget
        layout = QVBoxLayout()
        layout.addWidget(self.plotWidget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
