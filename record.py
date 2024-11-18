import pyaudio
import wave

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
FILE_NAME = "output.wav"

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))
# recording
stream = p.open(format = FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=chunk)

print("recording...")
all = []
for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
    data = stream.read(chunk)
    all.append(data)

stream.close()
p.terminate()

wavFile = wave.open(FILE_NAME, 'wb')
wavFile.setnchannels(CHANNELS)
wavFile.setsampwidth(p.get_sample_size(FORMAT))
wavFile.setframerate(RATE)
wavFile.writeframes(b"".join(all))
wavFile.close()


