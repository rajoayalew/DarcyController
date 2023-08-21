from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import QIODevice, QTimer, Slot, Signal, QByteArray
from PySide6.QtCore import QObject
import sys
import time
import re

class PortController(QObject):
    statusCodeReceived = Signal(int)
    dataToUpdateGUI = Signal(list)

    def __init__(self):
        super().__init__()

        self.arduino = QSerialPort()
        self.portName = None
        self.portList = QSerialPortInfo.availablePorts()
        self.platform = sys.platform
        self.messageReceived = ""
        self.sentMessage = ""
        self.newData = False
        self.count = 0

        self.tempTimer = QTimer(self)
        self.tempTimer.setSingleShot(True)
        self.tempTimer.timeout.connect(lambda: self.writeLine("<ping>"))

        self.arduino.readyRead.connect(self.readConnectMessage)

    def updatePortList(self):
        self.portList = QSerialPortInfo.availablePorts()

    def connectToPortCode(self):
        self.updatePortList()

        for port in self.portList:
            if (self.platform == "win32"):

                if "Arduino" in port.description():
                    code = self.connectHelper(port)
                    return code

            elif (self.platform == "linux"):

                if "Arduino" in port.manufacturer():
                    code = self.connectHelper(port)
                    return code

            elif (self.platform == "darwin"):
                return 4
            else:
                return 5

        return 6

    def connectToPort(self):
        code = self.connectToPortCode()

        match code:
            case 0:
                return ("Successfuly connected to Arduino on port " + self.portName)
            case 1:
                return ("Arduino is not capable of Darcy communication standard. Please upload the correct program to Arduino")
            case 2:
                return ("Failed to connect to Arduino as selected port doesn't exist")
            case 3:
                return ("Unknown error")
            case 4:
                return ("Get off MacOS")
            case 5:
                return ("You BSD folks will get support in maybe 5 years")
            case 6:
                return ("No Arduino detected. Try unplugging and replugging Arduino into computer")

    def connectHelper(self, passedPort):
        try:
            self.arduino.setPort(passedPort)
            self.arduino.open(QIODevice.OpenModeFlag.ReadWrite)
            self.arduino.setBaudRate(QSerialPort.BaudRate.Baud115200)
            self.portName = passedPort.portName()
            self.tempTimer.start(5000)

        except Exception as error:
            print ("No work")
            print (error)

    def readConnectMessage(self):
        message = self.receiveData()

        if message == "<pong>":
            self.statusCodeReceived.emit(0)
        elif message != "<pong>":
            self.statusCodeReceived.emit(1)

    def updateConnectionStatus(self):
        if (self.portName == None):
            return 1

        self.updatePortList()
        testList = self.getHumanPortList()

        for port in testList:
            if (self.portName in port):
                return 0

        return 1

    def receiveData(self):
        start = time.time()

        message = "<"
        startMarker = "<"
        endMarker = ">"
        receiveInProgress = False

        while (self.arduino.bytesAvailable() > 0 and self.newData == False):
            receivedData = self.arduino.read(1).data().decode('utf-8')

            if (receiveInProgress == True):

                if (receivedData != endMarker):
                    message += receivedData
                else:
                    receiveInProgress = False
                    self.newData = True

            elif (receivedData == startMarker):
                receiveInProgress = True

        message += ">"
        print ("Message below")
        print (message)
        print ("Message above")
        self.messageReceived = message
        self.newData = False

        #print ("It took this long to run this function: {}".format(time.time() - start))

        return message

    def decomposeResponse(self, originalMessage):
        values = []

        # Extract values within <>
        valuesBetweenBracketsSent = re.search(r'<(.*?)>', originalMessage).group(1)

        # Split the values into a list
        originalMessagePins = valuesBetweenBracketsSent.split(',')

        # Find the index of the colon

        colonLocation = originalMessagePins.index(':')

        print ()
        print (originalMessagePins)
        print (colonLocation)
        print ()

        # Extract numeric values before and after the colon
        dataPins = [int(val) for val in originalMessagePins[1:colonLocation] if val.replace('-', '').isdigit()]
        statePins = [int(val) for val in originalMessagePins[colonLocation+1:] if val.replace('-', '').isdigit()]

        ####

        valuesRecievedInBrackets = re.search(r'<(.*?)>', self.messageReceived).group(1)

        # Split the values into a list
        valuesList = valuesRecievedInBrackets.split(',')
        print ()
        print (valuesList)
        print ()

        # Separate numeric and non-numeric values
        dataValues = [int(val) for val in valuesList if val.replace('-', '').isdigit()]
        stateValues = [val for val in valuesList if val in ('PIN_LOW', 'PIN_HIGH')]

        print ()
        print (dataPins)
        print (statePins)
        print (dataValues)
        print (stateValues)
        print ()

        values.append(dataPins)
        values.append(statePins)
        values.append(dataValues)
        values.append(stateValues)

        self.dataToUpdateGUI.emit(values)

    def readWrite(self):
        if (self.count == 0):
            self.writeLine()
            self.count += 1

        originalMessage = self.sentMessage
        self.receiveData()
        self.decomposeResponse(originalMessage)
        self.writeLine()

    def writeLine(self, query="<d,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,:,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15>"):
        self.arduino.write(query.encode('utf-8'))
        self.sentMessage = query
        return query

    def getArduino(self):
        return self.arduino

    def getPlatform(self):
        return self.platform

    def getPortName(self):
        return self.portName

    def getHumanPortList(self):
        self.updatePortList()
        return [port.portName() for port in self.portList]

