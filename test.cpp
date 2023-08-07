#include <iostream>
#include <cstring>
#include <cstdlib>
#include <cmath>

const int numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];
int codes[30];
char returnData[100];

bool newData = false;

void receiveData();
void parseData();
char* handleCode(int, bool&, bool);
int readData();
int readData2();
int readData3();

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

    if (strcmp(strtokIndex, "ping") == 0) {
        strcpy(returnData, "<pong>");
        return;
    }

    returnData[0] = '<';
    index++;

    while (strtokIndex != NULL) {
        codes[index] = atoi(strtokIndex);
        strcat(returnData, handleCode(codes[index], isFirst, false));
        index++;
        strtokIndex = strtok(NULL, ","); // Move to the next token
    }

    strcat(returnData, ">");
    std::cout << returnData << std::endl;
    memset(returnData, 0, sizeof(returnData));
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
        isFirst = false; // Use assignment operator instead of ==
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

    strcat(numArray, std::to_string(data).c_str());
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

int main() {
    std::cout << "C++ program ready." << std::endl;

    while (true) {
        receiveData();
        if (newData == true) {
            strcpy(tempChars, receivedChars);
            parseData();
            newData = false;
            handleCode(10, newData, true);
        }
    }

    return 0;
}
