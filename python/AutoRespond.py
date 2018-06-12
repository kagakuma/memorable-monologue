import pyaudio
import audioop
import sys
import math
import numpy as np
import wave
import random
import pygame
import time
#visualizer
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


class AutoRespond:
    def __init__(self, filename):
        self.output_filename = filename
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16  # int16型
        self.CHANNELS = 2  # ステレオ
        self.RATE = 44100  # 441.kHz
        self.RECORD_SECONDS = 30  # 30秒でセッションが切れる設定の残り。プロット機能付きだと無限ループ
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        self.isTalking = False
        self.isStarted = False
        self.isResponded = False
        # プロット初期設定
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle(u"リアルタイムプロット")
        self.plt = self.win.addPlot()  # プロットのビジュアル関係
        self.plt.setYRange(-1, 1)  # y軸の上限、下限の設定
        self.curve = self.plt.plot()  # プロットデータを入れる場所

        # アップデート時間設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)  # 10msごとにupdateを呼び出し

        # 音声データの格納場所(プロットデータ)
        self.data = np.zeros(self.CHUNK)

    def responder(self, data):

        dict = {
            0: "うん",
            1: "うんうん",
            2: "なるほど",
            3: "そうだね",
            4: "そうなんだ"
        }

        print("* recording")

        #frames = []
        pygame.mixer.init()
        #frames.append(data)
        rms = audioop.rms(data, 2)
        decibel = 20 * math.log10(rms) if rms > 0 else 0
        #sys.stdout.write("\r rms %3d decibel %f" % (rms, decibel))
        if(rms > 400):
            self.isTalking = True
            self.isResponded = False
            if self.isStarted == False:
                self.isStarted = True

        else:
            self.isTalking = False

        if self.isTalking == False and self.isStarted == True and self.isResponded == False:
            pygame.mixer.music.load("un.wav")
            pygame.mixer.music.play()
            time.sleep(1)
            pygame.mixer.music.stop()
            respondWord =dict[random.randrange(5)]
            print(respondWord)
            self.isResponded = True

#        print("* done recording")

#        self.stream.stop_stream()
#        self.stream.close()
#        self.p.terminate()

#        wf = wave.open(self.output_filename, 'wb')
#        wf.setnchannels(self.CHANNELS)
#        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
#        wf.setframerate(self.RATE)
#        wf.writeframes(b''.join(frames))
#        wf.close()

    def update(self):
        stream = self.StreamRead()
        self.data = np.append(self.data, self.AudioInput(stream))
        self.responder(stream)
        if len(self.data)/1024 > 5:     #5*1024点を超えたら2048点を吐き出し
            self.data=self.data[2048:]
        self.curve.setData(self.data)   #プロットデータを格納
        print(self.data.size)


    def StreamRead(self):
        return self.stream.read(self.CHUNK)

    def AudioInput(self,streamdata):
        ret = streamdata    #音声の読み取り(バイナリ)
        #バイナリ → 数値(int16)に変換
        #32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)　これはレスポンダーとしては要検討。大きな音や小さい音を弾く手がある。
        ret=np.frombuffer(ret, dtype="int16")/32768.0
        return ret

if __name__ == "__main__":
    plotwin = AutoRespond("un.wav")
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

