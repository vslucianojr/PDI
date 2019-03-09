from tkinter import Tk #Graphical User Interface
from tkinter.filedialog import askopenfilename
from PIL import Image
import numpy as np

def main():
    print('Selecione a imagem a ser processada')

    Tk().withdraw()
    diretorio = askopenfilename()
    imagemOriginal = imgLida(diretorio)
    exibe(imagemOriginal)

def imgLida(caminhoArquivo):
    return Image.open(caminhoArquivo)

def exibe(imagem):
    imagem.show()

#transforma a imagem em array
def imagemArray(imagem): 
    return np.asarray(iimagem)

#transforma o array em imagem
def arrayImagem (array):

    imagem = Image.fromarray(array, mode='RGB')

    return imagem

#converte a imagem de RGB para YIQ
def RGBYIQ(imagemRGB, largura, altura):

    #copia a imagem e transforma array em float para os calculos de conversão
    imagemYIQ = imagemRGB.copy()
    imagemYIQ = imagemYIQ.astype(float)

    for i in range(altura): 
        for j in range (largura)
            imagemYIQ[i][j][0] = 0.299*imagemRGB[i][j][0] + 0.587*imagemRGB[i][j][1] + 0.114*imagemRGB[i][j][2]
			imagemYIQ[i][j][1] = 0.596*imagemRGB[i][j][0] - 0.274*imagemRGB[i][j][1] - 0.322*imagemRGB[i][j][2]
			imagemYIQ[i][j][2] = 0.211*imagemRGB[i][j][0] - 0.523*imagemRGB[i][j][1] + 0.312*imagemRGB[i][j][2]
	
    return imagemYIQ

def YIQRGB (imagemYIQ, largura, altura):

    #converter imagem para int 
	imagemRGB = imagemYIQ.astype(int)
	
	
	for i in range(altura):
		for j in range(largura):
			
			valor = int(1.000*imagemYIQ[i][j][0] + 0.956*imagemYIQ[i][j][1] + 0.621*imagemYIQ[i][j][2])
			if valor > 255:
				imagemRGB[i][j][0] = 255
			elif valor < 0:
				imagemRGB[i][j][0] = 0
			else:
				imagemRGB[i][j][0] = valor
				
			valor = int(1.000*imagemYIQ[i][j][0] - 0.272*imagemYIQ[i][j][1] - 0.647*imagemYIQ[i][j][2])
			
			if valor > 255:
				imagemRGB[i][j][1] = 255
			elif valor < 0:
				imagemRGB[i][j][1] = 0
			else:
				imagemRGB[i][j][1] = valor
				
			valor = int(1.000*imagemYIQ[i][j][0] - 1.106*imagemYIQ[i][j][1] + 1.703*imagemYIQ[i][j][2])
				
			if valor > 255:
				imagemRGB[i][j][2] = 255
			elif valor < 0:
				imagemRGB[i][j][2] = 0
			else:
				imagemRGB[i][j][2] = valor

	imagemRGB = np.uint8(imagemRGB)
	
	return imagemRGB


if __name__ == '__main__':
	main()



