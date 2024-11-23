## 目的
LLM ModuleとM5Stack CoreS3SEとの間でUART通信を行う

## llm_sysの停止
LLM ModuleのUbuntuが起動すると、M5StackのLLMのサービス(llm_sys,llm_asr,llm_audio,llm_kws,llm_llm,llm_tts)が自動的に起動するようになっています。
LLMのサービスは、M5StackとシリアルポートttyS1を介して通信を行っています。
LLMのサービスが起動している場合はシリアルポートttyS1を占有しているため、他のアプリケーションはシリアルポートttyS1にアクセスすることができません。
そのため、一旦、LLMのサービスを停止します。

psコマンドで起動中のLLMのサービスを確認することができます。

```
# ps aux | grep -i llm
root        1790  0.0  0.4 327008  4824 ?        Ssl  15:36   0:00 /opt/m5stack/bin/llm_sys
root        1791  0.0  0.4  84340  4228 ?        Ssl  15:36   0:00 /opt/m5stack/bin/llm_asr
root        1792  0.0  0.4  83024  3984 ?        Ssl  15:36   0:00 /opt/m5stack/bin/llm_audio
root        1793  0.0  0.5  96176  5368 ?        Ssl  15:36   0:00 /opt/m5stack/bin/llm_kws
root        1794  0.0  0.4  83552  4316 ?        Ssl  15:36   0:00 /opt/m5stack/bin/llm_llm
root        1795  0.0  1.6  98172 15828 ?        Ssl  15:36   0:00 /opt/m5stack/bin/llm_tts
root       11923  0.0  0.2  10056  2036 ttyS0    S+   16:41   0:00 grep --color=auto -i llm
```
systemctlコマンドで、LLMのサービスを停止することができます。
LLMのサービスはkillコマンドなどでプロセスを停止させても、自動的に再起動する設定になっています。

```
#systemctl stop llm-sys
```

LLMのサービスは、LLM ModuleのUbuntunの中で、以下のファイルで設定を行っています。

```
/usr/lib/systemd/system/llm-asr.service
/usr/lib/systemd/system/llm-audio.service
/usr/lib/systemd/system/llm-kws.service
/usr/lib/systemd/system/llm-llm.service
/usr/lib/systemd/system/llm-sys.service
/usr/lib/systemd/system/llm-tts.service
```

## LLM Module(Ubuntu)からM5StackS3SEへ文字列を送信する。

### M5StackS3SEのArduinoIDEプログラム

```cpp
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

### LLM Module(Ubuntu)のPythonプログラム


```python
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

## LLM Module(Ubuntu)からM5StackS3SEへ画像を送信する。


### M5StackS3SEのArduinoIDEプログラム

```cpp
#include <Arduino.h>
#include <M5Unified.h>

void setup() {
  M5.begin();
  M5.Display.setTextSize(1);
  M5.Display.setTextScroll(true);
  M5.Lcd.setTextFont(&fonts::efontJA_16);

  Serial.begin(115200);
  //Serial2.begin(115200, SERIAL_8N1, 16, 17);  // Basic
  // Serial2.begin(115200, SERIAL_8N1, 13, 14);  // Core2
  Serial2.begin(921600, SERIAL_8N1, 18, 17);  // CoreS3

  /* Reset ModuleLLM */
  M5.Display.printf(">>  ModuleLLM..\n");
  Serial.print(">>  ModuleLLM..\n");
}

void loop() {
  static const uint8_t packet_begin[3] = { 0xFF, 0xD8, 0xEA };

  if (Serial2.available() > 0) {

    uint8_t rx_buffer[10];
    int rx_size = Serial2.readBytes(rx_buffer, 10);

    if (rx_size == 10) {
      // パケット開始バイトのチェック
      if ((rx_buffer[0] == packet_begin[0]) && (rx_buffer[1] == packet_begin[1]) && (rx_buffer[2] == packet_begin[2])) {
        // 画像サイズの計算
        uint32_t jpeg_length = (uint32_t)(rx_buffer[4] << 16) | (rx_buffer[5] << 8) | rx_buffer[6];
        unsigned long start_time = millis();
        // バッファにデータを読み込み
        uint8_t* jpeg_buffer = new uint8_t[jpeg_length];
        int data_size = Serial2.readBytes(jpeg_buffer, jpeg_length);

        unsigned long tty_time = millis();
        M5.Lcd.drawJpg(jpeg_buffer, jpeg_length);
        unsigned long draw_time = millis();

        Serial.print("Image size: ");
        Serial.print(jpeg_length);
        Serial.print(" size: ");
        Serial.print(data_size);
        Serial.print("time(msec):");
        Serial.print(tty_time - start_time);
        Serial.print(",");
        Serial.print(draw_time - tty_time);
        Serial.println();
        // メモリの解放
        //delete[] jpeg_buffer;
      }
    }
  }
  Serial.print(".");
  delay(10);
}
```


### LLM Module(Ubuntu)のPythonプログラム


