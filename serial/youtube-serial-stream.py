import cv2
import serial
import time
from yt_dlp import YoutubeDL

class DualStreamTransmitter:
    def __init__(self, serial_port='/dev/ttyS1', baudrate=2000000, quality=50):
        """
        Initialize the dual stream transmitter
        Args:
            serial_port (str): Serial port to use
            baudrate (int): Baud rate for serial communication
            quality (int): JPEG compression quality (1-100)
        """
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.quality = quality
        self.frame_count = 0
        
    def get_stream_url(self, youtube_url):
        """Get the direct stream URL from YouTube URL"""
        ydl_opts = {'format': 'best'}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return info['url']
            
    def setup_serial(self):
        """Setup serial connection"""
        self.ser = serial.Serial(
            port=self.serial_port,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        if not self.ser.is_open:
            self.ser.open()
            
    def send_frame_serial(self, frame):
        """Send a single frame over serial"""
        # Resize frame for serial transmission
        resized_frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)
        
        # Convert frame to JPEG
        _, frame_data = cv2.imencode('.jpg', resized_frame, 
                                   [cv2.IMWRITE_JPEG_QUALITY, self.quality])
        image_data = frame_data.tobytes()
        total_size = len(image_data)

        # Extract size bytes
        img_size1 = (total_size & 0xFF0000) >> 16
        img_size2 = (total_size & 0x00FF00) >> 8
        img_size3 = (total_size & 0x0000FF)

        # Create packet header
        data_packet = bytearray([
            0xFF, 0xD8,  # Start markers
            0xEA, 0x01,  # Custom identifiers
            img_size1, img_size2, img_size3,  # Size bytes
            (self.frame_count >> 16) & 0xFF,  # Frame number
            (self.frame_count >> 8) & 0xFF,
            self.frame_count & 0xFF
        ])

        # Send header
        self.ser.write(data_packet)
        time.sleep(0.01)  # Small delay

        # Send frame data in chunks
        sent = 0
        chunk_size = 1024
        while sent < total_size:
            chunk = image_data[sent:sent + chunk_size]
            bytes_sent = self.ser.write(chunk)
            sent += bytes_sent
            
        self.frame_count += 1
        return sent

    def stream_youtube(self, youtube_url):
        """Stream YouTube video to both HTTP and serial"""
        try:
            # Get stream URL and setup
            stream_url = self.get_stream_url(youtube_url)
            self.setup_serial()
            cap = cv2.VideoCapture(stream_url)
            
            if not cap.isOpened():
                raise Exception("Could not open stream")
                
            #cv2.namedWindow('YouTube Stream', cv2.WINDOW_NORMAL)
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Display frame (HTTP stream)
                display_frame = cv2.resize(frame, (320, 240))
                #cv2.imshow('YouTube Stream', display_frame)
                
                # Send frame over serial
                bytes_sent = self.send_frame_serial(frame)
                print(f"\rFrame {self.frame_count} sent: {bytes_sent} bytes", end='')
                time.sleep(0.01)
                # Break on 'q' key
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #    break
                    
        except Exception as e:
            print(f"\nError occurred: {e}")
        finally:
            if 'cap' in locals():
                cap.release()
            if hasattr(self, 'ser') and self.ser.is_open:
                self.ser.close()
            #cv2.destroyAllWindows()

def main():
    # Configuration
    SERIAL_PORT = "/dev/ttyS1"
    BAUD_RATE = 2000000
    QUALITY = 50
    
    # YouTube URL
    #youtube_url = "https://www.youtube.com/watch?v=0FBiyFpV__g"
    youtube_url = "https://www.youtube.com/live/NowiK-fEbm0"

    
    # Create and run transmitter
    transmitter = DualStreamTransmitter(
        serial_port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        quality=QUALITY
    )
    transmitter.stream_youtube(youtube_url)

if __name__ == "__main__":
    main()
