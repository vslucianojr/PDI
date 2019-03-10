from tkinter import *  # Graphical User Interface
from tkinter.filedialog import askopenfilename
from PIL import Image
import numpy as np
import math

def selecionaImg():
    # Tornando global para ser acessada pelas demais funcoes
    global imagemOriginal, larguraOriginal, alturaOriginal, arrayOriginal
    img = Tk()  # Iniciando uma nova instancia tk
    img.withdraw()  # Abrindo janela
    diretorio = askopenfilename()  # Passando o caminho da imagem
    imagemOriginal = imgLida(diretorio)
    exibe(imagemOriginal)
    arrayOriginal = imagemArray(imagemOriginal)
    alturaOriginal = len(arrayOriginal)
    larguraOriginal = len(arrayOriginal[0])


def imgLida(caminhoArquivo):
    return Image.open(caminhoArquivo)


def exibe(imagem):  #Esta exibindo grande demais, precisa ajustar o tamanho de exibiçao da imagem
    imagem.show()


def selecionaFuncao():
    select = listbox.curselection()  #Capturando qual item esta selecionado na listbox
    for item in select:
        executaFunc(item)            #Chamando o seletor de funções passando qual item esta selecionado

def imagemArray(imagem):             #Transforma a imagem em array
    return np.asarray(imagem)

def arrayImagem(array):              #Transforma o array em imagem

    imagem = Image.fromarray(array, mode='RGB')

    return imagem

#--------------------------------- CONVERSÃO RGB - YIQ -----------------------------------------------------------

def RGBYIQ(imagemRGB, largura, altura): #Converte a imagem de RGB para YIQ

    #Copia a imagem e transforma array em float para os calculos de conversão
    imagemYIQ = imagemRGB.copy()
    imagemYIQ = imagemYIQ.astype(float)

    for i in range(altura):
        for j in range(largura):
            imagemYIQ[i][j][0] = 0.299*imagemRGB[i][j][0] + \
                0.587*imagemRGB[i][j][1] + 0.114*imagemRGB[i][j][2]
            imagemYIQ[i][j][1] = 0.596*imagemRGB[i][j][0] - \
                0.274*imagemRGB[i][j][1] - 0.322*imagemRGB[i][j][2]
            imagemYIQ[i][j][2] = 0.211*imagemRGB[i][j][0] - \
                0.523*imagemRGB[i][j][1] + 0.312*imagemRGB[i][j][2]

    return imagemYIQ

#--------------------------------- CONVERSÃO YIQ - RGB -----------------------------------------------------------

def YIQRGB(imagemYIQ, largura, altura):
    #Coonvertendo imagem para int
    imagemRGB = imagemYIQ.astype(int)

    for i in range(altura):
        for j in range(largura):
            valor = int(1.000*imagemYIQ[i][j][0] + 0.956 *
                        imagemYIQ[i][j][1] + 0.621*imagemYIQ[i][j][2])
            if valor > 255:
                imagemRGB[i][j][0] = 255
            elif valor < 0:
                imagemRGB[i][j][0] = 0
            else:
                imagemRGB[i][j][0] = valor
            
            valor = int(1.000*imagemYIQ[i][j][0] - 0.272* \
			            imagemYIQ[i][j][1] - 0.647*imagemYIQ[i][j][2])
                        
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
  #--------------------------------- EXIBIÇÃO DE BANDAS INDIVIDUAIS -----------------------------------------------------------

def selecionaBanda(banda, tipo): #Selecionando a banda que será utilizada e o tipo de exibicao
    run = True
    while run:
        if banda is 'R':
            if tipo is 'colorida': 
                arrayModificada = bandaColorida(arrayOriginal, larguraOriginal, alturaOriginal, banda)

            elif tipo is 'monocromatica':
                arrayModificada = bandaMonocromatica(arrayOriginal, larguraOriginal, alturaOriginal, banda)
            imagemModificada = arrayImagem(arrayModificada)
            exibe(imagemModificada)
            run = False
            
        elif banda is 'G':
            if tipo is 'colorida': 
                arrayModificada = bandaColorida(arrayOriginal, larguraOriginal, alturaOriginal, banda)
                
            elif tipo is 'monocromatica':
                arrayModificada = bandaMonocromatica(arrayOriginal, larguraOriginal, alturaOriginal, banda)
            imagemModificada = arrayImagem(arrayModificada)
            exibe(imagemModificada)
            run = False
            
        elif banda is 'B':
            if tipo is 'colorida': 
                arrayModificada = bandaColorida(arrayOriginal, larguraOriginal, alturaOriginal, banda)
                
            elif tipo is 'monocromatica':
                arrayModificada = bandaMonocromatica(arrayOriginal, larguraOriginal, alturaOriginal, banda)
            imagemModificada = arrayImagem(arrayModificada)
            exibe(imagemModificada)
            run = False
        else:
            return

