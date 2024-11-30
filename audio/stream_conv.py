import pyaudio
import numpy as np
import threading
import queue
import time

class RealtimeAudioConverter:
    def __init__(self):
        self.CHUNK = 1024 * 2  # バッファサイズ
        self.FORMAT_IN = pyaudio.paInt32
        self.FORMAT_OUT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE_IN = 32000
        self.RATE_OUT = 16000
        self.running = False
        self.audio = pyaudio.PyAudio()
        self.buffer = queue.Queue()

    def start_streaming(self):
        """オーディオストリーミングを開始"""
        self.running = True

        # 入力ストリームの設定
        self.input_stream = self.audio.open(
            format=self.FORMAT_IN,
            channels=self.CHANNELS,
            rate=self.RATE_IN,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        # 出力ストリームの設定
        self.output_stream = self.audio.open(
            format=self.FORMAT_OUT,
            channels=self.CHANNELS,
            rate=self.RATE_OUT,
            output=True,
            frames_per_buffer=self.CHUNK // 2  # 16kHzなので半分のサイズ
        )

        # 処理スレッドの開始
        self.process_thread = threading.Thread(target=self._process_audio)
        self.process_thread.start()

    def _process_audio(self):
        """オーディオ処理メインループ"""
        while self.running:
            try:
                # マイクから読み込み
                data = self.input_stream.read(self.CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int32)

                # 32bitから16bitへの変換
                # 32ビットの最大値で割って正規化し、16ビットの範囲にスケール
                audio_data_16bit = (audio_data / np.iinfo(np.int32).max * np.iinfo(np.int16).max).astype(np.int16)

                # 32kHzから16kHzへのダウンサンプリング（2サンプルの平均）
                audio_data_reshaped = audio_data_16bit.reshape(-1, 2)
                audio_data_16khz = np.mean(audio_data_reshaped, axis=1).astype(np.int16)

                # 変換したデータを出力
                self.output_stream.write(audio_data_16khz.tobytes())

            except Exception as e:
                print(f"Error processing audio: {e}")
                break

    def stop_streaming(self):
        """ストリーミングを停止"""
        self.running = False
        if hasattr(self, 'process_thread'):
            self.process_thread.join()
        
        if hasattr(self, 'input_stream'):
            self.input_stream.stop_stream()
            self.input_stream.close()
        
        if hasattr(self, 'output_stream'):
            self.output_stream.stop_stream()
            self.output_stream.close()
        
        self.audio.terminate()

# 使用例
if __name__ == "__main__":
    converter = RealtimeAudioConverter()
    print("Starting audio conversion... Press Ctrl+C to stop")
    try:
        converter.start_streaming()
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping audio conversion...")
        converter.stop_streaming()
