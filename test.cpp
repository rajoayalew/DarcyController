#include <iostream>
#include <cstring>
#include <cstdlib>
#include <cmath>
#include <string>
using namespace std;

const int numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];
int codes[30];
char returnData[100];

bool newData = false;
bool toggleable = false;

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

enum pinMode {
    HIGH,
    LOW
};

pinMode s1state = LOW;
pinMode s2state = LOW;
pinMode s3state = LOW;
pinMode s4state = LOW;
pinMode s5state = LOW;
pinMode s6state = LOW;
pinMode s7state = LOW;
pinMode s8state = LOW;
pinMode linestate1 = LOW;
pinMode linestate2 = LOW;
pinMode igniteState = LOW;
pinMode servo1state = LOW;
pinMode servo2state = LOW;
pinMode servo3state = LOW;
pinMode servo4state = LOW;

void receiveData();
void parseData();
char* handleGraphCodes(int, bool&, bool);
int readGraphPins(int);
char* handleToggleCodes(int, bool&, bool);
void clean();

int main() {
    std::cout << "C++ program ready." << std::endl;

    while (true) {
        receiveData();
        if (newData == true) {
            strcpy(tempChars, receivedChars);
            parseData();
            newData = false;
            handleGraphCodes(10, newData, true);
            handleToggleCodes(10, newData, true);
        }
    }

    return 0;
}

void receiveData() {
    static bool receivingInProgress = false;
    static int index = 0;
    char startMarker = '<';
    char endMarker = '>';
    char receivedData;

    while (newData == false) {
        receivedData = std::cin.get();

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

    std::cout << strtokIndex << std::endl;

    if (strcmp(strtokIndex, "ping") == 0) {
        strcpy(returnData, "<pong>");
        std::cout << returnData << std::endl;
        clean();
        return;
    }

    returnData[0] = '<';
    index++;

    if (strcmp(strtokIndex, "data") == 0) {
        strtokIndex = strtok(NULL, ",");

        while (strtokIndex != NULL) {
            std::cout << strtokIndex << std::endl;

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
    std::cout << returnData << std::endl;
    clean();
}

void abortA() {
  s1state = LOW;
  s2state = LOW;
  s3state = LOW;
  s4state = LOW;
  s5state = LOW;
  s6state = LOW;
  s7state = LOW;
  s8state = LOW;
  linestate1 = LOW;
  linestate2 = LOW;
  igniteState = LOW;
  servo1state = LOW;
  servo2state = LOW;
  servo3state = LOW;
  servo4state = LOW;
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
                s1state = (s1state == HIGH) ? LOW : HIGH;
                strcat(state, (s1state == HIGH) ? "HIGH" : "LOW");
                break;
            case 2:
                s2state = (s2state == HIGH) ? LOW : HIGH;
                strcat(state, (s2state == HIGH) ? "HIGH" : "LOW");
                break;
            case 3:
                s3state = (s3state == HIGH) ? LOW : HIGH;
                strcat(state, (s3state == HIGH) ? "HIGH" : "LOW");
                break;
            case 4:
                s4state = (s4state == HIGH) ? LOW : HIGH;
                strcat(state, (s4state == HIGH) ? "HIGH" : "LOW");
                break;
            case 5:
                s5state = (s5state == HIGH) ? LOW : HIGH;
                strcat(state, (s5state == HIGH) ? "HIGH" : "LOW");
                break;
            case 6:
                s6state = (s6state == HIGH) ? LOW : HIGH;
                strcat(state, (s6state == HIGH) ? "HIGH" : "LOW");
                break;
            case 7:
                s7state = (s7state == HIGH) ? LOW : HIGH;
                strcat(state, (s7state == HIGH) ? "HIGH" : "LOW");
                break;
            case 8:
                s8state = (s8state == HIGH) ? LOW : HIGH;
                strcat(state, (s8state == HIGH) ? "HIGH" : "LOW");
                break;
            case 9:
                linestate1 = (linestate1 == HIGH) ? LOW : HIGH;
                strcat(state, (linestate1 == HIGH) ? "HIGH" : "LOW");
                break;
            case 10:
                linestate2 = (linestate2 == HIGH) ? LOW : HIGH;
                strcat(state, (linestate2 == HIGH) ? "HIGH" : "LOW");
                break;
            case 11:
                igniteState = (igniteState == HIGH) ? LOW : HIGH;
                strcat(state, (igniteState == HIGH) ? "HIGH" : "LOW");
                break;
            case 12:
                servo1state = (servo1state == HIGH) ? LOW : HIGH;
                strcat(state, (servo1state == HIGH) ? "HIGH" : "LOW");
                break;
            case 13:
                servo2state = (servo2state == HIGH) ? LOW : HIGH;
                strcat(state, (servo2state == HIGH) ? "HIGH" : "LOW");
                break;
            case 14:
                servo3state = (servo3state == HIGH) ? LOW : HIGH;
                strcat(state, (servo3state == HIGH) ? "HIGH" : "LOW");
                break;
            case 15:
                servo4state = (servo4state == HIGH) ? LOW : HIGH;
                strcat(state, (servo4state == HIGH) ? "HIGH" : "LOW");
                break;
        }

    } else {

        switch (actualPin) {
            case 1:
                strcat(state, (s1state == HIGH) ? "HIGH" : "LOW");
                break;
            case 2:
                strcat(state, (s2state == HIGH) ? "HIGH" : "LOW");
                break;
            case 3:
                strcat(state, (s3state == HIGH) ? "HIGH" : "LOW");
                break;
            case 4:
                strcat(state, (s4state == HIGH) ? "HIGH" : "LOW");
                break;
            case 5:
                strcat(state, (s5state == HIGH) ? "HIGH" : "LOW");
                break;
            case 6:
                strcat(state, (s6state == HIGH) ? "HIGH" : "LOW");
                break;
            case 7:
                strcat(state, (s7state == HIGH) ? "HIGH" : "LOW");
                break;
            case 8:
                strcat(state, (s8state == HIGH) ? "HIGH" : "LOW");
                break;
            case 9:
                strcat(state, (linestate1 == HIGH) ? "HIGH" : "LOW");
                break;
            case 10:
                strcat(state, (linestate2 == HIGH) ? "HIGH" : "LOW");
                break;
            case 11:
                strcat(state, (igniteState == HIGH) ? "HIGH" : "LOW");
                break;
            case 12:
                strcat(state, (servo1state == HIGH) ? "HIGH" : "LOW");
                break;
            case 13:
                strcat(state, (servo2state == HIGH) ? "HIGH" : "LOW");
                break;
            case 14:
                strcat(state, (servo3state == HIGH) ? "HIGH" : "LOW");
                break;
            case 15:
                strcat(state, (servo4state == HIGH) ? "HIGH" : "LOW");
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

    strcat(numArray, std::to_string(data).c_str());
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






