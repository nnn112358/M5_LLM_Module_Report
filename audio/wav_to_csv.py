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
        
        # Convert raw data to numpy array
        if sample_width == 1:
            data = np.frombuffer(raw_data, dtype=np.uint8)
        elif sample_width == 2:
            data = np.frombuffer(raw_data, dtype=np.int16)
        elif sample_width == 4:
            data = np.frombuffer(raw_data, dtype=np.int32)
            
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

# Example usage
if __name__ == "__main__":
    wav_to_csv("S16_LE_08000Hz.wav", "S16_LE_08000Hz.csv")
    wav_to_csv("S16_LE_16000Hz.wav", "S16_LE_16000Hz.csv")
    wav_to_csv("S16_LE_24000Hz.wav", "S16_LE_24000Hz.csv")
    wav_to_csv("S16_LE_32000Hz.wav", "S16_LE_32000Hz.csv")
    wav_to_csv("S32_LE_08000Hz.wav", "S32_LE_08000Hz.csv")
    wav_to_csv("S32_LE_16000Hz.wav", "S32_LE_16000Hz.csv")
    wav_to_csv("S32_LE_24000Hz.wav", "S32_LE_24000Hz.csv")
    wav_to_csv("S32_LE_32000Hz.wav", "S32_LE_32000Hz.csv")
