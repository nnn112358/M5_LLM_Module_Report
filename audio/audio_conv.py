import wave
import numpy as np

def convert_wav(input_path, output_path):
    """
    32bit 32000Hz WAVファイルを16bit 16000Hzに変換する
    2サンプルの平均を取ってダウンサンプリングを行う
    
    Parameters:
    input_path (str): 入力WAVファイルのパス
    output_path (str): 出力WAVファイルのパス
    """
    # 入力WAVファイルを開く
    with wave.open(input_path, 'rb') as wav_in:
        # WAVファイルのパラメータを取得
        n_channels = wav_in.getnchannels()
        framerate = wav_in.getframerate()
        n_frames = wav_in.getnframes()
        
        # 音声データを読み込む
        data = wav_in.readframes(n_frames)
        data = np.frombuffer(data, dtype=np.int32)
        
        # 32bitから16bitに変換
        # 32ビットの最大値で割って-1から1の範囲に正規化し、
        # その後16ビットの最大値をかけて16ビット整数に変換
        data_16bit = (data / np.iinfo(np.int32).max * np.iinfo(np.int16).max).astype(np.int16)
        
        # 2サンプルずつの平均を計算してダウンサンプリング
        # データ長が奇数の場合も処理できるように調整
        if len(data_16bit) % 2 != 0:
            # 奇数の場合、最後に0を追加
            data_16bit = np.append(data_16bit, 0)
            
        # データを2サンプルずつのグループに分割して平均を計算
        data_reshaped = data_16bit.reshape(-1, 2)
        data_16khz = np.mean(data_reshaped, axis=1).astype(np.int16)
        
        # 出力WAVファイルを作成
        with wave.open(output_path, 'wb') as wav_out:
            wav_out.setnchannels(n_channels)
            wav_out.setsampwidth(2)  # 16bit = 2bytes
            wav_out.setframerate(16000)
            wav_out.writeframes(data_16khz.tobytes())

# 使用例
if __name__ == "__main__":
    convert_wav("input.wav", "output.wav")
