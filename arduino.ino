/*
const u_int8_t s1 = 1;
const u_int8_t s2 = 2;
const u_int8_t s3 = 3;
const u_int8_t s4 = 4;
const u_int8_t s5 = 5;
const u_int8_t s6 = 6;
const uint8_t s7 = 7;
const uint8_t s8 = 8;
const uint8_t lc1 = 9;
const uint8_t lc2 = 10;
const uint8_t igniter = 11;
const uint8_t servo1 = 12;
const uint8_t servo2 = 13;
const uint8_t servo3 = 14;
const uint8_t servo4 = 15;
*/

const int numChars = 230;
char receivedChars[numChars];
char tempChars[numChars];
int codes[50];
char returnData[numChars];

bool newData = false;
bool toggleable = false;

enum pinState {
    PIN_HIGH,
    PIN_LOW
};

pinState s1state = PIN_LOW;
pinState s2state = PIN_LOW;
pinState s3state = PIN_LOW;
pinState s4state = PIN_LOW;
pinState s5state = PIN_LOW;
pinState s6state = PIN_LOW;
pinState s7state = PIN_LOW;
pinState s8state = PIN_LOW;
pinState linestate1 = PIN_LOW;
pinState linestate2 = PIN_LOW;
pinState igniteState = PIN_LOW;
pinState servo1state = PIN_LOW;
pinState servo2state = PIN_LOW;
pinState servo3state = PIN_LOW;
pinState servo4state = PIN_LOW;

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
        toggleable = false;
        handleGraphCodes(0, newData, true);
        handleToggleCodes(0, newData, true);
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
        clean();
        return;
    }

    returnData[0] = '<';
    index++;

    if (strcmp(strtokIndex, "data") == 0) {
        strtokIndex = strtok(NULL, ",");

        while (strtokIndex != NULL) {

            if (strcmp(strtokIndex, ":") == 0) {
                codes[index] = int(' ');
                strcat(returnData, ", :");
                index++;
                strtokIndex = strtok(NULL, ",");
                toggleable = true;
            } else if (toggleable == true) {
                codes[index] = atoi(strtokIndex);
                strcat(returnData, handleToggleCodes(codes[index], isFirst, false));
                index++;
                strtokIndex = strtok(NULL, ",");
            } else {
                codes[index] = atoi(strtokIndex);
                strcat(returnData, handleGraphCodes(codes[index], isFirst, false));
                index++;
                strtokIndex = strtok(NULL, ","); // Move to the next token
            }
        }


    } else {
        strcpy(returnData, "<nonvalid>");
    }

    strcat(returnData, ">");
    Serial.println(returnData);
    clean();
}

char* handleToggleCodes(int pin, bool& isFirst, bool clear) {
    static char state[8];
    bool toggle = (pin > 0) ? false : true;
    int actualPin = abs(pin);

    if (clear) {
        memset(state, 0, sizeof(state));
        return state;
    }

    if (isFirst) {
        isFirst = false; // Use assignment operator instead of ==
    } else {
        strcpy(state, ", ");
    }


    if (toggle) {

        switch (actualPin) {
            case 1:
                s1state = (s1state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (s1state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 2:
                s2state = (s2state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (s2state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 3:
                s3state = (s3state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (s3state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 4:
                s4state = (s4state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (s4state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 5:
                s5state = (s5state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (s5state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 6:
                s6state = (s6state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (s6state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 7:
                s7state = (s7state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (s7state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 8:
                s8state = (s8state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (s8state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 9:
                linestate1 = (linestate1 == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (linestate1 == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 10:
                linestate2 = (linestate2 == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (linestate2 == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 11:
                igniteState = (igniteState == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (igniteState == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 12:
                servo1state = (servo1state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (servo1state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 13:
                servo2state = (servo2state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (servo2state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 14:
                servo3state = (servo3state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (servo3state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 15:
                servo4state = (servo4state == PIN_HIGH) ? PIN_LOW : PIN_HIGH;
                strcat(state, (servo4state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
        }

    } else {

        switch (actualPin) {
            case 1:
                strcat(state, (s1state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 2:
                strcat(state, (s2state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 3:
                strcat(state, (s3state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 4:
                strcat(state, (s4state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 5:
                strcat(state, (s5state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 6:
                strcat(state, (s6state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 7:
                strcat(state, (s7state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 8:
                strcat(state, (s8state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 9:
                strcat(state, (linestate1 == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 10:
                strcat(state, (linestate2 == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 11:
                strcat(state, (igniteState == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 12:
                strcat(state, (servo1state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 13:
                strcat(state, (servo2state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 14:
                strcat(state, (servo3state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
            case 15:
                strcat(state, (servo4state == PIN_HIGH) ? "PIN_HIGH" : "PIN_LOW");
                break;
        }
    }

    return state;

}

char* handleGraphCodes(int pin, bool& isFirst, bool clear) {
    int data;
    static char numArray[14];

    if (clear) {
        memset(numArray, 0, sizeof(numArray));
        return numArray;
    }

    if (isFirst) {
        isFirst = false; // Use assignment operator instead of ==
    } else {
        strcpy(numArray, ", ");
    }

    data = readGraphPins(pin);

    strcat(numArray, String(data).c_str());
    return numArray;
}

int readGraphPins(int pin) {
    switch (pin) {
        case 0:
            return 500;
            break;
        case 1:
            return 1000;
            break;
        case 2:
            return 1250;
            break;
        case 3:
            return 10;
            break;
        case 4:
            return 20;
            break;
        case 5:
            return 25;
            break;
        case 6:
            return 30;
            break;
        case 7:
            return 35;
            break;
        case 8:
            return 45;
            break;
        case 9:
            return 200;
            break;
        case 10:
            return 100;
            break;
        case 11:
            return 150;
            break;
        case 12:
            return 230;
            break;
        case 13:
            return 300;
            break;
        case 14:
            return 350;
            break;
    }

    return -1000;
}

void clean() {
    memset(returnData, 0, sizeof(returnData));
    memset(tempChars, 0, sizeof(tempChars));
    memset(codes, 0, sizeof(codes));
    memset(receivedChars, 0, sizeof(receivedChars));
    return;
}