def bandaColorida(arrayDaImagem, largura, altura, banda): #Para a exibicao colorida
  
	arrayDaImagem = arrayDaImagem.copy()
	if banda is 'R':
		for i in range(altura):
			for j in range(largura):
				arrayDaImagem[i][j][1] = 0
				arrayDaImagem[i][j][2] = 0
		return arrayDaImagem

	elif banda is 'G':
		for i in range(altura):
			for j in range(largura):
				arrayDaImagem[i][j][0] = 0
				arrayDaImagem[i][j][2] = 0
		return arrayDaImagem

	elif banda is 'B':
		for i in range(altura):
			for j in range(largura):
				arrayDaImagem[i][j][0] = 0
				arrayDaImagem[i][j][1] = 0
		return arrayDaImagem

	else:
		return arrayDaImagem

def bandaMonocromatica(imagem, largura, altura, banda): #Para a exibição monocromática
	
	imagemMonocromatica = imagem.copy()
	
	if banda is 'R':
		for i in range(altura):
			for j in range(largura):
				#Repete a matriz R em G e B
				imagemMonocromatica[i][j][1] = imagem[i][j][0]
				imagemMonocromatica[i][j][2] = imagem[i][j][0]
				
		return imagemMonocromatica
		
	elif banda is 'G':
		for i in range(altura):
			for j in range(largura):
				#Repete a matriz G em R e B
				imagemMonocromatica[i][j][0] = imagem[i][j][1]
				imagemMonocromatica[i][j][2] = imagem[i][j][1]
				
		return imagemMonocromatica

	elif banda is 'B':
		for i in range(altura):
			for j in range(largura):
				#Repete a matriz B em R e G
				imagemMonocromatica[i][j][0] = imagem[i][j][2]
				imagemMonocromatica[i][j][1] = imagem[i][j][2]
				
		return imagemMonocromatica
    #pega a media dos valores do pixel e atualiza com o valor obtido
    #esse processo deixa mais suave os niveis de cinza
    #elif banda is 'M':
        #for i in range(altura):
			#for j in range(largura):
                #media = (imagem[i][j][0]+imagem[i][j][1]+imagem[i][j][2])/3
				#imagemMonocromatica[i][j][0] = media
				#imagemMonocromatica[i][j][1] = media
                #imagemMonocromatica[i][j][2] = media
        #return imagemMonocromatica
	
	else:
		return imagemMonocromatica

#Troca as cores do pixel
#verde -> magenta,
#azul -> amarelo, 
#vermelho -> cíano, 
#branco -> preto



#--------------------------------- NEGATIVOS -----------------------------------------------------------


def filtroNegativoRGB(imagem, largura, altura):
	
	imagemNegativa = imagem.copy()
	
	for i in range(altura):
		for j in range(largura):
		     # Vai diminuir 255 de cada cor do pixel
			imagemNegativa[i][j][0] = 255 - imagem[i][j][0]
			imagemNegativa[i][j][1] = 255 - imagem[i][j][1]
			imagemNegativa[i][j][2] = 255 - imagem[i][j][2]
	
	return imagemNegativa

def filtroNegativoYIQ(imagem, largura, altura):
	int
	imagemNegativa = imagem.copy()
	
	for i in range(altura):
		for j in range(largura):
			imagemNegativa[i][j][0] = 255 - imagem[i][j][0]
	
	return imagemNegativa
#--------------------------------- CONTROLE DE BRILHO -----------------------------------------------------------

# def brilhoAditivoRGB (imagem, largura, altura):

#     imagemFinal = imagem.copy()

#     if type(c) != int:
#         c = int(c)


#     for i in range(altura):
#         for j in range(largura):

