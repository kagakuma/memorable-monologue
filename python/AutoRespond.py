import pyaudio
import audioop
import sys
import math
import numpy as np
import wave
import random
import pygame
import time


class AutoRespond:
    def __init__(self, filename):
        self.output_filename = filename
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16  # int16型
        self.CHANNELS = 2  # ステレオ
        self.RATE = 44100  # 441.kHz
        self.RECORD_SECONDS = 30  # 5秒録音
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)


    def responder(self):

        isTalking = False
        isStarted = False
        isResponded = False
        dict = {
            0: "うん",
            1: "うんうん",
            2: "なるほど",
            3: "そうだね",
            4: "そうなんだ"
        }



        print("* recording")

        frames = []
        pygame.mixer.init()
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = self.StreamRead()
            frames.append(data)
            rms = audioop.rms(data, 2)
            decibel = 20 * math.log10(rms) if rms > 0 else 0
            #sys.stdout.write("\r rms %3d decibel %f" % (rms, decibel))
            if(rms > 400):
                isTalking = True
                isResponded = False
                if isStarted == False:
                    isStarted = True

            else:
                isTalking = False

            if isTalking == False and isStarted == True and isResponded == False:
                pygame.mixer.music.load("un.wav")
                pygame.mixer.music.play()
                time.sleep(1)
                pygame.mixer.music.stop()
                respondWord =dict[random.randrange(5)]
                print(respondWord)
                print(i)
                isResponded = True


        print("* done recording")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        wf = wave.open(self.output_filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def StreamRead(self):
        return self.stream.read(self.CHUNK)

    def AudioInput(self):
        ret = self.StreamRead()    #音声の読み取り(バイナリ)
        #バイナリ → 数値(int16)に変換
        #32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)
        ret=np.frombuffer(ret, dtype="int16")/32768.0
        return ret

if __name__ == "__main__":
    responder = AutoRespond("detect.wav")
    responder.responder()

