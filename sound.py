import queue
import sys
import threading

import sounddevice as sd
import soundfile as sf
from pynput import keyboard

flag = True  # stop sign

class SoundRecThread(threading.Thread):
    def __init__(self, audiofile='record.wav'):
        threading.Thread.__init__(self)
        self.bRecord = True
        self.filename = audiofile
        self.samplerate = 44100
        self.channels = 2

    def run(self):
        q = queue.Queue()

        def callback(indata, frames, time, status):
            """This is called (from a separate thread) for each audio block."""
            if status:
                print(status, file=sys.stderr)
            q.put(indata.copy())

        with sf.SoundFile(self.filename,
                          mode='x',
                          samplerate=self.samplerate,
                          channels=self.channels) as file:
            with sd.InputStream(samplerate=self.samplerate,
                                channels=self.channels,
                                callback=callback):
                while self.bRecord:
                    file.write(q.get())

    def stoprecord(self):
        self.bRecord = False

def start_sound():
    wav_file = "temp.wav"
    t2 = SoundRecThread(wav_file)
    t2.start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    while flag:
        pass
    t2.stoprecord()

def on_press(key):
    """
    keyboard listening event
    :param key:
    :return:
    """
    global flag
    if key == keyboard.Key.esc:
        flag = False
        print("stop monitor！")
        return False  # return False

if __name__ == "__main__":
    start_sound()
