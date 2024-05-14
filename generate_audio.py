from pydub import AudioSegment
from gtts import gTTS
import sys
import os

# Certifique-se de que o caminho do ffmpeg está correto
AudioSegment.converter = "C:/Program Files/ffmpeg/bin/ffmpeg.exe"

def generate_audio(text):
    # Converte o texto para fala usando gTTS
    tts = gTTS(text, lang='pt')
    tts.save("text_to_speech.wav")
    
    # Carrega o áudio de fala gerado
    speech = AudioSegment.from_wav("text_to_speech.wav")
    
    # Carrega o áudio base
    base_voice = AudioSegment.from_wav("usar.wav")
    
    # Ajusta a duração do áudio de fala para igualar a duração do áudio base
    speech = speech.set_frame_rate(base_voice.frame_rate).set_channels(base_voice.channels)
    
    # Combina o áudio base com o áudio de fala
    combined = base_voice.overlay(speech, position=0)
    
    return combined

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python generate_audio.py <texto>")
        sys.exit(1)

    text = sys.argv[1]

    audio = generate_audio(text)
    audio.export("output.wav", format="wav")

    # Remove o arquivo temporário de áudio de fala
    os.remove("text_to_speech.wav")
