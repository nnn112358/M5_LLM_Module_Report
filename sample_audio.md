ax620e_bsp_sdk/msp/sample
## 目的
AxeraのSDKを使って、マイクから録音をするには。

https://github.com/AXERA-TECH/ax620e_bsp_sdk/tree/main/msp/sample/audio


## 
```
# sample_audio -h
usage: sample_audio      <command> <args>
commands:
ai:                      ai get data.
ao:                      ao play data.
ai_aenc:                 aenc link mode.
adec_ao:                 decode link mode.
args:
  -D:                    card number.                (support 0), default: 0
  -d:                    device number.              (support 0,1,2,3), default: 0
  -c:                    channels.                   (support 2,4), default: 2
  -r:                    rate.                       (support 8000~48000), default: 48000
  -b:                    bits.                       (support 16,32), default: 16
  -p:                    period size.                (support 80~1024), default: 1024
  -v:                     is wave file.               (support 0,1), default: 1
  -e:                     encoder type.               (support g711a, g711u, aac, lpcm, g726, opus), default: g711a
  -w:                     write audio frame to file.  (support 0,1), default: 0
  -G:                     get number.                 (support int), default: -1
  -L:                     loop number.                (support int), default: 1
  -i:                     input file.                 (support char*), default: NULL
  -o:                     output file.                (support char*), default: NULL
  --aec-mode:             aec mode.                   (support 0,1,2), default: 0
  --sup-level:            Suppression Level.          (support 0,1,2), default: 0
  --routing-mode:         routing mode.               (support 0,1,2,3,4), default: 0
  --aenc-chns:            encode channels.            (support 1,2), default: 2
  --layout:               layout mode.                (support 0,1,2), default: 0
  --ns:                   ns enable.                  (support 0,1), default: 0
  --ag-level:             aggressiveness level.       (support 0,1,2,3), default: 2
  --agc:                  agc enable.                 (support 0,1), default: 0
  --target-level:         target level.               (support -31~0), default: -3
  --gain:                 compression gain.           (support 0~90), default: 9
  --resample:             resample enable.            (support 0,1), default: 0
  --resrate:              resample rate.              (support 8000~48000), default: 16000
  --vqe-volume:           vqe volume.                 (support 0~10.0), default: 1.0
  --converter:            converter type.             (support 0~4), default: 2
  --aac-type:             aac type.                   (support 2,23,39), default: 2
  --trans-type:           trans type.                 (support 0,2), default: 2
  --asc-file:             asc file.                   (support char*), default: NULL
  --length-file:          length file.                (support char*), default: NULL
  --save-file:            save file.                  (support 0,1), default: 0
  --ctrl:                 ctrl enable.                (support 0,1), default: 0
  --instant:              instant enable.             (support 0,1), default: 0
  --period-count:         period count.               (support int), default: 4
  --insert-silence:       insert silence enable.      (support int), default: 0
  --sim-drop:             sim drop enable.            (support int), default: 0
  --db-detection:         db detection enable.        (support int), default: 0
  --mix:                  mix enable.                 (support int), default: 0
  --mix-file:             mix file.                   (support char*), default: NULL
  --async-test:           async test enable.          (support int), default: 0
  --async-test-name:      async test name.            (support char*), default: NULL
  --async-test-number:    async test number.          (support int), default: 10
  --hpf:                  hpf enable.                 (support int), default: 0
  --hpf-freq:             hpf frequency.              (support int), default: 200
  --hpf-db:               hpf db.                     (support int), default: -3
  --lpf:                  lpf enable.                 (support int), default: 0
  --lpf-freq:             lpf frequency.              (support int), default: 3000
  --lpf-db:               lpf db.                     (support int), default: 0
  --eq:                   eq enable.                  (support int), default: 0
````

1）功能说明：
オーディオ フォルダーの下にあるコードは、顧客がオーディオ モジュール全体の構成プロセスをすぐに理解できるように、Axera SDK パッケージによって提供されるサンプル リファレンス コードです。
サンプル コードでは、ai 記録、ao 再生、ai_aenc エンコード、adec_ao デコードの関数を示します。
当社は、Everest メーカーのコーデック ドライバーを提供しています: es8388、es7210、es8311、es7243l、および es8156

2）使用示例：
例 1: ヘルプ情報を表示する
````
sample_audio -h
````
例 2: 16kHz オーディオを録音する
````
sample_audio ai -D 0 -d 0 -r 16000 -p 160 -w 1
````
例 3: FIXED モードのエコー キャンセルを有効にして 16kHz オーディオを録音する
````
sample_audio ai -D 0 -d 0 -r 16000 -p 160 --aec-mode 2 --routing-mode 0 --layout 1 -w 1
````
例 4: 16kHz オーディオを再生する
````
sample_audio ao -D 0 -d 1 -r 16000
````
例 5: 16kHz オーディオを録音してエンコードする
````
sample_audio ai_aenc -D 0 -d 0 -r 16000 -p 160 -w 1
````
例 6: 16kHz オーディオを録音し、モノラルでエンコードする
````
sample_audio ai_aenc -D 0 -d 0 -r 16000 -p 160 --layout 1 --aenc-chns 1 -w 1
````
例 7: 16kHz オーディオをデコードして再生する
````
sample_audio adec_ao -D 0 -d 1 -r 16000
````
例 8: 内蔵コーデック アップストリーム HPF LPF EQ
````
sample_audio ai -D 0- d 0 --hpf 1 --hpf-freq 200 --hpf-db -12 --lpf 1 --lpf-freq 3000 --lpf-db 0 --eq 1
````
例 9: 内蔵コーデック ダウンストリーム HPF LPF EQ
````
sample_audio ao -D 0 -d 1 --hpf 1 --hpf-freq 200 --hpf-db -12 --lpf 1 --lpf-freq 3000 --lpf-db 0 --eq 1
````
3) 実行結果の例:
正常に実行したら、Ctrl+C を実行して終了します。wave ファイルが現在のディレクトリに生成され、ユーザーはそれを開いて実際の効果を確認できます。

4) 注意事項:
(1) サウンド カード番号とデバイス番号については、/dev/snd/ を参照してください。例:
 pcmC0D0c: カード 0、デバイス 0、キャプチャ デバイス
 pcmC0D1p: カード 0、デバイス 1、再生デバイス



