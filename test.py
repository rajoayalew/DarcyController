from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QSplitter, QLabel, QGridLayout, QHBoxLayout, QApplication
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        totalContainer = QWidget()
        mainButtonBox = QVBoxLayout()

        # Add stretch to make buttons resize automatically

        solenoidHBox1 = QHBoxLayout()
        solenoidHBox2 = QHBoxLayout()
        lineIgniteHBox = QHBoxLayout()
        servoHBox = QHBoxLayout()
        abortHBox = QHBoxLayout()

        solenoidLabel = QLabel("Solenoids")
        lineIgniterLabel = QLabel("Line Cutters and Igniters")
        servoLabel = QLabel("Servo Label")
        abortLabel = QLabel("Aborts and Starts")

        solenoidLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lineIgniterLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        servoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        abortLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        mainButtonBox.addWidget(solenoidLabel)
        mainButtonBox.addLayout(solenoidHBox1)
        mainButtonBox.addLayout(solenoidHBox2)
        mainButtonBox.addWidget(lineIgniterLabel)
        mainButtonBox.addLayout(lineIgniteHBox)
        mainButtonBox.addWidget(servoLabel)
        mainButtonBox.addLayout(servoHBox)
        mainButtonBox.addWidget(abortLabel)
        mainButtonBox.addLayout(abortHBox)

        # Add stretch to make buttons resize automatically


        totalContainer.setLayout(mainButtonBox)
        self.setCentralWidget(totalContainer)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
