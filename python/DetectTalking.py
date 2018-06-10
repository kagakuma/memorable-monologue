import pyaudio
import audioop
import sys
import math
import wave


class DetectTalking:
    def __init__(self, filename):
        self.output_filename = filename

    def record(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16  # int16型
        CHANNELS = 2  # ステレオ
        RATE = 44100  # 441.kHz
        RECORD_SECONDS = 30  # 5秒録音

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
            rms = audioop.rms(data, 2)
            decibel = 20 * math.log10(rms) if rms > 0 else 0
            #sys.stdout.write("\r rms %3d decibel %f" % (rms, decibel))
            if(rms > 400):
                sys.stdout.write("\r Talking")
            else:
                sys.stdout.write("\r Silent")

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.output_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


if __name__ == "__main__":
    detector = DetectTalking("detect.wav")
    detector.record()

