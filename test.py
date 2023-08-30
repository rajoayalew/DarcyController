"""
from communications import OldPortConnection
import time
import random

port = OldPortConnection()
print(port.connectToPort())
file = open("output.txt", "w")
time.sleep(1)
#port.sendHeartbeat()
#time.sleep(0.5)

def generateString():
    starterString = "<d,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,:,"
    values = [1, -1]

    for i in range(1, 16):
        if (i == 15):
            multiplier = random.choice(values)
            starterString += "{}".format(i*multiplier)
            continue

        multiplier = random.choice(values)
        starterString += "{},".format(i*multiplier)

    starterString += ">"
    return starterString

arduino = port.getArduino()

while True:

    if (port.arduino.in_waiting > 0):
        response = arduino.readline().decode('utf-8').rstrip('\n')
        print (response + "\n")
        file.write(response + "\n")
        # port.printLine()

    stringRequest = generateString()
    print (stringRequest + "\n")
    port.arduino.write(stringRequest.encode('utf-8'))
    file.write(stringRequest + "\n")

    #x = input("Enter a message: ")
    #port.arduino.write(x.encode('utf-8'))
    time.sleep(0.25)
"""

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'autosequence.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, Signal, Slot)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform, QDoubleValidator)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QStatusBar, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QDialog)

import json
import os
import copy

class DoubleLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setPlaceholderText("(seconds)")

        doubleValidator = QDoubleValidator()
        self.setValidator(doubleValidator)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        self.count = 1
        self.box = QVBoxLayout()
        self.timings = []
        self.hasBeenLoaded = False
        self.file = None
        self.autoSequenceName = None
        self.fileContent = None
        self.path = "autosequences.json"

        if (not self.autoSequenceFileExists()):
            self.file = open(self.path, "x")
            self.file.close()

        if (self.isEmpty()):
            self.file = open(self.path, "a")
            emptyJSONObject = {}
            json.dump(emptyJSONObject, self.file, indent=4)
            self.content = emptyJSONObject
            self.file.close()

        self.file = open(self.path, "r")
        self.fileContent = json.load(self.file)
        self.file.close()

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        MainWindow.resize(400, 606)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # Defines the GroupBox that holds the area where you choose predetermined autosequences and load them
        self.chooseAutoBox = QGroupBox(self.centralwidget)
        self.chooseAutoBox.setObjectName(u"chooseAutoBox")
        self.chooseAutoBox.setGeometry(QRect(20, 20, 351, 121))

        # The dropdown menu that lists all possible autosequences
        self.loadAuto = QComboBox(self.chooseAutoBox)
        self.loadAuto.setObjectName(u"loadAuto")
        self.loadAuto.setGeometry(QRect(20, 40, 321, 24))
        self.populateLoadBox()
        self.loadAuto.setCurrentIndex(-1)
        self.loadAuto.currentIndexChanged.connect(self.updateAutoSequenceName)

        # The button that loads the selected autosequence in the dropdown
        self.loadButton = QPushButton(self.chooseAutoBox)
        self.loadButton.setObjectName(u"loadButton")
        self.loadButton.setGeometry(QRect(250, 80, 94, 32))

        font = QFont()
        font.setPointSize(8)

        # GroupBox that holds all the timing settings
        self.autoTimingBox = QGroupBox(self.centralwidget)
        self.autoTimingBox.setObjectName(u"autoTimingBox")
        self.autoTimingBox.setEnabled(True)
        self.autoTimingBox.setGeometry(QRect(19, 140, 351, 381))

        # The new timing button that adds a new state setting to the autoTimingBox
        self.addNewTimingButtton = QPushButton(self.autoTimingBox)
        self.addNewTimingButtton.setObjectName(u"addNewTimingButtton")
        self.addNewTimingButtton.setGeometry(QRect(250, 350, 94, 32))
        self.addNewTimingButtton.setFont(font)

        # Defines a ScrollArea that makes it so if there are many settings we can scroll
        # through them
        self.autoScrollTimeBox = QScrollArea(self.autoTimingBox)
        self.autoScrollTimeBox.setObjectName(u"autoScrollTimeBox")
        self.autoScrollTimeBox.setGeometry(QRect(9, 29, 331, 311))
        self.autoScrollTimeBox.setWidgetResizable(True)
        self.autoScrollTimeBox.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.autoScrollTimeBox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Idk what this is but it needs to be the parent of everything
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 331, 311))
        self.scrollAreaWidgetContents.setLayout(self.box)

        # GroupBox that holds a setting
        self.timingBox = QGroupBox()
        self.timingBox.setObjectName(u"timingBox")
        self.timingBox.setGeometry(QRect(10, 0, 311, 61))
        self.timingBox.setFixedSize(311, 61)
        self.timings.append(self.timingBox)
        self.box.addWidget(self.timingBox)

        # A dropdown menu in timingBox that allows someone to choose a sensor
        self.chooseToggleable = QComboBox(self.timingBox)
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")
        self.chooseToggleable.addItem("")

        self.chooseToggleable.setObjectName(u"chooseToggleable")
        self.chooseToggleable.setGeometry(QRect(10, 30, 111, 24))

        # A dropdown menu that allows someone to choose what to set the toggleable
        self.chooseState = QComboBox(self.timingBox)
        self.chooseState.addItem("")
        self.chooseState.addItem("")
        self.chooseState.setObjectName(u"chooseState")
        self.chooseState.setGeometry(QRect(130, 30, 81, 24))
        self.chooseState.setEditable(False)

        # Allows to set how much time until to set something
        self.addTiming = DoubleLineEdit(self.timingBox)
        self.addTiming.setObjectName(u"setTiming")
        self.addTiming.setGeometry(QRect(220, 30, 81, 24))

        # Sets the QScrollArea widget to be the widget with all the group box settings in it
        self.autoScrollTimeBox.setWidget(self.scrollAreaWidgetContents)

        # Save file to json file
        self.saveLoadoutButton = QPushButton(self.centralwidget)
        self.saveLoadoutButton.setObjectName(u"saveLoadoutButton")
        self.saveLoadoutButton.setGeometry(QRect(270, 530, 94, 32))

        # Sets everything to be the central widget of mainwindow
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        #
        self.addNewTimingButtton.clicked.connect(self.newTimingButtonClicked)
        self.saveLoadoutButton.clicked.connect(self.saveLoadoutButtonClicked)
        self.loadButton.clicked.connect(self.loadButtonClicked)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Autosequence", None))

        self.chooseAutoBox.setTitle(QCoreApplication.translate("MainWindow", u"Choose Autosequences", None))
        self.loadButton.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.autoTimingBox.setTitle(QCoreApplication.translate("MainWindow", u"Autosequence Timing", None))
        self.addNewTimingButtton.setText(QCoreApplication.translate("MainWindow", u"Add New Timing", None))
        self.timingBox.setTitle(QCoreApplication.translate("MainWindow", u"Timing 1", None))

        self.chooseToggleable.setItemText(0, QCoreApplication.translate("MainWindow", u"Solenoid 1", None))
        self.chooseToggleable.setItemText(1, QCoreApplication.translate("MainWindow", u"Solenoid 2", None))
        self.chooseToggleable.setItemText(2, QCoreApplication.translate("MainWindow", u"Solenoid 3", None))
        self.chooseToggleable.setItemText(3, QCoreApplication.translate("MainWindow", u"Solenoid 4", None))
        self.chooseToggleable.setItemText(4, QCoreApplication.translate("MainWindow", u"Solenoid 5", None))
        self.chooseToggleable.setItemText(5, QCoreApplication.translate("MainWindow", u"Solenoid 6", None))
        self.chooseToggleable.setItemText(6, QCoreApplication.translate("MainWindow", u"Solenoid 7", None))
        self.chooseToggleable.setItemText(7, QCoreApplication.translate("MainWindow", u"Solenoid 8", None))
        self.chooseToggleable.setItemText(8, QCoreApplication.translate("MainWindow", u"Line Cutter 1", None))
        self.chooseToggleable.setItemText(9, QCoreApplication.translate("MainWindow", u"Line Cutter 2", None))
        self.chooseToggleable.setItemText(10, QCoreApplication.translate("MainWindow", u"Igniter", None))
        self.chooseToggleable.setItemText(11, QCoreApplication.translate("MainWindow", u"Servo 1", None))
        self.chooseToggleable.setItemText(12, QCoreApplication.translate("MainWindow", u"Servo 2", None))
        self.chooseToggleable.setItemText(13, QCoreApplication.translate("MainWindow", u"Servo 3", None))
        self.chooseToggleable.setItemText(14, QCoreApplication.translate("MainWindow", u"Servo 4", None))

        self.chooseState.setItemText(0, QCoreApplication.translate("MainWindow", u"HIGH", None))
        self.chooseState.setItemText(1, QCoreApplication.translate("MainWindow", u"LOW", None))

        self.chooseState.setPlaceholderText("")
        self.addTiming.setText("")
        self.addTiming.setPlaceholderText(QCoreApplication.translate("MainWindow", u"(seconds)", None))
        self.saveLoadoutButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))

    def newTimingButtonClicked(self):

        """
        self.timingBox = QGroupBox(self.scrollAreaWidgetContents)
        self.timingBox.setObjectName(u"timingBox")
        self.timingBox.setGeometry(QRect(10, 0, 311, 61))
        self.chooseToggleable.setGeometry(QRect(10, 30, 111, 24))
        self.chooseState.setGeometry(QRect(130, 30, 81, 24))
        self.addTiming.setGeometry(QRect(220, 30, 81, 24))
        """

        toggleableList = ["Solenoid 1", "Solenoid 2", "Solenoid 3", "Solenoid 4",
                          "Solenoid 5", "Solenoid 6", "Solenoid 7",
                          "Solenoid 8", "Line Cutter 1", "Line Cutter 2", "Igniter",
                          "Servo 1", "Servo 2", "Servo 3", "Servo 4"]

        stateList = ["HIGH", "LOW"]

        self.count += 1
        self.box.addSpacing(10)

        self.newTimingBox = QGroupBox(self.scrollAreaWidgetContents)
        self.newTimingBox.setFixedSize(311, 61)

        self.newChooseToggleable = QComboBox(self.newTimingBox)
        self.newChooseToggleable.addItems(toggleableList)
        self.newChooseToggleable.setGeometry(QRect(10, 30, 111, 24))
        self.newChooseToggleable.setObjectName("chooseToggleable")

        self.newChooseState = QComboBox(self.newTimingBox)
        self.newChooseState.addItems(stateList)
        self.newChooseState.setGeometry(QRect(130, 30, 81, 24))
        self.newChooseState.setObjectName("chooseState")

        self.newAddTiming = DoubleLineEdit(self.newTimingBox)
        self.newAddTiming.setGeometry(QRect(220, 30, 81, 24))
        self.newAddTiming.setObjectName("setTiming")

        self.box.addWidget(self.newTimingBox)
        self.newTimingBox.setTitle("Timing {}  ".format(self.count))
        #elf.newTimingBox.setGeometry(QRect(, 20, 50, 61))
        self.timings.append(self.newTimingBox)

    def loadHelper(self, timingNumber, toggleableName, selectedState, activationTime):

        toggleableList = ["Solenoid 1", "Solenoid 2", "Solenoid 3", "Solenoid 4",
                          "Solenoid 5", "Solenoid 6", "Solenoid 7",
                          "Solenoid 8", "Line Cutter 1", "Line Cutter 2", "Igniter",
                          "Servo 1", "Servo 2", "Servo 3", "Servo 4"]

        stateList = ["HIGH", "LOW"]

        self.box.addSpacing(10)

        self.newTimingBox = QGroupBox(self.scrollAreaWidgetContents)
        self.newTimingBox.setFixedSize(311, 61)

        self.newChooseToggleable = QComboBox(self.newTimingBox)
        self.newChooseToggleable.addItems(toggleableList)
        self.newChooseToggleable.setGeometry(QRect(10, 30, 111, 24))
        self.newChooseToggleable.setObjectName("chooseToggleable")
        self.newChooseToggleable.setCurrentText(toggleableName)

        self.newChooseState = QComboBox(self.newTimingBox)
        self.newChooseState.addItems(stateList)
        self.newChooseState.setGeometry(QRect(130, 30, 81, 24))
        self.newChooseState.setObjectName("chooseState")
        self.newChooseState.setCurrentText(selectedState)

        self.add1 = DoubleLineEdit(self.newTimingBox)
        self.add1.setGeometry(QRect(220, 30, 81, 24))
        self.add1.setObjectName("setTiming")
        self.add1.setText(str(activationTime))

        self.box.addWidget(self.newTimingBox)
        self.newTimingBox.setTitle("Timing {}".format(timingNumber))
        self.timings.append(self.newTimingBox)

    def autoSequenceFileExists(self):
        path = "./autosequences.json"
        checkBool = os.path.isfile(path)
        return (checkBool)

    def updateAutoSequenceName(self):
        self.autoSequenceName = self.loadAuto.currentText()

    def saveLoadoutButtonClicked(self):

        if (self.loadAuto.currentIndex() == -1 or self.loadAuto.currentText() == "New Autosequence"):
            self.saveWindow = saveNewAutosequence()
            self.saveWindow.setWindowModality(Qt.ApplicationModal)
            self.saveWindow.autoSequenceNameSignal.connect(self.updateAutoSequenceAndSave)
            self.saveWindow.show()
        else:
            self.saveLoadout()

    @Slot(str)
    def updateAutoSequenceAndSave(self, name):
        self.autoSequenceName = name
        self.saveLoadout()

    def saveLoadout(self):

        dataToWrite = {
            "autosequenceName": self.autoSequenceName
        }

        for index in range(0, len(self.timings)):
            groupBox = self.timings[index]

            chooseToggleable = groupBox.findChildren(QComboBox, "chooseToggleable")[0]
            chooseState = groupBox.findChildren(QComboBox, "chooseState")[0]
            setTiming = groupBox.findChildren(QLineEdit, "setTiming")[0]
            timing = float(setTiming.text())
            timingNumber = index + 1

            """
            print()
            print(groupBox.title())
            print(chooseToggleable)
            print(chooseState)
            print(setTiming)
            print(timing)
            print(index)
            print()
            """

            timingObject = {
                              "timingNumber": timingNumber,
                              "selectedToggleable": chooseToggleable.currentText(),
                              "selectedState": chooseState.currentText(),
                              "secondsToActivate": timing
                                                                     }

            dataToWrite["timingObject" + str(index)] = timingObject

        keyList = list(self.fileContent.keys())
        idNum = None

        if (len(keyList) == 0):
            idNum = 0
        else:

            if (self.autoSequenceName == None or self.loadAuto.currentText() == "New Autosequence"):
                idNum = int(keyList[-1][2:]) + 1
            else:

                for key in self.fileContent:
                    data = self.fileContent[key]
                    autoSequenceName = data["autosequenceName"]

                    if (autoSequenceName == self.autoSequenceName):
                        idNum = key[2:]

        self.file = open(self.path, "w")
        self.fileContent["id" + str(idNum)] = dataToWrite
        json.dump(self.fileContent, self.file, indent=4)
        self.file.close()

    def populateLoadBox(self):

        if (self.isEmpty()):
            return

        jsonContent = self.fileContent

        for key in jsonContent:
            data = jsonContent[key]
            autoSequenceName = data["autosequenceName"]
            self.loadAuto.addItem(autoSequenceName)

    def loadButtonClicked(self):

        loadAutoItems = [self.loadAuto.itemText(i) for i in range(self.loadAuto.count())]

        if (self.loadAuto.currentIndex() == -1):
            return
        elif ("New Autosequence" not in loadAutoItems):
            self.loadAuto.addItem("New Autosequence")

        self.clear_layout(self.box)
        jsonContent = copy.deepcopy(self.fileContent)
        findAutoSequenceName = self.loadAuto.currentText()

        for key in jsonContent:
            data = jsonContent[key]
            currentAutoSequenceName = data["autosequenceName"]
            index = 0

            if (currentAutoSequenceName == findAutoSequenceName):

                first_key = next(iter(data))
                data.pop(first_key)

                for num in data:
                    timingObject = data["timingObject" + str(index)]
                    timingNumber = timingObject["timingNumber"]
                    toggleableName = timingObject["selectedToggleable"]
                    selectedState = timingObject["selectedState"]
                    activationTime = timingObject["secondsToActivate"]

                    self.loadHelper(timingNumber, toggleableName, selectedState, activationTime)

                    index += 1

        lastGroupBox = self.timings[-1]
        timingName = lastGroupBox.title()
        spaceIndex = timingName.find(" ")
        self.count = int(timingName[spaceIndex+1:])

    def emptyVBoxLayout(self):
        while (self.box.count() > 0):
            item = self.box.takeAt(0)
            print (item)
            widget = item.widget()
            self.box.removeWidget(widget)
            widget.deleteLater()
            self.timings = []

    def clear_layout(self, layout, delete_widgets=True):
        while (layout.count() > 0):

            item = layout.takeAt(0)

            if delete_widgets:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            child_layout = item.layout()
            if child_layout:
                self.clear_layout(child_layout, delete_widgets)
            del item

        self.timings = []

    def isEmpty(self):
        if (os.path.getsize(self.path) == 0):
            return True
        else:
            return False


class saveNewAutosequence(QMainWindow):
    autoSequenceNameSignal = Signal(str)

    def __init__(self, parent=None):
        super().__init__()

        # Make sure that u arent overwriting another autosequence
        # Ensure different names

        self.autoSequenceNameText = None

        self.setWindowTitle("Save Autosequence")
        self.label = QLabel("To save this autosequence, please give it a name.")

        self.groupBox = QGroupBox()
        self.groupBox.setTitle("Set New Autosequence Name:")
        self.lineEdit = QLineEdit()
        groupBoxLayout = QHBoxLayout()
        groupBoxLayout.addWidget(self.lineEdit)
        self.groupBox.setLayout(groupBoxLayout)

        self.pushButton = QPushButton("Save")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.groupBox)
        layout.addWidget(self.pushButton)

        container = QWidget()
        container.setLayout(layout)
        container.setLayout(layout)

        self.pushButton.clicked.connect(self.passAutoSequenceName)
        self.setCentralWidget(container)

    def passAutoSequenceName(self):
        self.autoSequenceNameText = self.lineEdit.text()
        self.autoSequenceNameSignal.emit(self.autoSequenceNameText)
        self.close()

    def closeEvent(self, event):
        super().closeEvent(event)
