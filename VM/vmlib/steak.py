import winsound as ws
import math

def fbeep(freq, dur):
    ws.Beep(freq, dur)

def f16beep(freq, dur):

    fer = math.floor(freq * 0.49942016601)
    fer += 37
    ws.Beep(fer, dur)

def f8beep(freq, dur):

    fer = freq * 256
    f16beep(fer, dur)