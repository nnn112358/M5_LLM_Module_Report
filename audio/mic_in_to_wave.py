import pyaudio
import wave
import sys

def record_audio(output_filename, duration=5, format_bit=pyaudio.paInt16,sample_rate=8000,sample_hosei=1, channels=1, chunk=1024):
    """
    Function to record audio from microphone and save to WAV file

    Parameters:
    output_filename (str): Name of the WAV file to save
    duration (int): Recording duration in seconds (default: 5)
    sample_rate (int): Sampling rate (default: 44100Hz)
    channels (int): Number of channels (default: 1 (mono))
    chunk (int): Number of samples to read at once (default: 1024)
    """

    # Create PyAudio instance
    audio = pyaudio.PyAudio()
    sample_rate2=sample_rate*sample_hosei
    try:
        # Open recording stream
        stream = audio.open(
            format=format_bit,  # Record in 16-bit integer
            channels=channels,        # Mono
            rate=sample_rate,        # Sampling rate
            input=True,              # Set as input stream
            frames_per_buffer=chunk  # Chunk size
        )

        print(f"Starting recording... Will record for {duration} seconds")

        # List to store audio data
        frames = []

        # Record for specified duration
        for _ in range(0, int(sample_rate2 / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        print("Recording completed")

        # Close stream
        stream.stop_stream()
        stream.close()

        # Save as WAV file
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(format_bit))
            wf.setframerate(sample_rate2)
            wf.writeframes(b''.join(frames))

        print(f"Recording saved to {output_filename}")

    finally:
        # Terminate PyAudio
        audio.terminate()

if __name__ == "__main__":
    # Usage example
    record_audio("S16_LE_08000Hz.wav", duration=1,format_bit=pyaudio.paInt16,sample_rate=4000,sample_hosei=2)
    record_audio("S16_LE_16000Hz.wav", duration=1,format_bit=pyaudio.paInt16,sample_rate=8000,sample_hosei=2)
    record_audio("S16_LE_24000Hz.wav", duration=1,format_bit=pyaudio.paInt16,sample_rate=12000,sample_hosei=2)
    record_audio("S16_LE_32000Hz.wav", duration=1,format_bit=pyaudio.paInt16,sample_rate=16000,sample_hosei=2)

    record_audio("S32_LE_08000Hz.wav", duration=1,format_bit=pyaudio.paInt32,sample_rate=8000,sample_hosei=1)
    record_audio("S32_LE_16000Hz.wav", duration=1,format_bit=pyaudio.paInt32,sample_rate=16000,sample_hosei=1)
    record_audio("S32_LE_24000Hz.wav", duration=1,format_bit=pyaudio.paInt32,sample_rate=24000,sample_hosei=1)
    record_audio("S32_LE_32000Hz.wav", duration=1,format_bit=pyaudio.paInt32,sample_rate=32000,sample_hosei=1)

    record_audio("S24_LE_08000Hz.wav", duration=1,format_bit=pyaudio.paInt24,sample_rate=8000,sample_hosei=1)
    record_audio("S24_LE_16000Hz.wav", duration=1,format_bit=pyaudio.paInt24,sample_rate=16000,sample_hosei=1)
    record_audio("S24_LE_24000Hz.wav", duration=1,format_bit=pyaudio.paInt24,sample_rate=24000,sample_hosei=1)
    record_audio("S24_LE_32000Hz.wav", duration=1,format_bit=pyaudio.paInt24,sample_rate=32000,sample_hosei=1)

