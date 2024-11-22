

## 目的
LLM ModuleとM5Stack CoreS3SEとの間で、シリアル通信を行う


llm_sysが/dev/ttyS1

### Arduino側
![image](https://github.com/user-attachments/assets/57b5af43-0654-4a99-bb32-bb2d136cc1df)

```
#include <Arduino.h>
#include <M5Unified.h>

void setup(){
    M5.begin();
    M5.Display.setTextSize(1);
    M5.Display.setTextScroll(true);
    M5.Lcd.setTextFont(&fonts::efontJA_16);

    /* Init module serial port */
    Serial.begin(115200);
    //Serial2.begin(115200, SERIAL_8N1, 16, 17);  // Basic
    // Serial2.begin(115200, SERIAL_8N1, 13, 14);  // Core2
     Serial2.begin(115200, SERIAL_8N1, 18, 17);  // CoreS3

    /* Reset ModuleLLM */
    M5.Display.printf(">>  ModuleLLM..\n");
    Serial.print(">>  ModuleLLM..\n");
}

void loop(){
    if (Serial2.available() > 0) { 
      String input = Serial2.readString();
      std::string question = input.c_str();

      M5.Display.setTextColor(TFT_GREEN);
      M5.Display.printf("<< %s\n", question.c_str());
      Serial.printf("<< %s\n", question.c_str());
      M5.Display.setTextColor(TFT_YELLOW);
      M5.Display.printf(">> ");
      Serial.printf(">> ");

      M5.Display.println();
    }
    Serial.print(".");

    delay(500);
}
```
### LLM Module(Ubuntu)側

```
import serial
import time

def send_serial_data():
    try:
        # Serial port configuration
        ser = serial.Serial(
            port='/dev/ttyS1',    # Device name
            baudrate=115200,        # Baud rate
            bytesize=serial.EIGHTBITS,    # Number of data bits
            parity=serial.PARITY_NONE,    # Parity
            stopbits=serial.STOPBITS_ONE, # Stop bits
            timeout=1             # Timeout in seconds
        )

        # Check if port is open
        if ser.isOpen():
            print("Serial port is open")

        # Send message
        message = "Hello, Serial Port!\n"
        ser.write(message.encode())  # Convert string to bytes and send

        # Wait a bit to ensure transmission
        time.sleep(0.1)

        # Close the port
        ser.close()
        print("Message sent successfully")

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_serial_data()
```


