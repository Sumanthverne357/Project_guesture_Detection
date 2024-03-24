

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include <BLE2902.h>

#include <string.h>


#include "Gesture.h"

#define PAG7660_CS D3 ///Uncomment for SPI
pag7660 Gesture; // Combined mode is used by default
//pag7660 Gesture(GESTURE_THUMB_MODE); // Thumb mode is used

String x;
String DataToSend;

//void Thumb_mode()
//{
//      pag7660_gesture_t result;
//    if (Gesture.getResult(result)) {
//        if (result.thumb.up)
//            Serial.println("Thumb Up");
//        else if (result.thumb.down)
//            Serial.println("Thumb Down");
//        }
//}

BLECharacteristic *pCharacteristic;
bool deviceConnected = false;

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

class MyServerCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
      BLEDevice::startAdvertising();
    }
};

void printResultCombinedMode(const pag7660_gesture_t& result) {
    const char *cursor_str[] = {
        NULL,
        "Tap",
        "Grab",
        "Pinch",
    };
    switch (result.type) {
    case 0:
        switch (result.cursor.type) {
        case 1:
        case 2:
        case 3:
            if (result.cursor.select){
                Serial.println(cursor_str[result.cursor.type]);
                DataToSend = cursor_str[result.cursor.type];
            }
            break;
        default:
            DataToSend ="";
            break;
        }
        break;
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
        Serial.print(result.type);
        Serial.println("-finger");
        DataToSend ="";
        // DataToSend = String(result.type)+"-finger";
        break;
    case 6:
        Serial.print("Rotate Right ");
        Serial.println(result.rotate);
        DataToSend = "Rotate_Right";
        break;
    case 7:
        Serial.print("Rotate Left ");
        Serial.println(result.rotate);
        DataToSend = "Rotate_Left";
        break;
    case 8:
        Serial.println("Swipe Left");
        DataToSend = "Swipe_Left";
        send_data(DataToSend);
        break;
    case 9:
        Serial.println("Swipe Right");
        DataToSend = "Swipe_Right";
        send_data(DataToSend);
        break;
    case 19:
    case 20:
    case 21:
    case 22:
    case 23:
        Serial.print(result.type - 19 + 1);
        Serial.println("-finger push");
        DataToSend ="";
        // x = result.type - 19 + 1 ;
        // DataToSend = x+"-finger_push";
        break;
    default:
        DataToSend ="";
        break;
    }
    send_data(DataToSend);
}

void init_BLE(){
  BLEDevice::init("ESP32_BLE_Device");
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ |
                      BLECharacteristic::PROPERTY_NOTIFY 
                    );
  pCharacteristic->addDescriptor(new BLE2902());
  pService->start();
  BLEAdvertising *pAdvertising = pServer->getAdvertising();
  BLEDevice::startAdvertising();
  pAdvertising->start();

  // Retrieve and print the device's MAC address
  BLEAddress deviceAddress = BLEDevice::getAddress();
  Serial.print("Device MAC Address: ");
  Serial.println(deviceAddress.toString().c_str());
}
void setup() {
  Serial.begin(115200);
  init_BLE();
  
//  while(!Serial) {
//      delay(100);
//  }
  Serial.println("\nPAG7660 Gesture combined mode.");
  
  
  if(Gesture.init(PAG7660_CS)) {        //Uncomment for SPI
      Serial.println("PAG7660 initialization success");
      Serial.println("The device started, now you can pair it with bluetooth!");
  } else {
      Serial.println("PAG7660 initialization failed");
  }
  Serial.println("Please input your gestures:\n");
}
void send_data(String dataToSend){
    if (deviceConnected){
    pCharacteristic->setValue(dataToSend.c_str());
    pCharacteristic->notify();
//    Serial.println("sent data");
    delay(200);
    }
}
void loop() {
    pag7660_gesture_t result;
    if (Gesture.getResult(result)) {
        printResultCombinedMode(result);
    }
}
