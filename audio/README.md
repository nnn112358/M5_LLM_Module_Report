Module-LLMのマイク(ALSA経由)を調べてみた件

## 目的
Module-LLMのマイクから、PythonのプログラムからALSAを経由してを呼び出して録音を行い、
wavファイルの評価を行いました。

## 注意事項
Module-LLMの初期ファームウェアで評価した結果です。<br>
今後のファームウェアバージョンアップで変更が入る可能性が高いです。<br>

audioデータは、axera-techのSDKを使ってデータ取得することが推奨されています。<br>
但し、現状はPythonから扱うaudioライブラリはないため、Linuxの標準環境であるALSA経由のデータを
Pythonのプログラムから呼び出す手段をとっています。

## 結論
先に結論を述べますが、現状、ALSAを経由してマイクからのデータを扱う場合には、BitRate設定：16Bit以外が無難です。
例えば、BitRate設定：32Bitで取り込み、16BitのBitRateへ変換することがお勧めとなります。

## 背景

Module-LLMの発売直後、@devemin 氏によって、マイクから音声がとれたと報告がありました。

https://x.com/devemin/status/1853944346556719523

その後、@devemin 氏と@tokkyo氏 によって、BitRate と周波数によって、音が変であると報告がありました。

https://x.com/devemin/status/1853944952205803886

https://x.com/tokkyo/status/1862242255777726856

https://x.com/tokkyo/status/1862939208568242278

@HanxiaoM氏から、
ALSA オーディオ入力の実装に​​バグがあることが報告がありました。

https://x.com/HanxiaoM/status/1853866167137644827

対策として、wavファイルのヘッダを書き換える方法の報告がありました。

https://x.com/HanxiaoM/status/1862455344288735508

その後、 @mongonta555　氏によって、以下の手段によって、
日本語認識できるwavファイルが生成できたと報告がありました。
・arecordで5秒録音→ファイルヘッダを32000Hzに書き換え、ffmpegで32000HzのWAVファイルを16000Hzに変換

https://x.com/mongonta555/status/1862872794406773242


## 調査内容

スマートフォンから、toneジェネレータのアプリを使って、1kHzの音をModule-LLMの近くで鳴らしました。

![image](https://github.com/user-attachments/assets/0c9a1dc2-8ea6-404e-99d6-70cc1248d696)

Module-LLMで、ALSA経由でマイクから音を1秒取得するPythonのプログラムを起動しました。
音のデータをwavファイルに保存しました。

```
root@m5stack-LLM:# python3 mic_input_data.py
```


```python3 mic_input_data.py
import pyaudio
import wave
import sys

def record_audio(output_filename, duration=5, format_bit=pyaudio.paInt16,sample_rate=8000,sample_hosei=1, channels=1, chunk=1024):
    """
    Parameters:
    output_filename (str): Name of the WAV file to save
    duration (int): Recording duration in seconds (default: 5)
    sample_rate (int): Sampling rate (default: 8000Hz)
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
        audio.terminate()

if __name__ == "__main__":
#Bitrate 16Bit
    record_audio("S16_LE_08000Hz.wav", duration=1,format_bit=pyaudio.paInt16,sample_rate=8000)
    record_audio("S16_LE_16000Hz.wav", duration=1,format_bit=pyaudio.paInt16,sample_rate=16000)
    record_audio("S16_LE_24000Hz.wav", duration=1,format_bit=pyaudio.paInt16,sample_rate=24000)
    record_audio("S16_LE_32000Hz.wav", duration=1,format_bit=pyaudio.paInt16,sample_rate=32000)
#Bitrate 32Bit
    record_audio("S32_LE_08000Hz.wav", duration=1,format_bit=pyaudio.paInt32,sample_rate=8000)
    record_audio("S32_LE_16000Hz.wav", duration=1,format_bit=pyaudio.paInt32,sample_rate=16000)
    record_audio("S32_LE_24000Hz.wav", duration=1,format_bit=pyaudio.paInt32,sample_rate=24000)
    record_audio("S32_LE_32000Hz.wav", duration=1,format_bit=pyaudio.paInt32,sample_rate=32000)
#Bitrate 24Bit
    record_audio("S24_LE_08000Hz.wav", duration=1,format_bit=pyaudio.paInt24,sample_rate=8000)
    record_audio("S24_LE_16000Hz.wav", duration=1,format_bit=pyaudio.paInt24,sample_rate=16000)
    record_audio("S24_LE_24000Hz.wav", duration=1,format_bit=pyaudio.paInt24,sample_rate=24000)
    record_audio("S24_LE_32000Hz.wav", duration=1,format_bit=pyaudio.paInt24,sample_rate=32000)
```
https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/audio/mic_in_to_wave.py<br>

次に、wavファイルをテキストファイルに変換するpythonプログラムを実行しました。

```
root@m5stack-LLM:# python3 wav_to_csv.py
```

```wav_to_csv
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
```
https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/audio/wav_to_csv.py<br>


## 調査結果

テキスト化したwavファイルのデータをグラフ化したものが以下になります。
32Bitと24Bitのwavは、16Bitの振幅換算する後処理を入れています。

![image](https://github.com/user-attachments/assets/009342e7-a3a2-4024-9e9c-bbb81017d818)

・BirRate：16Bitでは、1kHzの音が、500Hzに変化しており、2個のデータを取るたびに、振幅 0 のデータが挿入されている。
・32Bitと24Bitのwavはそのような異常は見られない。


## 結論
現状、ALSAを経由してマイクからのデータを扱う場合には、BitRate設定：16Bit以外が無難です。
例えば、BitRate設定：32Bitで取り込み、16BitのBitRateへ変換することがお勧めとなります。


参考リンク
https://x.com/nnn112358/status/1863508092471930989
https://x.com/devemin/status/1853944346556719523
https://x.com/HanxiaoM/status/1853866167137644827
https://x.com/HanxiaoM/status/1862455344288735508
https://x.com/mongonta555/status/1862872794406773242
https://wiki.onakasuita.org/pukiwiki/?Module%20LLM%2FJulius
https://x.com/tokkyo/status/1862655788202041414
https://x.com/nnn112358/status/1862636059571708066