```py
import serial
import time
import cv2
from pathlib import Path

def send_video_over_serial(video_path, serial_port='/dev/ttyS1', baudrate=115200, quality=70):
    """
    Send MP4 video frames over serial port with identification packet
    Args:
        video_path (str): Path to the MP4 video
        serial_port (str): Serial port to use
        baudrate (int): Baud rate for serial communication
        quality (int): JPEG compression quality (1-100)
    """
    try:
        # Open the serial port
        ser = serial.Serial(
            port=serial_port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )

        # Check if serial port is open
        if not ser.is_open:
            ser.open()

        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Error opening video file")

        frame_count = 0
        while True:
            # Read frame from video
            ret, frame = cap.read()
            if not ret:
                break

            resized_frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
            # Convert frame to JPEG
            _, frame_data = cv2.imencode('.jpg', resized_frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
            image_data = frame_data.tobytes()
            total_size = len(image_data)

            # Extract size bytes
            img_size1 = (total_size & 0xFF0000) >> 16
            img_size2 = (total_size & 0x00FF00) >> 8
            img_size3 = (total_size & 0x0000FF) >> 0

            # Create packet with header and frame number
            data_packet = bytearray([
                0xFF,   # Start marker 1
                0xD8,   # Start marker 2
                0xEA,   # Custom identifier 1
                0x01,   # Custom identifier 2
                img_size1,  # Size byte 1 (MSB)
                img_size2,  # Size byte 2
                img_size3,  # Size byte 3 (LSB)
                (frame_count >> 16) & 0xFF,  # Frame number byte 1
                (frame_count >> 8) & 0xFF,   # Frame number byte 2
                frame_count & 0xFF           # Frame number byte 3
            ])

            # Send identification packet
            ser.write(data_packet)
            print(f"Sent frame {frame_count} header: {' '.join([f'{b:02X}' for b in data_packet])}")

            # Small delay after sending header
            time.sleep(0.01)

            start_t = time.perf_counter()
            # Send frame data
            sent = 0
            chunk_size = 4096
            while sent < total_size:
                chunk = image_data[sent:sent + chunk_size]
                bytes_sent = ser.write(chunk)
                sent += bytes_sent

                # Print progress
                progress = (sent / total_size) * 100
                print(f"Frame {frame_count} Progress: {progress:.1f}% ({sent}/{total_size} bytes)", end='\r')

                # Small delay to prevent buffer overflow
                #time.sleep(0.01)

            end_t = time.perf_counter()
            print(f"\nFrame {frame_count} transmission completed!")
            frame_count += 1


            elapsed_time = end_t - start_t
            print(f"time: {elapsed_time}sec")

        print(f"\nVideo transmission completed! Total frames sent: {frame_count}")

    except serial.SerialException as e:
        print(f"Serial port error: {e}")
    except FileNotFoundError:
        print(f"Video file not found: {video_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed")
        if 'cap' in locals():
            cap.release()
            print("Video capture released")

# Example usage
if __name__ == "__main__":
    # Configuration
    VIDEO_PATH = "BadApple.mp4"
    SERIAL_PORT = "/dev/ttyS1"
    BAUD_RATE = 921600
    QUALITY = 50  # JPEG quality (1-100)

    # Send the video
    send_video_over_serial(
        video_path=VIDEO_PATH,
        serial_port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        quality=QUALITY
    )
```
### LLM Module(Ubuntu)のPythonプログラム

```
import serial
import time
from pathlib import Path

def send_image_over_serial(image_path, serial_port='/dev/ttyS1', baudrate=115200, quality=70):
    """
    Send a JPG image over serial port with identification packet

    Args:
        image_path (str): Path to the JPG image
        serial_port (str): Serial port to use
        baudrate (int): Baud rate for serial communication
        quality (int): JPEG compression quality (1-100)
    """
    try:
        # Open the serial port
        ser = serial.Serial(
            port=serial_port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )

        # Check if serial port is open
        if not ser.is_open:
            ser.open()

        # Read the image file
        image_data = Path(image_path).read_bytes()
        total_size = len(image_data)

        # Create identification packet similar to the reference code
        # Extract size bytes
        img_size1 = (total_size & 0xFF0000) >> 16
        img_size2 = (total_size & 0x00FF00) >> 8
        img_size3 = (total_size & 0x0000FF) >> 0

        # Create packet with header (0xFF, 0xD8, 0xEA, 0x01) and size information
        data_packet = bytearray([
            0xFF,   # Start marker 1
            0xD8,   # Start marker 2
            0xEA,   # Custom identifier 1
            0x01,   # Custom identifier 2
            img_size1,  # Size byte 1 (MSB)
            img_size2,  # Size byte 2
            img_size3,  # Size byte 3 (LSB)
            0x00,   # Reserved
            0x00,   # Reserved
            0x00    # Reserved
        ])

        # Send identification packet
        ser.write(data_packet)
        print(f"Sent identification packet: {' '.join([f'{b:02X}' for b in data_packet])}")

        # Small delay after sending header
        time.sleep(0.1)

        # Send image data
        sent = 0
        chunk_size = 1024
        while sent < total_size:
            chunk = image_data[sent:sent + chunk_size]
            bytes_sent = ser.write(chunk)
            sent += bytes_sent

            # Print progress
            progress = (sent / total_size) * 100
            print(f"Progress: {progress:.1f}% ({sent}/{total_size} bytes)", end='\r')

            # Small delay to prevent buffer overflow
            time.sleep(0.01)

        print("\nImage transmission completed successfully!")

    except serial.SerialException as e:
        print(f"Serial port error: {e}")
    except FileNotFoundError:
        print(f"Image file not found: {image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed")

# Example usage
if __name__ == "__main__":
    # Configuration
    IMAGE_PATH = "image.jpg"
    SERIAL_PORT = "/dev/ttyS1"
    BAUD_RATE = 921600
    QUALITY = 70  # JPEG quality (1-100)

    # Send the image
    send_image_over_serial(
        image_path=IMAGE_PATH,
        serial_port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        quality=QUALITY
    )
```
## 参考

Wi-FiがないM5StickVを、M5StickCと繋ぎLINEに投稿してみるまでの手順<br>
https://qiita.com/nnn112358/items/5efd926fea20cd6c2c43

M5Module-LLM/examples/TextAssistant/TextAssistant.ino<br>
https://github.com/m5stack/M5Module-LLM/blob/main/examples/TextAssistant/TextAssistant.ino
