const int numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];
int codes[30];
char returnData[100];

boolean newData = false;

void setup() {
  Serial.begin(115200);
  Serial.println("Arduino ready.");
  Serial.println();
}

void loop() {
    receiveData();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
        parseData();
        newData = false;
        handleCode(0, newData, true);
    }
}

void receiveData() {
    static boolean receivingInProgress = false;
    static int index = 0;
    char startMarker = '<';
    char endMarker = '>';
    char receivedData;

    while (Serial.available() > 0 && newData == false) {
        receivedData = Serial.read();

        if (receivingInProgress == true) {
            if (receivedData != endMarker) {
                receivedChars[index] = receivedData;
                index++;

                if (index >= numChars) {
                    index = numChars - 1;
                }

            } else {
                receivedChars[index] = '\0';
                receivingInProgress = false;
                index = 0;
                newData = true;
            }
        } else if (receivedData == startMarker) {
          receivingInProgress = true;
        }

    }
}

void parseData() {
    char* strtokIndex = strtok(tempChars, ",");
    int index = 0;
    bool isFirst = true;

    if (strcmp(strtokIndex, "ping") == 0) {
        strcpy(returnData, "<pong>");
        Serial.println(returnData);
        return;
    }

    returnData[0] = '<';
    index++;

    while (strtokIndex != '\0') {
        codes[index] = atoi(strtokIndex);
        strcat(returnData, handleCode(codes[index], isFirst, false));
        index++;
        strtokIndex = strtok(NULL, ",");
    }

    strcat(returnData, ">\0");
    Serial.println(returnData);
    memset(returnData, 0, sizeof(returnData));
    memset(tempChars, 0, sizeof(tempChars));
    memset(codes, 0, sizeof(codes));
    memset(receivedChars, 0, sizeof(receivedChars));
}

char* handleCode(int code, bool& isFirst, bool clear) {
    int data;
    static char numArray[14];

    if (clear) {
      memset(numArray, 0, sizeof(numArray));
      return numArray;
    }

    if (isFirst) {
      isFirst = false;
    } else {
      strcpy(numArray, ", ");
    }

    switch (code) {
        case 0:
          data = readData();
          break;
        case 1:
          data = readData2();
          break;
        case 2:
          data = readData3();
          break;
    }

    strcat(numArray, String(data).c_str());
    return numArray;

}

int readData() {
    return 10;
}

int readData2() {
    return 20;
}

int readData3() {
    return 30;
}
