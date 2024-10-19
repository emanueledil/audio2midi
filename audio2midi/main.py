import pyaudio
import numpy as np
from scipy.fft import fft, fftfreq

RATE = 44100  # sampling frequency
CHUNK = 1024  # frame per buffer
# window size: 23,2 ms 

def get_frequency(data, rate):
    fft_data = fft(data)
    freqs = fftfreq(len(fft_data), d=1/rate)
    positive_freqs = freqs[:len(freqs) // 2]
    magnitudes = abs(fft_data[:len(fft_data) // 2])
    
    # keep peak amplitude
    peak_idx = np.argmax(magnitudes)
    peak_freq = positive_freqs[peak_idx]
    return abs(peak_freq)

def play_tone(stream, frequency, duration=0.1):
    t = np.linspace(0, duration, int(RATE * duration), False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    tone = (tone * 32767).astype(np.int16)
    stream.write(tone.tobytes())

# set audio stream 
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

stream_output = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=RATE,
                       output=True)
print("Inizio del rilevamento delle frequenze (CTRL+C per terminare)")
try:
    while True:
        # read from microphone
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        
        # get peak frequency
        frequency = get_frequency(data, RATE)
        print(f"Frequenza dominante: {frequency:.2f} Hz")
        if frequency > 0:
            play_tone(stream_output, frequency)
except KeyboardInterrupt:
    print("Rilevamento terminato.")
    stream.stop_stream()
    stream.close()
    p.terminate()
