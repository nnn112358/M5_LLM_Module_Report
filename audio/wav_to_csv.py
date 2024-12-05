import wave
import numpy as np
import csv
import struct

def wav_to_csv(input_wav, output_csv):
    """
    Convert a WAV file to CSV format
    Parameters:
        input_wav (str): Path to input WAV file
        output_csv (str): Path to output CSV file
    """
    # Open the wav file
    with wave.open(input_wav, 'rb') as wav_file:
        # Get basic information
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        
        # Read raw data
        raw_data = wav_file.readframes(n_frames)
        
        # Convert raw data to numpy array based on bit depth
        if sample_width == 1:  # 8-bit
            data = np.frombuffer(raw_data, dtype=np.uint8)
            # Convert uint8 to signed int8
            data = data.astype(np.int16) - 128
        elif sample_width == 2:  # 16-bit
            data = np.frombuffer(raw_data, dtype=np.int16)
        elif sample_width == 3:  # 24-bit
            # Create a numpy array to store the 24-bit data as 32-bit
            data = np.zeros(len(raw_data) // 3, dtype=np.int32)
            
            # Process each 24-bit sample
            for i in range(0, len(raw_data), 3):
                # Combine three bytes into a 24-bit integer
                sample = (raw_data[i] & 0xFF) | \
                        ((raw_data[i + 1] & 0xFF) << 8) | \
                        ((raw_data[i + 2] & 0xFF) << 16)
                
                # Convert to signed value
                if sample & 0x800000:  # If sign bit is set
                    sample = sample - 0x1000000
                
                data[i // 3] = sample
        elif sample_width == 4:  # 32-bit
            data = np.frombuffer(raw_data, dtype=np.int32)
        else:
            raise ValueError(f"Unsupported sample width: {sample_width} bytes")
            
        # Reshape if stereo
        if n_channels == 2:
            data = data.reshape(-1, 2)
            
    # Calculate time array
    time_array = np.linspace(0, n_frames / frame_rate, n_frames)
    
    # Write to CSV
    with open(output_csv, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write header
        if n_channels == 1:
            writer.writerow(['Time (s)', 'Amplitude'])
        else:
            writer.writerow(['Time (s)', 'Left Channel', 'Right Channel'])
            
        # Write data
        if n_channels == 1:
            for t, amp in zip(time_array, data):
                writer.writerow([t, amp])
        else:
            for t, (left, right) in zip(time_array, data):
                writer.writerow([t, left, right])

if __name__ == "__main__":
    wav_to_csv("S16_LE_08000Hz.wav", "S16_LE_08000Hz.csv")
    wav_to_csv("S16_LE_16000Hz.wav", "S16_LE_16000Hz.csv")
    wav_to_csv("S16_LE_24000Hz.wav", "S16_LE_24000Hz.csv")
    wav_to_csv("S16_LE_32000Hz.wav", "S16_LE_32000Hz.csv")
    wav_to_csv("S24_LE_08000Hz.wav", "S24_LE_08000Hz.csv")
    wav_to_csv("S24_LE_16000Hz.wav", "S24_LE_16000Hz.csv")
    wav_to_csv("S24_LE_24000Hz.wav", "S24_LE_24000Hz.csv")
    wav_to_csv("S32_LE_08000Hz.wav", "S32_LE_08000Hz.csv")
    wav_to_csv("S32_LE_16000Hz.wav", "S32_LE_16000Hz.csv")
    wav_to_csv("S32_LE_24000Hz.wav", "S32_LE_24000Hz.csv")
    wav_to_csv("S32_LE_32000Hz.wav", "S32_LE_32000Hz.csv")