#             #Aplicando o brilho em R

#             valor = imagemFinal[i][j][0].copy()
#             limite = valor + c

#            #Defnindo os limites
#             if limite > 255:
#                 imagemFinal[i][j][0] = 255
#             elif limite < 0:
#                 imagemFinal[i][j][0] = 0
#             else:
#                 imagemFinal[i][j][0] += c

#             #Aplicando o brilho em G

#             valor = imagemFinal[i][j][1].copy()
#             limite = valor + c
#             if limite > 255:
#                 imagemFinal[i][j][1] = 255
#             elif limite < 0:
#                 imagemFinal[i][j][1] = 0
#             else:
#                 imagemFinal[i][j][1] += c

#             #Aplicando o brilho em B

#             valor = imagemFinal[i][j][2].copy()
#             limite = valor + c
#             if limite > 255:
#                 imagemFinal[i][j][2] = 255
#             elif limite < 0:
#                 imagemFinal[i][j][2] = 0
#             else:
#                 imagemFinal[i][j][2] += c

#     return imagemFinal
    
# def brilhoMultiplicativoRGB (imagem, largura, altura, fator):

#     imagemFinal = imagem.copy()

#     if fator < 0:
#         return imagemFinal


#     for i in range(altura):
#         for j in range(largura):


#             #Aplicando o brilho em R
#             valor = imagemFinal[i][j][0].copy()
#             limite = valor * fator

#             if limite < 255:
#                 imagemFinal[i][j][0] = limite
#             else:
#                 imagemFinal[i][j][0] = 255

#             #Aplicando o brilho em G
#             valor = imagemFinal[i][j][1].copy()
#             limite = valor * fator

#             if limite < 255:
#                 imagemFinal[i][j][1] = limite
#             else:
#                 imagemFinal[i][j][1] = 255

#             #Aplicando o brilho em B
#             valor = imagemFinal[i][j][2].copy()
#             limite = valor * fator

#             if limite < 255:
#                 imagemFinal[i][j][2] = limite
#             else:
#                 imagemFinal[i][j][2] = 255
       
#     return imagemFinal


# def brilhoAditivoYIQ (imagem, largura, altura):

#     imagemFinal = imagem.copy()

#     if type(c) != int:
#         c = int(c)


#     for i in range(altura):
#         for j in range(largura):

#             #Aplicando o brilho em y

#             valor = imagemFinal[i][j][0].copy()
#             limite = valor + c

#            #Defnindo os limites
#             if limite > 255:
#                 imagemFinal[i][j][0] = 255
#             elif limite < 0:
#                 imagemFinal[i][j][0] = 0
#             else:
#                 imagemFinal[i][j][0] += c

#     return imagemFinal

# def brilhoMultiplicativoYIQ (imagem, largura, altura, fator):

#     imagemFinal = imagem.copy()

#     for i in range(altura):
#         for j in range(largura):


#             #Aplicando o brilho em Y
#             valor = imagemFinal[i][j][0].copy()
#             limite = valor * fator

#             if limite < 255:
#                 imagemFinal[i][j][0] = limite
#             else:
#                 imagemFinal[i][j][0] = 255
#     int
#     return imagemFinal
#--------------------------------- LIMIARIZAÇÃO -----------------------------------------------------------


