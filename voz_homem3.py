import sys
import os
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import speedup, normalize

def get_voice(engine, voice_gender):
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice_gender == 'male' and 'brazil' in voice.languages:
            return voice.id
        elif voice_gender == 'female' and 'brazil' in voice.languages and 'feminine' in voice.name.lower():
            return voice.id
    return voices[0].id  # Default to first voice if no match is found

def generate_audio(text, output_path, voice_gender='male', volume=0.9, rate=200, speed_factor=1.0):
    engine = pyttsx3.init()
    voice_id = get_voice(engine, voice_gender)
    engine.setProperty('voice', voice_id)

    engine.setProperty('volume', volume)
    engine.setProperty('rate', rate)

    engine.save_to_file(text, output_path)
    engine.runAndWait()

    # Adjust speed of the generated audio
    audio = AudioSegment.from_file(output_path)
    adjusted_audio = speedup(audio, playback_speed=speed_factor)
    normalized_audio = normalize(adjusted_audio)
    normalized_audio.export(output_path, format="wav")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Uso: python voz_homem3.py <texto> <caminho_output> <voice_gender> <volume> <speed_factor>")
        sys.exit(1)

    text = sys.argv[1]
    output_path = sys.argv[2]
    voice_gender = sys.argv[3]
    volume = float(sys.argv[4])
    speed_factor = float(sys.argv[5])

    generate_audio(text, output_path, voice_gender=voice_gender, volume=volume, speed_factor=speed_factor)
