# Project_gesture_detection
1. Use file esp32_BLE_Guesture.ino to upload to esp32 seed studio
   
     download guesture library from : https://github.com/Seeed-Studio/Grove_Gesture/tree/dev
2. keep the Grove Smart IR Gesture Sensor in SPI mode
   
     All switches need to be toggled to the ON position
    ![SPI_I2C_config](https://github.com/Sumanthverne357/Project_gesture_detection/assets/151477718/140b4a3f-643a-48ae-9f7c-6acb266c5685)
   
4. Use the code BLE_main.py to read the guestures in your laptop/PC, run the following commands in command prompt

     pip install bleak
     pip install asyncio
   
6. Use the code main.py to read the guestures and update the same in GUI

 
