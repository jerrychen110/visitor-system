import wave
import pyaudio
import os
import threading
import time
class Recorder(object):
    def __init__(self, chunk=4096, channels=1, rate=16000):
        self.channels = channels
        self.rate = rate
        self.format = pyaudio.paInt16
        self.chunk = chunk
        self._running = True
        self._frames = []

    def start(self):
        threading._start_new_thread(self._recording,())

    def _recording(self):
        self._running = True
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=self.channels, rate=self.rate, input=True, input_device_index=1, frames_per_buffer=self.chunk)
        while(self._running):
            data = stream.read(self.chunk)
            self._frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
    
    def stop(self):
        self._running = False

    def save(self, filename):
        '''save the date to the wavfile'''
        p = pyaudio.PyAudio()
        if not filename.endswith(".wav"):
            filename = filename +".wav"
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(self._frames))
        wf.close()
        



# if __name__ == "__main__":
#     bd = Recorder()
#     bd.start()
#     time.sleep(5)
#     bd.stop()
#     bd.save("Test")