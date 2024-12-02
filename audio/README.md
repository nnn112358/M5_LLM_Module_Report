#　目的
Module-LLMのマイクからwavファイルをPython(ALSA経由)で取得し、
wavファイルをcsv化して確認をした。<br>

- マイクからwavファイルを生成する<br>
https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/audio/mic_in_to_wave.py<br>
- wavからcsvファイルを生成する<br>
https://github.com/nnn112358/M5_LLM_Module_Report/blob/main/audio/wav_to_csv.py<br>

結果<br>
1Hzのtoneを録音した結果<br>
注記：16Bitでは、ヘッダとデータとで周波数が2倍ズレる不具合があるので、ヘッダに書き込む周波数を2倍に変えている。Pythonプログラム参照<br>
注記：32Bitでは、16Bitの振幅に換算するために、1/(2^16)を乗じている。24Bitでは、16Bitの振幅に換算するために、1/(2^8)を乗じている。<br>

![image](https://github.com/user-attachments/assets/f9636b00-4365-482b-93cd-eaec06597e0f)

経緯<br>
https://x.com/nnn112358/status/1863508092471930989

