## LLM Moduleのマイクとスピーカを使用する手順




```
再生：aplay -D plughw:0,1 test1.wav
aplay: 音声を再生するコマンド
-D plughw:0,1: 音を出すスピーカーを選ぶ（0,1は機器の番号）
test1.wav: 再生するファイル

録音：arecord -f S32_LE -r 32000 -D plughw:0,0 test1.wav
```


```
# aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: Audio [Axera Audio], device 1: 6050000.i2s_mst-actt 23f2000.audio_codec-1 [6050000.i2s_mst-actt 23f2000.audio_codec-1]
  Subdevices: 1/1
  Subdevice #0: subdevice #0

# tinypcminfo
Info for card 0, device 0:

PCM out:
cannot open card(0) device (0): No such file or directory
Device does not exist.

PCM in:
      Access:   0x000009
   Format[0]:   0x000444
   Format[1]:   00000000
 Format Name:   S16_LE, S24_LE, S32_LE
   Subformat:   0x000001
        Rate:   min=8000Hz      max=192000Hz
    Channels:   min=2           max=2
 Sample bits:   min=16          max=32
 Period size:   min=32          max=16384
Period count:   min=2           max=4096


```




![image](https://github.com/user-attachments/assets/35f61900-cd86-4179-ac11-d2b2060ad021)

https://gist.github.com/MarsTechHAN/d6e51d39c3a0bbc00acea41e24d4d4f1#file-ax630c_alsa_fix_samplerate-c-L38


![image](https://github.com/user-attachments/assets/ab0775e5-7bc9-49cd-b3de-a36dbf291034)



vosk-model-small-ja-0.22


















from:@devemin
```
cat /proc/asound/pcm
でサウンド構成がわかり、
sudo apt install alsa-utils
alsamixer で画面の右の方までぐーっといき、100 になってるANA GAIN をいくつかボリュームを下げ、
aplay -D hw:0,1 /root/bird.wav
とかで、16bit/16kHz/stereo とかのwave を再生できた！

cd /root
arecord -D plughw:0,0 -f S24_LE -r 24000 mic2.wav

再生は、
aplay -D plughw:0,1 /root/mic2.wav
sudo apt install portaudio19-dev
python から音声の録音/再生できたー

sudo apt install portaudio19-dev
pip install pyaudio

昨日のポストと同じく、24bit / bitrate 24000 にして録音した。
再生もできたけど、やっぱり wave ファイルの Hz/bitrate 次第で変な再生になったりエラーになったりする。これは ALSA あたりを自分はよくわかってないｗ

```
