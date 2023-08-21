from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import QIODevice, QTimer, Slot, Signal, QByteArray
from PySide6.QtCore import QObject
import sys
import time

class PortController(QObject):
    statusCodeReceived = Signal(int)

    def __init__(self):
        super().__init__()

        self.arduino = QSerialPort()
        self.portName = None
        self.portList = QSerialPortInfo.availablePorts()
        self.platform = sys.platform
        self.connected = False
        self.message = ""
        self.newData = False

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
            self.tempTimer.start(2000)

        except Exception as error:
            print ("No work")
            print (error)

    def updateConnectionStatus(self):
        if (self.portName == None):
            return 1

        self.updatePortList()
        testList = self.getHumanPortList()

        for port in testList:
            if (self.portName in port):
                return 0

        return 1

    def readConnectMessage(self):
        message = self.receiveData()

        if message == "<pong>":
            self.statusCodeReceived.emit(0)
        elif message != "<pong>":
            self.statusCodeReceived.emit(1)

    def readLine(self):
        message = self.arduino.readAll().data().decode('utf-8').rstrip('\n')
        self.message = message

        if not message:
            print ("empty message")
        print (message)

        return message

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
                    message += (receivedData)
                else:
                    receiveInProgress = False
                    self.newData = True

            elif (receivedData == startMarker):
                receiveInProgress = True

        message += ">"
        print (message)
        self.newData = False

        print ("It took this long to run this function: {}".format(time.time() - start))

        return message

    def writeLine(self, query="<d,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,:,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15>"):
        self.arduino.write(query.encode('utf-8'))

    def getArduino(self):
        return self.arduino

    def getPlatform(self):
        return self.platform

    def getPortName(self):
        return self.portName

    def getHumanPortList(self):
        self.updatePortList()
        return [port.portName() for port in self.portList]
