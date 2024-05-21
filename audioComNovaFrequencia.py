import sys
import os
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import normalize

def read_frequencies_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            bass = float(lines[0].split(":")[1].strip())
            midrange = float(lines[1].split(":")[1].strip())
            treble = float(lines[2].split(":")[1].strip())
        return bass, midrange, treble
    except Exception as e:
        print(f"Erro ao ler arquivo de tonalidade: {e}")
        return None, None, None

def adjust_pitch(audio_segment, semitones):
    # Obtém a taxa de amostragem atual
    sample_rate = audio_segment.frame_rate

    # Calcula o fator de ajuste com base nos semitons
    pitch_adjustment = 1.5 ** (semitones / 10.0)

    # Limita o fator de ajuste para evitar valores extremos
    pitch_adjustment = max(0.5, min(pitch_adjustment, 25.0))

    # Aplica o ajuste de tonalidade
    return audio_segment._spawn(audio_segment.raw_data).set_frame_rate(int(sample_rate * pitch_adjustment))



def generate_audio(text, output_path, voice_gender='male', volume=0.9, rate=300):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voice_gender == 'male':
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)

    engine.setProperty('volume', volume)
    engine.setProperty('rate', rate)

    engine.save_to_file(text, output_path)
    engine.runAndWait()

def apply_audio_effects(audio_segment, semitones=0, gain_db=0, normalize_audio=False):
    if semitones != 0:
        audio_segment = adjust_pitch(audio_segment, semitones)
    
    if gain_db != 0:
        audio_segment += gain_db
    
    if normalize_audio:
        audio_segment = normalize(audio_segment)
    
    return audio_segment

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python audioComNovaFrequencia.py <texto> <caminho_output> <caminho_tonalidade> <caminho_audio_referencia>")
        sys.exit(1)

    text = sys.argv[1]
    output_path = sys.argv[2]
    tonality_file = sys.argv[3]
    reference_audio_path = sys.argv[4]

    if not os.path.isfile(reference_audio_path):
        print(f"Erro: Arquivo de áudio de referência '{reference_audio_path}' não encontrado.")
        sys.exit(1)

    bass, midrange, treble = read_frequencies_from_file(tonality_file)
    if bass is None or midrange is None or treble is None:
        print("Erro: Frequências inválidas.")
        sys.exit(1)

    # Calculando o ajuste de tonalidade com base na média das frequências
    mean_pitch = (bass + midrange + treble) / 3.0
    semitones_adjustment = midrange - mean_pitch

    # Gerando áudio sem ajuste de velocidade
    temp_audio_path = "temp_audio.wav"
    generate_audio(text, temp_audio_path, voice_gender='male', volume=0.9, rate=120)
    print("Áudio gerado com sucesso")

    # Aplicando ajuste de tonalidade e outros efeitos
    audio = AudioSegment.from_file(temp_audio_path)
    processed_audio = apply_audio_effects(audio, semitones=semitones_adjustment, gain_db=5, normalize_audio=True)
    processed_audio.export(output_path, format="wav")

    # Removendo arquivo temporário
    os.remove(temp_audio_path)

    print(f"Áudio final gerado e salvo em {output_path}")