#Separa a imagem em dois grupos:
#pixels com valores abaixo do limiar
# pixels acima do valor do limiar
#o limiar é a intensidade do cinza
def filtroLimiarizacaoRGB(imagem, largura, altura, limiar, banda):
	
	imagemLimiarizada = imagem.copy()
	
	if banda is 'R':
		for i in range(altura):
			for j in range(largura):
				#Verifica sempre se o valor daquela banda no pixel é menor ou igual
				#o limiar, caso seja maior ele trunca em 255
				if imagemLimiarizada[i][j][0] <= limiar:
                    #Deixa os pixels brancos,no caso tom mais claro
					imagemLimiarizada[i][j][0] = 0
					imagemLimiarizada[i][j][1] = 0
					imagemLimiarizada[i][j][2] = 0
				else:
					imagemLimiarizada[i][j][0] = 255
					imagemLimiarizada[i][j][1] = 255
					imagemLimiarizada[i][j][2] = 255
				
		return imagemLimiarizada
	
	elif banda is 'G':
		for i in range(altura):
			for j in range(largura):
				if imagemLimiarizada[i][j][1] <= limiar:
					imagemLimiarizada[i][j][0] = 0
					imagemLimiarizada[i][j][1] = 0
					imagemLimiarizada[i][j][2] = 0
				else:
					imagemLimiarizada[i][j][0] = 255
					imagemLimiarizada[i][j][1] = 255
					imagemLimiarizada[i][j][2] = 255

		return imagemLimiarizada
	
	elif banda is 'B':
		for i in range(altura):
			for j in range(largura):
				if imagemLimiarizada[i][j][2] <= limiar:
					imagemLimiarizada[i][j][0] = 0
					imagemLimiarizada[i][j][1] = 0
					imagemLimiarizada[i][j][2] = 0
				else:
					imagemLimiarizada[i][j][0] = 255
					imagemLimiarizada[i][j][1] = 255
					imagemLimiarizada[i][j][2] = 255
				
		return imagemLimiarizada
	
	else:
		return imagemLimiarizada
		

def filtroLimiarizacaoYIQ(imagem, largura, altura, limiar):
	
	imagemLimiarizada = imagem.copy()
	

	for i in range(altura):
		for j in range(largura):
			if imagemLimiarizada[i][j][0] <= limiar:
				imagemLimiarizada[i][j][0] = 0

			else:
				imagemLimiarizada[i][j][0] = 255
				
	return imagemLimiarizada

#--------------------------------- MEDIANA -----------------------------------------------------------


def filtroMedianaRGB (imagem, largura, altura, m, n):
    m = m.get()
    n = n.get()
    m = int(m)
    n = int(n)
    ImagemMediana = imagem.copy()

    limiteAltura = math.floor(m/2)
    print(limiteAltura)
     
    limiteLargura = math.floor(n/2)
    print( limiteLargura)
                #Cria uma matriz de 0`s com a dimensáo do Kernel para cada banda.
                
    bandaR = np.zeros((m,n), dtype = int) 
    bandaG = np.zeros((m,n), dtype = int) 
    bandaB = np.zeros((m,n), dtype = int) 

    soma = 0
    mediana = 0
    
    for i in range(limiteAltura, altura - limiteAltura):               #Laço para percorrer a altura
        for j in range(limiteLargura, largura - limiteLargura):        #Laço para percorrer a largura
	
            contAltura = limiteAltura
            contLargura = limiteLargura
			
            #Laço para percorrer a banda R dos Pixels da parte da imagem referente ao tamanho do Kernel 
            for k in range(m):
                for l in range(n):
                    bandaR[k][l] = imagem[i - contAltura][j - contLargura][0]
                    contLargura -= 1
                    contAltura -= 1
                    contLargura = limiteLargura

            #Ordena os valores da banda R	
            bandaOrdenadoR = np.sort(bandaR, axis = None)
			
            #Verififica se a quantidade de elementos do array ordenado é par ou impar e define a mediana	

            if len(bandaOrdenadoR)%2 == 0:
                soma += bandaOrdenadoR[len(bandaOrdenadoR)/2]
                soma += bandaOrdenadoR[(len(bandaOrdenadoR)/2) - 1]
                mediana = int(soma/2)
            else:
                mediana = bandaOrdenadoR[math.floor(len(bandaOrdenadoR)/2)]
	
            ImagemMediana[i][j][0] = mediana
			
            #Reinicializando variáveis
            mediana = 0
            soma = 0
            contAltura = limiteAltura
            contLargura = limiteLargura
			
            for k in range(m):
                for l in range(n):
                    bandaG[k][l] = imagem[i - contAltura][j - contLargura][1]
                    contLargura -= 1
                    contAltura -= 1
                    contLargura = limiteLargura
				
            bandaOrdenadoG = np.sort(bandaG, axis = None)
			
            if len(bandaOrdenadoG)%2 == 0:
                soma += bandaOrdenadoG[len(bandaOrdenadoG)/2]
                soma += bandaOrdenadoG[(len(bandaOrdenadoG)/2) - 1]
                mediana = int(soma/2)
            else:
                mediana = bandaOrdenadoG[math.floor(len(bandaOrdenadoG)/2)]
	
            ImagemMediana[i][j][1] = mediana
		
            mediana = 0
            soma = 0
            contAltura = limiteAltura
            contLargura = limiteLargura
			
            for k in range(m):
                for l in range(n):
                    bandaB[k][l] = imagem[i - contAltura][j - contLargura][2]
                    contLargura -= 1
                contAltura -= 1
                contLargura = limiteLargura
				
            bandaOrdenadaB = np.sort(bandaB, axis = None)
			
            if len(bandaOrdenadaB)%2 == 0:
                soma += bandaOrdenadaB[len(bandaOrdenadaB)/2]
                soma += bandaOrdenadaB[(len(bandaOrdenadaB)/2) - 1]
                mediana = int(soma/2)
            else:
                mediana = bandaOrdenadaB[math.floor(len(bandaOrdenadaB)/2)]
	
			
            ImagemMediana[i][j][2] = mediana
			
			
    return ImagemMediana


