import pyaudio
import wave
import time


class ReadWave:
    def __init__(self, filename):
        self.filename = filename
        self.wf = wave.open(self.filename, 'rb')

    def callback(self,in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def play(self):
        CHUNK = 1024

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True)

        """ 
           format  : ストリームを読み書きするときのデータ型
           channels: ステレオかモノラルかの選択 1でモノラル 2でステレオ
           rate    : サンプル周波数
           output  : 出力モード

        """
        stream.start_stream()

        while stream.is_active():
            print("while")
            time.sleep(0.1)

        stream.stop_stream()
        stream.close()

        p.terminate()
