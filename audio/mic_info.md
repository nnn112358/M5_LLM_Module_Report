
## 目的
Module_LLMのUbuntu上でPythonプログラムから、マイク入力の音声をwavファイルに保存する。  
ただし、現状は以下の2点の課題があることがわかっている。  

・現状(24/12/02)、Module_LLMのマイク入力をAlsa経由で取得する場合、S16_LEの設定で取り込むと、ヘッダとWavファイルの中身とでミスマッチが起きている。  
　S16_LEを指定した場合、音声データはサンプルレートが指定値の2倍で生成され、指定値でヘッダを書き込むとにミスマッチになるバグがある。  
 　以下のPythonプログラム(mic_in_test.py)では、暫定的に、ヘッダを修正するようにしている。  
  
 <img src="https://gist.github.com/user-attachments/assets/b88d4b17-8a2e-4408-9c10-9a0b90196ac2" width="500"> <br>
https://x.com/HanxiaoM/status/1853866167137644827   
 <img src="https://gist.github.com/user-attachments/assets/643eb208-053c-401a-ba29-85c6a33c2283" width="500">  <br>
https://x.com/HanxiaoM/status/1862455344288735508   

・通常、ASR認識のプログラムは、16Bit/16kHzの音声ファイルに対応していることが多い。  
　以下のPythonプログラムにて、16Bit/16kHでサンプリングした音声ファイルを日本語認識にかけると、認識しない。
　タカヲ氏が32Bit/32kHzでサンプリングした音声ファイルを16Bit/16kHに変換すると、認識しやすいことを発見した。  
 
 https://x.com/mongonta555/status/1862872794406773242  
 <img src="https://gist.github.com/user-attachments/assets/6c4b95d4-4c53-4cab-84f3-002109899c5e" width="500">

 
```
# python3 mic_in_test.py
# ffmpeg -y -i  S32_LE_32000Hz.wav -ac 1 -ar 16000 -acodec pcm_s16le -f wav "S32_LE_32000Hz_ffmpeg.wav"
```

音声の出力は以下のコマンドにて、Module-LLMのスピーカから出力することができる。

```
aplay -D plughw:0,1 S32_LE_32000Hz.wav
```

## Pythonプログラム：マイクから音声を取得し、wavファイル保存


```mic_in_test.py
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
#    record_audio("S16_LE_08000Hz.wav", duration=5,format_bit=pyaudio.paInt16,sample_rate=4000,sample_hosei=2)
    record_audio("S16_LE_16000Hz.wav", duration=5,format_bit=pyaudio.paInt16,sample_rate=8000,sample_hosei=2)
#    record_audio("S16_LE_24000Hz.wav", duration=5,format_bit=pyaudio.paInt16,sample_rate=12000,sample_hosei=2)
#    record_audio("S16_LE_32000Hz.wav", duration=5,format_bit=pyaudio.paInt16,sample_rate=16000,sample_hosei=2)

#    record_audio("S32_LE_08000Hz.wav", duration=5,format_bit=pyaudio.paInt32,sample_rate=8000,sample_hosei=1)
#    record_audio("S32_LE_16000Hz.wav", duration=5,format_bit=pyaudio.paInt32,sample_rate=16000,sample_hosei=1)
#    record_audio("S32_LE_24000Hz.wav", duration=5,format_bit=pyaudio.paInt32,sample_rate=24000,sample_hosei=1)
    record_audio("S32_LE_32000Hz.wav", duration=5,format_bit=pyaudio.paInt32,sample_rate=32000,sample_hosei=1)
```




