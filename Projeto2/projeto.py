import numpy as np
import matplotlib.pyplot as plotagem
from PIL import Image
import cv2
import scipy.io.wavfile
from scipy import fftpack
import pydub
from pydub.playback import play
import math

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

    rate, audioData = scipy.io.wavfile.read("audioComp.wav")
    desenhaGrafico (audioData)

    #DCT = dct1D(audioData)
  
    DCT = fftpack.dct(audioData, norm = 'ortho') #Calcula a Transformada Discreta
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

    #print(listaComDCT)

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

    AudioTransformado = fftpack.idct(DCT, norm = 'ortho')
    AudioTransformado = AudioTransformado.astype("int16")
    scipy.io.wavfile.write("audioTransformado.wav", rate, AudioTransformado)

    AudioTransformadoImportantes = fftpack.idct(dctFiltrada, norm = 'ortho')
    AudioTransformadoImportantes = AudioTransformadoImportantes.astype("int16")
    scipy.io.wavfile.write("AudioTransformadoImportantes.wav", rate, AudioTransformadoImportantes)

    plotaDCTs(DCT, dctFiltrada)

def DCTImagem(n):
    imagem = Image.open("lena.bmp")
    imagem.show()
    imagem = np.asarray(imagem)
    print (imagem)

    #resultDCT = imDCT(imagem)
    #dct = imDCT(resultDCT.T)

    #dct  = imDCT(imDCT(imagem).T)
    #dct  = dct2D(imagem)

    #Funcao da biblioteca scipy, já utilizando a transposta
    dct = fftpack.dct(fftpack.dct(imagem.T, norm = 'ortho').T, norm = 'ortho')
    
    #Exibindo o resultado da DCT
    im = Image.fromarray(dct)
    im.show()

    #Copia da DCT para uma lista
    listadct = dct.copy()
    listadct = listadct.tolist()
    
    aux = listadct.copy()
    indices = []
    
    for i in range(0,n):
        
        maior = -1
        for linha in range(len(aux)):
            for coluna in range(len(aux[0])):
                if maior < abs(aux[linha][coluna]):
                    maior = abs(aux[linha][coluna])
                    indicex = linha
                    indicey = coluna
    
        aux[indicex][indicey] = -1
        
        indices.append(str(indicex)+','+str(indicey))
    
    listadct = dct.copy()
    
    print(indices)

    for i in range(0, len(imagem)):
        for j in range(0, len(imagem[0])):
            indice = (str(i)+','+str(j))
            if indice not in indices:
                listadct[i][j] = 0
                
    dctFiltrada = np.asarray(listadct)	
    
    im = Image.fromarray(dctFiltrada)
    im.show()
    
    #dct  = invDCT(invDCT(imagem).T)
    idct = fftpack.idct(fftpack.idct(dctFiltrada.T, norm = 'ortho').T, norm = 'ortho')
    
    im = Image.fromarray(idct)
    
    im.show()

def DCT1D(vector):
    N = len(vector)
    X = []
    for k in range(N):
        alpha = math.sqrt(1.0/N) if k == 0 else math.sqrt(2.0/N)
        sum = 0
        for (n, val) in range(N):
            sum += vector[n] * math.cos(((2*math.pi*k*n)/2*N)+((k*math.pi)/2*N))
        X.append(sum)

    return X

def imDCT(image):
    out = image.copy()
    for i in range(len(out[0])):
        out[i] = DCT1D(image[i])
        
    return out

def invdct1D(vector):
    """ Brief
    Description
    """

    N = len(vector)
    x = np.zeros(N)

    for n in range(N):
        sum = 0
        for k in range(N):
            alpha = math.sqrt(1.0/N) if k == 0 else math.sqrt(2.0/N)
            #sum += alpha * vector[k] * math.cos(((2*(3.14159265359)*k*n)/2*N)+((k*(3.14159265359))/2*N))
            sum += alpha * vector[k] * math.cos( (math.pi * (2*n+1) * k) / (2*N) )
        x[n] = sum

    return x

def invDCT(matrix):
    out = matrix.copy()
    for i in range(len(out)):
        out[i] = invdct1D(matrix[i])

    return out

def deslocador(c):

    rate, audioData = scipy.io.wavfile.read("audioComp.wav")
    DCT = fftpack.dct(audioData, norm = 'ortho') #Calcula a dct dos dados do áudio
    #DCT = dct1D(audioData)
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
    
    print('\n\n1-Questão 1\n' 
        '2-Questão 2\n'
        '3-Questão 3\n')
    op = int(input('Escolha a opção: '))

    if op == 1:
        n = int(input('\nIndique o número de frequências desejadas: '))
        DCTAudio(n)

    elif op == 2:
        n = int(input('\nIndique o número de frequências desejadas: '))
        DCTImagem(n)

    elif op == 3:
        c = int(input('\nIndique o deslocamento desejado: '))
        deslocador(c)
    else:
        print('\nTchau')


if __name__ == '__main__':
    main()