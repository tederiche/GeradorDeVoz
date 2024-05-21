import librosa
import numpy as np
from pydub import AudioSegment
from scipy.signal import butter, lfilter
import pyttsx3

# Função para aplicar filtro
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Carregar áudio original e analisar
def analyze_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    S = np.abs(librosa.stft(y))
    spectral_centroid = librosa.feature.spectral_centroid(S=S)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(S=S)
    return y, sr, spectral_centroid, spectral_bandwidth

# Gerar áudio com pyttsx3
def generate_speech(text, file_path):
    engine = pyttsx3.init()
    engine.save_to_file(text, file_path)
    engine.runAndWait()

# Aplicar equalização ao áudio gerado
def apply_equalization(input_file, output_file, lowcut, highcut):
    y, sr = librosa.load(input_file, sr=None)
    y_eq = bandpass_filter(y, lowcut, highcut, sr)
    audio_eq = AudioSegment(
        data=y_eq.tobytes(), 
        sample_width=2, 
        frame_rate=sr, 
        channels=1
    )
    audio_eq.export(output_file, format="wav")

# Caminhos dos arquivos
original_audio = "C:/Users/PREDATOR/Documents/SERVIDOR/gerarAudio/usar.wav"
generated_audio = "C:/Users/PREDATOR/Documents/SERVIDOR/gerarAudio/generated.wav"
equalized_audio = "C:/Users/PREDATOR/Documents/SERVIDOR/gerarAudio/equalized.wav"

# Texto para sintetizar
text = "Olá, este é um teste de sintetização de voz."

# Analisar o áudio original
y, sr, spectral_centroid, spectral_bandwidth = analyze_audio(original_audio)

# Gerar áudio sintetizado
generate_speech(text, generated_audio)

# Aplicar equalização ao áudio sintetizado
lowcut = spectral_centroid.mean() - spectral_bandwidth.mean() / 2
highcut = spectral_centroid.mean() + spectral_bandwidth.mean() / 2
apply_equalization(generated_audio, equalized_audio, lowcut, highcut)

print("Processo concluído. O áudio equalizado foi salvo como", equalized_audio)