def filtroMedianaYIQ (imagem, largura, altura, m, n):

    ImagemMediana = imagem.copy()

    limiteAltura = math.floor(m/2)
    limiteLargura = math.floor(n/2)

    #Cria uma matriz de 0`s com a dimensáo do Kernel para cada banda.
                
    bandaY = np.zeros((m,n), dtype = int) 


    soma = 0
    mediana = 0
    
    for i in range(limiteAltura, altura - limiteAltura):               #Laço para percorrer a altura
        for j in range(limiteLargura, largura - limiteLargura):        #Laço para percorrer a largura
	
            contAltura = limiteAltura
            contLargura = limiteLargura
			
            #Laço para percorrer a banda Y dos Pixels da parte da imagem referente ao tamanho do Kernel 
            for k in range(m):
                for l in range(n):
                    bandaY[k][l] = imagem[i - contAltura][j - contLargura][0]  #
                    contLargura -= 1
                    contAltura -= 1
                    contLargura = limiteLargura

            #Ordena os valores da banda y	
            bandaOrdenadoY = np.sort(bandaY, axis = None)
			
            #Verififica se a quantidade de elementos do array ordenado é par ou impar e define a mediana	

            if len(bandaOrdenadoY)%2 == 0:
                soma += bandaOrdenadoY[len(bandaOrdenadoY)/2]
                soma += bandaOrdenadoY[(len(bandaOrdenadoY)/2) - 1]
                mediana = int(soma/2)
            else:
                mediana = bandaOrdenadoY[math.floor(len(bandaOrdenadoY)/2)]
	
            ImagemMediana[i][j][0] = mediana

    return ImagemMediana


#--------------------------------- CHAMADA DAS FUNÇÕES -----------------------------------------------------------