import serial.tools.list_ports

class OldPortConnection():
    def __init__(self):
        self.arduino = None
        self.portName = None
        self.portList = serial.tools.list_ports.comports()
        self.platform = sys.platform

    def updatePortList(self):
        self.portList = serial.tools.list_ports.comports()

    def connectToPortCode(self):
        self.updatePortList()

        for port in self.portList:
            if (self.platform == "win32"):

                if "Arduino" in port.description:
                    attemptedPort = str(port).split(" ")[0]
                    code = self.connectHelper(attemptedPort)
                    return code

            elif (self.platform == "linux"):

                if "Arduino" in port.manufacturer:
                    attemptedPort = str(port).split(" ")[0]
                    code = self.connectHelper(attemptedPort)
                    return code

            elif (self.platform == "darwin"):
                return 3
            else:
                return 4

        return 5

    def connectToPort(self):
        code = self.connectToPortCode()

        match code:
            case 0:
                return ("Successfuly connected to Arduino on port " + self.portName)
            case 1:
                return ("Failed to connect to Arduino as selected port doesn't exist")
            case 2:
                return ("Unknown error")
            case 3:
                return ("Get off MacOS")
            case 4:
                return ("You BSD folks will get support in maybe 5 years")
            case 5:
                return ("No Arduino detected. Try unplugging and replugging Arduino into computer")

    def connectHelper(self, portName):
        try:
            self.arduino = serial.Serial(port=portName, baudrate=115200, timeout=0.1)
            self.portName = portName
            return 0
        except (FileNotFoundError):
            return 1
        except:
            return 2

    def connectionStatus(self):
        if (self.portName == None):
            return 1

        self.updatePortList()
        testList = self.getHumanPortList()

        for port in testList:
            if (self.portName in port):
                return 0

        return 1

    def printLine(self):
        if (self.connectionStatus() == 0):
            data = self.arduino.readline()
            data = data.decode('utf-8').rstrip('\n')
            print (data)
        else:
            print ("No connection")

    def sendHeartbeat(self):
        numbytes = self.arduino.write('ping'.encode('utf-8'))
        print (numbytes)

    def checkHeartBeat(self):
        response = self.arduino.readline()
        return (response == "pong")

    def getArduino(self):
        return self.arduino

    def getPlatform(self):
        return self.platform

    def getPortName(self):
        return self.portName

    def getPortList(self):
        return self.portList

    def getHumanPortList(self):
        return [str(port).split(" ")[0] for port in list(serial.tools.list_ports.comports())]