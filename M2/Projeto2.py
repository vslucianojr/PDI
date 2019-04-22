import numpy as np
import scipy.io.wavfile 
from scipy import fftpack #Funções Matemáticas
import pydub
from pydub.playback import play
import matplotlib.pyplot as plotagem #Plotagem de gráficos
from PIL import Image #Imagens

#Função para plotagem do gráfico
def desenhaGrafico (data):
    plotagem.figure('Data')
    plotagem.plot(data, linewidth=0.1, alpha=1,color='red')
    plotagem.ylabel('Amplitude')
    plotagem.show()

#Função para plotagem do gráfico com a DCT Filtrada

def plotaDCTs(dct, dctFiltrada):
	plotagem.figure('Domínio da Frequência')
	plotagem.subplot(211)
	plotagem.plot(dct, linewidth=0.1, alpha=1.0, color='blue')
	plotagem.ylabel('Frequencia')
	plotagem.subplot(212)
	plotagem.plot(dctFiltrada, linewidth=0.1, alpha=1.0, color='blue')
	plotagem.ylabel('Frequencia')
	plotagem.show()

#Encontra os DCTS de um áudio mais importantes e zera os demais

def DCTAudio (na):

    rate, audioData = scipy.io.wavfile.read("audio.wav")
    desenhaGrafico (audioData)
    DCT = fftpack.dct(audioData, norm = 'ortho') #Calcula a Transformada Discreta de Fourier

    dctFiltrada = DCT.copy()
	
    listaComDCT = dctFiltrada.tolist() #Cria uma lista com os valores resultantes da Transformada Discreta
    Indices = []

    #Percorre todo o array e troca os valores pelo seu módulo
    for i in range(0, len(listaComDCT)):
        listaComDCT[i] = abs(listaComDCT[i])
        aux = listaComDCT.copy()

    #Adiciona na lista os n índices de maior valor, com n = numero de amostras
    for i in range(0,na):
        Indices.append(listaComDCT.index(max(aux)))
        indiceAux = aux.index(max(aux))
        aux.pop(indiceAux)

        dctFiltrada = DCT.copy()
	
    #Preserva os DCT's de tamanho igual aos da lista de IndiceMaximo verificando se eles estão na lista e zera os demais
    for i in range(0, len(dctFiltrada)):
        if i not in Indices:
            dctFiltrada[i] = 0
	
    dctFiltrada = np.asarray(dctFiltrada)

    AudioTransformado = fftpack.idct(dctFiltrada, norm = 'ortho')
    AudioTransformado = AudioTransformado.astype("int16")
    scipy.io.wavfile.write("audioTransformado.wav", rate, AudioTransformado)

    plotaDCTs(DCT, dctFiltrada)

def DCTImagem (na):

    imagem = Image.open("lena.bmp")
    imagem.show()
    imagem = np.asarray(imagem)

    DCT = fftpack.dct(fftpack.dct(imagem.T, norm = 'ortho').T, norm = 'ortho')
    rxc = len(imagem)*len(imagem[0])

    im = Image.fromarray(DCT)
    im.show()

    listaDeDCT = DCT.copy()
    list(listaDeDCT)
    listaDeDCT = listaDeDCT.tolist()
    aux = listaDeDCT.copy()
    Indices = []

    #Percorre os elementos da matriz em busca de incides de maiores valores e adiciona no array de Indices
    for i in range(0,na):
		
        maior = max([valor for linha in aux for valor in linha]) #Percorre cada linha e cada elemento da matriz e retorna o maior valor
		
        x = [x for x in aux if maior in x][0] #Verifica se o maior valor está em cada linha da matriz. Lista de linhas
		
        linha = listaDeDCT.index(x)
        coluna = x.index(maior)
	
        aux[linha][coluna] = -1
		
        Indices.append(str(linha)+','+str(coluna))
	
    listaDeDCT = DCT.copy()

    #Percorre a imagem em busca dos cossenos de maior relevância, zerando os demais

    for i in range(0, len(imagem)):
        for j in range(0, len(imagem[0])):
            indice = (str(i)+','+str(j))
            if indice not in Indices:
                listaDeDCT[i][j] = 0
				
    dctFiltrada = np.asarray(listaDeDCT)

    im = Image.fromarray(dctFiltrada)
    im.show()
    idct = fftpack.idct(fftpack.idct(dctFiltrada.T, norm = 'ortho').T, norm = 'ortho')
    im = Image.fromarray(idct)
    im.show()
 


def main():
	
    print('\n\n1-Transformada de Cossenos Discretos com Audio 1\n' 
    '2-Transformada de Cossenos Discretos com Imagem\n'
	'3- ----------\n')
    op = int(input('Escolha a opção: '))

    if op == 1:
        n = int(input('\nNúmero de frequências desejadas: '))
        DCTAudio(n)

    if op == 2:
        n = int(input('\nNúmero de frequências desejadas: '))
        DCTImagem(n)
        

if __name__ == '__main__':
	main()