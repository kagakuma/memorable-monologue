import record
import readwave

recorder = record.RecordWave("output.wav")
recorder.record()
player = readwave.ReadWave("output.wav")
player.play()
