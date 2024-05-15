import sys
import os
import numpy as np
import librosa
from pydub import AudioSegment
from gtts import gTTS
from scipy.io.wavfile import write

# Certifique-se de que o caminho do ffmpeg está correto
AudioSegment.converter = "C:/Program Files/ffmpeg/bin/ffmpeg.exe"

def analyze_pitch(audio_path):
    y, sr = librosa.load(audio_path)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = []

    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)

    if len(pitch_values) == 0:
        raise ValueError("Nenhuma tonalidade foi detectada no áudio.")

    average_pitch = np.mean(pitch_values)
    return average_pitch

def adjust_pitch(audio_segment, target_pitch, current_pitch):
    factor = target_pitch / current_pitch
    new_frame_rate = int(audio_segment.frame_rate * factor)
    adjusted_audio = audio_segment._spawn(audio_segment.raw_data, overrides={'frame_rate': new_frame_rate})
    return adjusted_audio.set_frame_rate(audio_segment.frame_rate)

def generate_audio(base_voice_path, text, output_path):
    # Analisar a tonalidade do áudio base
    base_pitch = analyze_pitch(base_voice_path)

    # Gerar áudio a partir do texto usando gTTS
    tts = gTTS(text, lang='pt')
    tts.save("temp_tts.wav")

    # Analisar a tonalidade do áudio gerado
    tts_pitch = analyze_pitch("temp_tts.wav")

    # Ajustar a tonalidade do áudio gerado para combinar com a do áudio base
    speech = AudioSegment.from_wav("temp_tts.wav")
    adjusted_speech = adjust_pitch(speech, base_pitch, tts_pitch)

    # Salvar o áudio ajustado
    adjusted_speech.export(output_path, format="wav")

    # Remover o arquivo temporário
    os.remove("temp_tts.wav")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python generate_audio.py <caminho_voz_base> <texto>")
        sys.exit(1)

    base_voice_path = sys.argv[1]
    text = sys.argv[2]
    output_path = "output.wav"

    generate_audio(base_voice_path, text, output_path)
    print(f"Áudio gerado salvo em {output_path}")
