import wave
import numpy as np
from scipy.fft import fft
from sklearn.ensemble import RandomForestRegressor

# Função para calcular as frequências do áudio com janelas sobrepostas
def calcular_tonalidade_voz_sobreposta(arquivo_wav, frequencia_minima=85, frequencia_maxima=255, tamanho_janela=1024, taxa_amostragem=44100, sobreposicao=0.5):
    arquivo = wave.open(arquivo_wav, 'r')
    num_frames = arquivo.getnframes()
    taxa_amostragem_audio = arquivo.getframerate()
    num_janelas = int(num_frames // (tamanho_janela * (1 - sobreposicao))) - 1  # Calcula o número de janelas com sobreposição
    tonalidades = []
    
    for i in range(num_janelas):
        posicao_inicial = int(i * tamanho_janela * (1 - sobreposicao))
        posicao_final = posicao_inicial + tamanho_janela
        arquivo.setpos(posicao_inicial)
        dados = np.frombuffer(arquivo.readframes(tamanho_janela), dtype=np.int16)
        transformada = fft(dados)
        frequencias_janela = np.fft.fftfreq(tamanho_janela, 1.0 / taxa_amostragem)
        frequencias_interesse = frequencias_janela[(frequencias_janela >= frequencia_minima) & (frequencias_janela <= frequencia_maxima)]
        tonalidade_janela = np.mean(frequencias_interesse)
        tonalidades.append(tonalidade_janela)
    
    arquivo.close()
    
    return tonalidades

# Função para extrair características do áudio para treinamento do modelo
def extrair_caracteristicas_arquivo(arquivo_wav):
    tonalidades = calcular_tonalidade_voz_sobreposta(arquivo_wav)
    # Calcula a média das tonalidades
    return np.mean(tonalidades)

# Exemplo de uso do modelo de aprendizado de máquina para prever a tonalidade da voz
def prever_tonalidade_voz(arquivo_wav, modelo):
    feature = extrair_caracteristicas_arquivo(arquivo_wav)
    return modelo.predict([[feature]])[0]  # Passa a característica como uma lista dentro de outra lista

# Exemplo de treinamento do modelo (usando dados fictícios)
# Supondo que você tenha dados de treinamento X_train, y_train e dados de teste X_test, y_test
# Substitua os dados fictícios pelos seus dados reais
X_train = np.random.rand(150, 1)
y_train = np.random.rand(150)
X_test = np.random.rand(35, 1)
y_test = np.random.rand(50)

modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Exemplo de previsão de tonalidade da voz
tonalidade_prevista = prever_tonalidade_voz('C:/Users/PREDATOR/Documents/SERVIDOR/gerarAudio/usar.wav', modelo)

# Salvar tonalidade prevista em um arquivo de texto
with open('tonalidade_prevista.txt', 'w') as arquivo_saida:
    arquivo_saida.write(str(tonalidade_prevista))
