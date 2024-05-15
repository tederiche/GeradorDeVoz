import sys
import os
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play

def read_tonality_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            tonality = float(file.readline().strip())  # Lê apenas a primeira linha
        return tonality
    except Exception as e:
        print(f"Erro ao ler arquivo de tonalidade: {e}")
        return None

def adjust_audio_speed(audio_path, output_path, speed_factor):
    audio = AudioSegment.from_file(audio_path)
    if speed_factor <= 0:  # Verificar se speed_factor é positivo
        print("Erro: Tonalidade inválida para ajuste de velocidade.")
        sys.exit(1)

    adjusted_audio = audio.speedup(playback_speed=speed_factor)
    adjusted_audio.export(output_path, format="wav")

def adjust_pitch(audio_segment, semitones):
    new_sample_rate = int(audio_segment.frame_rate * (2.0 ** (semitones / 30.0)))
    return audio_segment._spawn(audio_segment.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(audio_segment.frame_rate)

def generate_audio(text, output_path, voice_gender='male', speed_factor=1.0, volume=0.9, rate=150):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voice_gender == 'male':
        engine.setProperty('voice', voices[0].id)  # Escolha a voz masculina
    else:
        engine.setProperty('voice', voices[1].id)  # Escolha a voz feminina

    engine.setProperty('volume', volume)  # Ajuste o volume da fala (entre 0 e 1)
    engine.setProperty('rate', rate)  # Ajuste a taxa de fala

    engine.save_to_file(text, output_path)
    engine.runAndWait()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python vozHomem.py <texto> <caminho_output> <caminho_tonalidade>")
        sys.exit(1)

    text = sys.argv[1]
    output_path = sys.argv[2]
    tonality_file = sys.argv[3]

    if not os.path.isfile(tonality_file):
        print(f"Erro: Arquivo de tonalidade '{tonality_file}' não encontrado.")
        sys.exit(1)

    tonality = read_tonality_from_file(tonality_file)
    if tonality is None or tonality == 0:  # Adiciona verificação para tonality não ser zero
        print("Erro: Tonalidade inválida.")
        sys.exit(1)

    # Calcular o fator de velocidade
    speed_factor = tonality * 5  # Exemplo de ajuste do fator de velocidade

    print(f"Tonalidade lida: {tonality}")

    temp_audio_path = "temp_audio.wav"
    generate_audio(text, temp_audio_path, voice_gender='male', speed_factor=speed_factor, volume=0.9, rate=180)
    print("Áudio gerado com sucesso")
    
    # Ajustar a velocidade do áudio
    adjust_audio_speed(temp_audio_path, output_path, speed_factor)
    
    # Ajustar o tom do áudio
    audio = AudioSegment.from_file(output_path)
    semitones = 2  # Aumentar a gravidade da voz (pitch)
    pitched_audio = adjust_pitch(audio, semitones)
    pitched_audio.export(output_path, format="wav")
    os.remove(temp_audio_path)

    print(f"Áudio final gerado e salvo em {output_path}")
