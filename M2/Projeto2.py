import numpy as np
import math
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

#CalculaDCT

def dct1D(vector):
    N = len(vector)
    X = np.zeros(N)
    for k in range(N):
        CK = math.sqrt(1.0/N) if k == 0 else math.sqrt(2.0/N)
        sum = 0
        for n in range(N):
            f1 = ((2*(3.141592653589)*k*n)/2*N)
            f2 = ((k*(3.141592653589))/2*N)
            sum += vector[n] * math.cos(f1+f2)
            #sum += vector[n] * math.cos(((2*math.pi*k*n)/2*N)+((k*math.pi)/2*N))
        X[k] = CK * sum

    return X

#CalculaIDCT
def idct1D(vector):

    N = len(vector)
    x = np.zeros(N)

    for n in range(N):
        sum = 0
        for k in range(N):
            f1 = ((2*(3.141592653589)*k*n)/2*N)
            f2 = ((k*(3.141592653589))/2*N)
            CK = math.sqrt(1.0/N) if k == 0 else math.sqrt(2.0/N)
            sum += vector[n] * math.cos(f1+f2)
            sum += CK * vector[k] * math.cos((f1)+(f2))
            #sum += alpha * vector[k] * math.cos( (math.pi * (2*n+1) * k) / (2*N) )
        x[n] = sum

    return x

#Encontra os DCTS de um áudio mais importantes e zera os demais

def DCTAudio (na):

    rate, audioData = scipy.io.wavfile.read("audio.wav")
    desenhaGrafico (audioData)

    DCT = dct1D(audioData)
  
    #DCT = fftpack.dct(audioData, norm = 'ortho') #Calcula a Transformada Discreta
    #print (DCT)
    dctFiltrada = DCT.copy()
   # print (dctFiltrada)


    listaComDCT = dctFiltrada.tolist() #Cria uma lista com os valores resultantes da Transformada Discreta
    #print(listaComDCT)
    Indices = []

    #Percorre todo o array e troca os valores pelo seu módulo
    for i in range(0, len(listaComDCT)):
        listaComDCT[i] = abs(listaComDCT[i])
        aux = listaComDCT.copy()

    print(listaComDCT)

    #Adiciona na lista os n índices de maior valor, com n = numero de amostras
    for i in range(0,na):
        Indices.append(listaComDCT.index(max(aux)))
        indiceAux = aux.index(max(aux))
        aux.pop(indiceAux)

       # dctFiltrada = DCT.copy()
	
    print(Indices)

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


    #DCT = dct1D(imagem)
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

 
def deslocador(c):

	rate, audioData = scipy.io.wavfile.read("audio.wav")
	#DCT = fftpack.dct(audioData, norm = 'ortho') #Calcula a dct dos dados do áudio
	DCT = dct1D(audioData)
	dctFiltrada = DCT.tolist()


	if c > 0:
		manter = len(dctFiltrada) - c
		lista1 = dctFiltrada[0:manter]
		lista2 = [0]*c
		
		dctFiltrada = lista2+lista1
	
	elif(c < 0):

		lista1 = dctFiltrada[abs(c):]
		lista2 = [0]*abs(c)
	
		dctFiltrada = lista1+lista2
		
	else:
		pass

		
	dctFiltrada = np.asarray(dctFiltrada)
	audioTransformado = fftpack.idct(dctFiltrada, norm = 'ortho')
	audioTransformado = audioTransformado.astype("int16")
	
	scipy.io.wavfile.write("audio3.wav", rate, audioTransformado)
	plotaDCTs(DCT, dctFiltrada)

def main():
	
    print('\n\n1-Transformada de Cossenos Discretos com Audio 1\n' 
    '2-Transformada de Cossenos Discretos com Imagem\n'
	'3- Deslocador de Frequencias\n')
    op = int(input('Escolha a opção: '))

    if op == 1:
        n = int(input('\nNúmero de frequências desejadas: '))
        DCTAudio(n)

    if op == 2:
        n = int(input('\nNúmero de frequências desejadas: '))
        DCTImagem(n)

    if op == 3:
        n = int(input('\nNúmero de deslocamento: '))
        deslocador(n)
        

if __name__ == '__main__':
	main()