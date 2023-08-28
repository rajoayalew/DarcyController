from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import QIODevice, QTimer, Slot, Signal, QByteArray
from PySide6.QtCore import QObject
import sys
import time
import re

"""
PortController is the way that the program communicates with the Arduino

Sensors and Toggleables:

    s1 = 1;
    s2 = 2;
    s3 = 3;
    s4 = 4;
    s5 = 5;
    s6 = 6;
    s7 = 7;
    s8 = 8;
    lc1 = 9;
    lc2 = 10;
    igniter = 11;
    servo1 = 12;
    servo2 = 13;
    servo3 = 14;
    servo4 = 15;

    loadCell0 = 0
    loadCell1 = 1
    loadCell2 = 2
    temp0 = 3
    temp1 = 4
    temp2 = 5
    temp3 = 6
    temp4 = 7
    temp5 = 8
    pressure1 = 9
    pressure2 = 10
    pressure3 = 11
    pressure4 = 12
    pressure5 = 13
    pressure6 = 14

Signals:

    statusCodeReceived: This Signal is emits a code in the form of the integer which states
                        the result of the attempt to connect to the Arduino. The corresponding Slot
                        which handles the code is the receiveCode method in mainWindow.py

    dataToUpdateGUI: This Signal emits a an array which itself contains four arrays.
                     At index 0, we have dataPins which contains the pin numbers that the last command sent
                     requested data (from sensors) from. At index 1, we have the statePins which contain the
                     pins that the last command sent request data (from toggleables) from. At index 2, we have
                     the data from the sensors. At index 3, we have the data from the toggleables. At index 3,
                     we have the state of the toggleables. This signal is handled by

Members:

    arduino: Initially set to None, but will be set to a QSerialPort later
    portName: Human readable name of the port the Arduino is connected to, initally set to None
    portList: Is initially set to a list of QSerialPortInfo, its how we get the port that we connect to
    platform: The OS the software is being run on
    messageReceived: The response from the command that has been set by receiveData
    sentMessage: The command just sent to the Arduino
    newData: Variable used by the receiveData method to determine whether to continue reading data or not
    count: Number of time readWrite function has run. Mainly used to make sure that it skips the receiveData
           and decomposeResponse as there is no data to read or write

Methods:

# updatePortList(): Updates the portList member variable with all the serial ports that are avialable to connect to.

# connectToPortCode(): Method that ensures that program will work across platforms, passes the port we are going to
connect to the connectHelper()

# connectToPort(): Was used to test functionality of this class without a GUI however as this class is now a child of
QObject this method has no use currently (Needs to be deleted at some point)

# onnectHelper(): Actually connects the computer to the serial port, and starts a 5 second timer which at the end will write
<ping> to the Arduino. The 5 second delay is to allow the Arduino some time to start up.

# readConnectMessage(): Method that reads the data that the Arduino will write to the computer on startup. After writing <ping>,
it expects to get a <pong> back from the Arduino, which means it adheres to the communication standard. If it does receive <pong>,
it sends emits a statusCodeReceived value of 0, if not it sends out a different value which will be handled by the mainwindow.py

# updateConnectionStatus(): Currently has no use, thinking of ways it could be made useful, but currently right now doesn't have much
use

# receiveData(): After we are connected to the Arduino, receiveData will be the main way we read from the Arduino. Each message sent to
and from the Arduino must me encased in brackets <>, and there are certain keywords/letters which will instruct the Arduino to do different
things.

    Here are the commands that can be sent:
        1. <ping>: returns <pong> mainly used to check if we are connected to an Arduino and it supports the standard
        2. <d,....>:, A command starting with the letter d indicates that it is trying to receive data from the Arduino will explain more
        3. <abortA>: Tells the Arduino to do a type A abort where all toggleables (servos, line cutters, solenoids) are set to LOW or 0V
        4. <abortB>: Tells the Arduino to do a type B abort

    In order to recieve data from the Arduino you send the command <d, following with the pins you want to want to read data from.
    In my terminology, I have two groups of things called sensors and toggelables. Data are your sensors (temperature, mass, pressure) and toggleables
    are your servos, line cutters, and solenoids.

    When you want to read data from your sensors, you follow the <d, command with the pin number of the sensor followed by a comma (you don't need to
    add a comma if its the last thing in the command)

    For example:
        <d,0>: Is a command that will return the value of the sensor at pin number 1 (<valueOfPin1> would be response you get)
        <d,0,1>: Is a command that will return the value of the sensor at pin #1 and pin #2 (<valueOfPin1,valueOfPin2>)
        <d,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14>: In our current configuration will get the data from all the sensors

    If you want to read data from the toggelables, you just add a ,: tag to indicate that you are switching from reading data from sensors to the toggelables
    and then it is much the same as with the sensors

    For example:
        <d,:,1>: Gets the current state of the toggleable at pinNumber 1
        <d,:,1,2>: Gets the current state of toggleable at pinNumber1 and pinNumber2
        <d,:,1,2,3,4,5,6,7,8,9,10,11,12,13,14>: Gets the current state of the all toggleables in the current configuration

    In order to read data from both, its pretty simple:
        <d,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,:,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15>
    and its response is going to look like this:
        <100,200,300,400,500,600,700,800,900,100,10,20,30,40,50,PIN_HIGH,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW>


# decomposeResponse():

    This method decomposes the response like this:
    <100,200,300,400,500,600,700,800,900,100,10,20,30,40,50,PIN_HIGH,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW,PIN_LOW>
    into two arrays with the sensor data in one array and the toggleable data into another array by using some regular expression magic.

    This data is then sent via a signal to a graph.py where it will be decoded there to update the graph.

# readWrite():

    This method is method that contains the main part of the communications after the 'Run AutoSequence' button is clicked.
    It contains three functions:
        1. receiveData()
        2. decomposeResponse()
        3. writeLine()

    If it is the first time running this command it writes a command to the Arduino. After the first time it is run, it will read data from Arduino,
    then decompose the data, and then write a new command to the Arduino.

    This method is called via a timer which is defined in controlWindow.py. The speed that this method run is also defined in that file as well.

# writeLine():

    This method is a wrapper for the write() method of the QSerialPort class. Seeing as most commands are just queries for all the data, the query
    argument has been set to that as a default argument although it can be overwritten with a different command.

# getArduino():

    This method just returns the QSerialPort.

# getPlatform():

    This method returns what OS you are running this software on.

# getPortName():

    This method returns the human readable serial port that you are connected to.
    Returns None if you are not connected to anything.

# getHumanPortList():

    Returns a human readable list of all open QSerialPorts.

# init():

    When this class is initialized, this class calls the super constructor of QObject, which
    this class inherits from. It then sets the class member variables to their value as said
    in the section above. Next it starts a QTimer which calls the the writeLine method with the
    command ping after 5 seconds which is used to make sure that the program has completed its
    bootloader sequence and actually recieves the data. Next, it connects the readyRead signal
    (which emits a signal whenever there is data to be read in serial buffer) to the readConnectMessage.
"""

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

        print ("It took this long to run this function: {}".format(time.time() - start))

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