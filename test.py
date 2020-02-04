import soundfile as sf
import numpy as np
sound_path = "voice.wav"
maxim = 32767

data, samplerate = sf.read(sound_path)
scaled = np.int16(data/np.max(np.abs(data)) * maxim)
print(len(scaled))