def executaFunc(opcao):                 #Seletor, inserir aqui as chamadas das funcoes de tratamento de imagem
    loop = True
    bandaType = Tk()
    global imagemModificada, arrayModificada, fator
    imagemModificaIsRGB = True
    while loop:
        if opcao == 1:                      #Converter para YIQ
            print('1')
            arrayModificada = RGBYIQ(arrayOriginal, larguraOriginal, alturaOriginal)
            imagemModificada = arrayImagem(arrayModificada)
            exibe(imagemModificada)
            loop = False

        elif opcao == 2:                    #Converter para RGB
            print('2')
            arrayModificada = YIQRGB(arrayModificada, larguraOriginal, alturaOriginal)
            imagemModificada = arrayImagem(arrayModificada)
            exibe(imagemModificada)
            loop = False

        elif opcao == 3:                    #Imagem com banda individual colorida
            print('3')
            bandaType = Tk()
            btnR =  Button(bandaType, text="Banda R", command= lambda: selecionaBanda('R', 'colorida'))
            btnG = Button(bandaType, text="Banda G", command= lambda: selecionaBanda('G', 'colorida'))
            btnB = Button(bandaType, text="Banda B", command= lambda: selecionaBanda('B', 'colorida'))
            btnR.pack()
            btnG.pack()
            btnB.pack()
            loop = False

        elif opcao == 4:                    #Imagem com banda individual monocromática
            print('4')
            btnR =  Button(bandaType, text="Banda R", command= lambda: selecionaBanda('R', 'monocromatica'))
            btnG = Button(bandaType, text="Banda G", command= lambda: selecionaBanda('G', 'monocromatica'))
            btnB = Button(bandaType, text="Banda B", command= lambda: selecionaBanda('B', 'monocromatica'))
            btnR.pack()
            btnG.pack()
            btnB.pack()
            loop = False
            
        elif opcao == 5:                    #Imagem negativa
            print('5')

            if imagemModificaIsRGB is True:
                arrayModificada = filtroNegativoRGB(arrayOriginal, larguraOriginal, alturaOriginal)
                imagemModificada = arrayImagem(arrayModificada)
                exibe(imagemModificada)
                loop = False

            else:
                arrayModificada = filtroNegativoYIQ(arrayOriginal, larguraOriginal, alturaOriginal)
                imagemModificada = arrayImagem(arrayModificada)
                exibe(imagemModificada)
                loop = False     

        elif opcao == 6:                    #Controle de brilho aditivo
            # fator = int(input('Informe o fator de Adição! '))
            
            # if imagemModificaIsRGB is True:
            #     arrayModificada = brilhoMultiplicativoRGB(arrayOriginal, larguraOriginal, alturaOriginal, fator)
            #     imagemModificada = arrayImagem(arrayModificada)
            #     exibe(imagemModificada)
            #     loop = False

        elif opcao == 7:                    #Controle de brilho multiplicativo
            # fator = int(input('Informe o fator de Multiplicação! '))
            
            # if imagemModificaIsRGB is True:
            #     arrayModificada = brilhoMultiplicativoRGB(arrayOriginal, larguraOriginal, alturaOriginal, fator)
            #     imagemModificada = arrayImagem(arrayModificada)
            #     exibe(imagemModificada)
            #     loop = False

        elif opcao == 8:                    #Convolução mxn
            print('8')
        elif opcao == 9:                    #Filtro mediana
            medianaUi = Tk()
            lbMediana = Label(medianaUi, text='Insira os valores M e N')
            lbMediana.pack()
            lbM = Label(medianaUi, text='M =')
            lbN = Label(medianaUi, text='N =')
            m = Entry(medianaUi)
            n = Entry(medianaUi)
            lbM.pack()
            m.pack()
            lbN.pack()
            n.pack()
            if imagemEhRGB is True:
                arrayModificada = filtroMedianaRGB(arrayOriginal, larguraOriginal, alturaOriginal, m, n)
                imagemModificada = arrayImagem(arrayModificada)
                exibe(imagemModificada)
            else:
               arrayModificada = filtroMedianaYIQ(arrayImagemModificada, larguraOriginal, alturaOriginal, m, n)
               imagemModificada = arrayImagem(arrayModificada)
               exibe(imagemModificada)
            loop = False

        elif opcao == 10:                   #Limiarizacao
            print('10')
        elif opcao == 11:                   #Salvar a imagem selecionada
            print('11')
        else:
            print('Opção inválida!')


master = Tk()
master.title("Trabalho 1 - PDI")
listbox = Listbox(master)
listbox = Listbox(master, width=50, height=20, selectmode=SINGLE)
listbox.pack(side="left",fill="both", expand=True)
listbox.insert(END, "############# Menu de Opções ##############")
listbox.insert(1, "1 - Converter para YIQ")
listbox.insert(2, "2 - Converter para RGB")
listbox.insert(3, "3 - Imagem com banda individual colorida")
listbox.insert(4, "4 - Imagem com banda individual monocromática")
listbox.insert(5, "5 - Imagem negativa")
listbox.insert(6, "6 - Controle de brilho aditivo")
listbox.insert(7, "7 - Controle de brilho multiplicativo")
listbox.insert(8, "8 - Convolução mxn")
listbox.insert(9, "9 - Filtro mediana")
listbox.insert(10, "10 - Limiarização")
listbox.insert(11, "11 - Salvar a imagem modificada")
listbox.insert(12, "12 - Finalizar sistema")
# Botoes
selectImg = Button(master, text="Selecionar Imagem", justify=LEFT, command=selecionaImg)
selectImg.pack()
selectFunc = Button(master, text="Executar Função", justify=LEFT, command=selecionaFuncao)
selectFunc.pack()
encerrar = Button(master, text="Encerrar", justify=LEFT, command=master.quit)
encerrar.pack()

mainloop()
