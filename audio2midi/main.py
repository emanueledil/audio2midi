import pyaudio
import numpy as np

# Parametri audio
RATE = 44100
CHUNK = 1024

# Funzione per applicare un effetto di distorsione ai campioni
def distorsione(samples, gain=10):
    distorted = samples * gain
    distorted = np.clip(distorted, -32768, 32767)
    return distorted.astype(np.int16)

# Funzione principale per elaborare l'audio in tempo reale
def main():
    p = pyaudio.PyAudio()

    # Apertura dello stream audio per input e output
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

    print("Inizio elaborazione audio in tempo reale... (Premi Ctrl+C per terminare)")
    try:
        while True:
            # Leggi i dati dallo stream
            data = stream.read(CHUNK)
            samples = np.frombuffer(data, dtype=np.int16)

            # Applica l'effetto di distorsione
            distorted_samples = distorsione(samples)

            # Scrivi i dati distorti nello stream di output
            stream.write(distorted_samples.tobytes())
    except KeyboardInterrupt:
        print("\nElaborazione terminata.")
    finally:
        # Chiudi lo stream e termina PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
