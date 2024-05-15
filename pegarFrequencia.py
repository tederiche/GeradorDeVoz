import wave
import numpy as np
from scipy.fft import fft

# Função para calcular as frequências do áudio
def calcular_frequencias(arquivo_wav, tamanho_janela=1024, taxa_amostragem=44100):
    # Abre o arquivo WAV
    arquivo = wave.open(arquivo_wav, 'r')
    
    # Obtém os parâmetros do áudio
    num_frames = arquivo.getnframes()
    taxa_amostragem_audio = arquivo.getframerate()
    
    # Calcula o número de janelas a serem processadas
    num_janelas = num_frames // tamanho_janela
    
    frequencias = []
    
    for janela in range(num_janelas):
        # Lê os dados da janela
        dados = np.frombuffer(arquivo.readframes(tamanho_janela), dtype=np.int16)
        
        # Calcula a transformada de Fourier dos dados
        transformada = fft(dados)
        
        # Obtém as frequências presentes na transformada
        frequencias_janela = np.fft.fftfreq(tamanho_janela, 1.0 / taxa_amostragem)
        
        # Adiciona as frequências ao resultado
        frequencias.append(frequencias_janela)
    
    # Fecha o arquivo WAV
    arquivo.close()
    
    return frequencias

# Exemplo de uso
frequencias_audio = calcular_frequencias('C:/Users/PREDATOR/Documents/SERVIDOR/gerarAudio/usar.wav')

# Salvar frequências em um arquivo de texto
with open('frequencias.txt', 'w') as arquivo_saida:
    for frequencias_janela in frequencias_audio:
        arquivo_saida.write(', '.join(str(freq) for freq in frequencias_janela) + '\n')
