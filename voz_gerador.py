import sys
import os
from pydub import AudioSegment
from gtts import gTTS
from pydub.playback import play

def adjust_pitch(audio_segment, target_pitch):
    # Calcular o fator de ajuste de tonalidade
    current_pitch = audio_segment.dBFS
    factor = target_pitch - current_pitch
    return audio_segment.apply_gain(factor)

def adjust_volume(audio_segment, target_dBFS):
    # Calcular o fator de ajuste de volume
    factor = target_dBFS - audio_segment.dBFS
    return audio_segment.apply_gain(factor)

def generate_audio(base_voice_path, text, output_path, target_pitch=None):
    # Carregar o áudio base
    base_audio = AudioSegment.from_wav(base_voice_path)

    # Analisar a tonalidade do áudio base
    base_pitch = base_audio.dBFS

    # Gerar áudio para o texto usando gTTS
    tts = gTTS(text, lang='pt')
    tts.save("temp_tts.mp3")

    # Carregar o áudio gerado
    generated_audio = AudioSegment.from_mp3("temp_tts.mp3")

    # Ajustar a tonalidade do áudio gerado para combinar com a do áudio base
    if target_pitch is not None:
        adjusted_speech = adjust_pitch(generated_audio, target_pitch)
    else:
        adjusted_speech = generated_audio

    # Ajustar o volume do áudio gerado
    adjusted_speech = adjust_volume(adjusted_speech, base_pitch)

    # Salvar o áudio ajustado
    adjusted_speech.export(output_path, format="wav")

    # Reproduzir o áudio usando pydub
    play(adjusted_speech)

    # Remover arquivos temporários
    os.remove("temp_tts.mp3")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python voz_gerador.py <caminho_voz_base> <texto>")
        sys.exit(1)

    base_voice_path = sys.argv[1]
    text = sys.argv[2]
    output_path = "output.wav"

    # Modifique o pitch para -5 dBFS
    generate_audio(base_voice_path, text, output_path, target_pitch=-5)
    print(f"Áudio gerado salvo em {output_path}")
