import pygame
import tkinter as tk
import numpy as np
from scipy.signal import butter, lfilter

# Inizializza pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

# Parametri audio
campionamento = 44100
banda_bassa = 25
banda_alta = 250  # valore iniziale

suono_corrente = None  # variabile globale per il suono corrente

def filtro_passabanda(dati, lowcut, highcut, fs, ordine=3):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(ordine, [low, high], btype='band')
    y = lfilter(b, a, dati)
    return y

def genera_rumore_banda_limited():
    global suono_corrente
    durata_buffer = 10
    rumore = np.random.normal(0, 1, int(durata_buffer * campionamento))

    rumore_filtrato = filtro_passabanda(rumore, banda_bassa, banda_alta, campionamento)

    ampiezza_max = np.max(np.abs(rumore_filtrato))
    print("Volume max:", ampiezza_max)

    if ampiezza_max == 0 or np.isnan(ampiezza_max):
        suono = np.zeros_like(rumore_filtrato, dtype=np.int16)
    else:
        suono = ((rumore_filtrato / ampiezza_max) * 32767).astype(np.int16)

    print("Shape sound:", suono.shape)
    print("Values sound:", suono[:10])

    suono_corrente = pygame.sndarray.make_sound(suono)
    volume_iniziale = slider_volume.get() / 100  # scala volume da 0-100 a 0.0-1.0
    suono_corrente.set_volume(volume_iniziale)
    suono_corrente.play(loops=-1)

def avvia_suono():
    stop_suono()
    genera_rumore_banda_limited()

def stop_suono():
    pygame.mixer.stop()

def aggiorna_volume(valore):
    if suono_corrente:
        volume = float(valore) / 100  # scala volume da 0-100 a 0.0-1.0
        suono_corrente.set_volume(volume)

def aggiorna_banda_alta(valore):
    global banda_alta
    banda_alta = int(valore)
    print(f"Nuova banda alta: {banda_alta} Hz")
    avvia_suono()  # riavvia il suono con nuova banda

# GUI
root = tk.Tk()
root.title("Dog Masking Sound")

frame_bottoni = tk.Frame(root)
frame_bottoni.pack(pady=20)

btn_avvia = tk.Button(frame_bottoni, text="START", command=avvia_suono, width=20)
btn_avvia.pack(side=tk.LEFT, padx=10)

btn_stop = tk.Button(frame_bottoni, text="STOP", command=stop_suono, width=10)
btn_stop.pack(side=tk.LEFT, padx=10)

# Slider volume
volume_frame = tk.Frame(root)
volume_frame.pack(pady=10)

tk.Label(volume_frame, text="Volume").pack()

slider_volume = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                         command=aggiorna_volume, length=200)
slider_volume.set(0)  # volume iniziale a metà (50%)
slider_volume.pack()

# Slider banda alta
banda_frame = tk.Frame(root)
banda_frame.pack(pady=10)

tk.Label(banda_frame, text="Highest Freq. played / Freq. Banda Alta (Hz)").pack()

slider_banda_alta = tk.Scale(banda_frame, from_=50, to=250, orient=tk.HORIZONTAL,
                             command=aggiorna_banda_alta, length=200)
slider_banda_alta.set(banda_alta)  # valore iniziale
slider_banda_alta.pack()

root.mainloop()
