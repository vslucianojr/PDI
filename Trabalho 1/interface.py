from tkinter import *  # Graphical User Interface
from tkinter.filedialog import askopenfilename
from PIL import Image
import numpy as np


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


def exibe(imagem):  # Esta exibindo grande demais, precisa ajustar o tamanho de exibiçao da imagem
    imagem.show()


def selecionaFuncao():
    select = listbox.curselection()  # Capturando qual item esta selecionado na listbox
    for item in select:
        # Chamando o seletor de funções passando qual item esta selecionado
        executaFunc(item)

# transforma a imagem em array


def imagemArray(imagem):
    return np.asarray(imagem)

# transforma o array em imagem


def arrayImagem(array):

    imagem = Image.fromarray(array, mode='RGB')

    return imagem

# converte a imagem de RGB para YIQ


def RGBYIQ(imagemRGB, largura, altura):

    # copia a imagem e transforma array em float para os calculos de conversão
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


def YIQRGB(imagemYIQ, largura, altura):
    # converter imagem para int
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

def executaFunc(opcao):                 #Seletor, inserir aqui as chamadas das funcoes de tratamento de imagem
    loop = True
    global imagemModificada, arrayModificada
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
        elif opcao == 4:                    #Imagem com banda individual monocromática
            print('4')
        elif opcao == 5:                    #Imagem negativa
            print('5')
        elif opcao == 6:                    #Controle de brilho aditivo
            print('6')
        elif opcao == 7:                    #Controle de brilho multiplicativo
            print('7')
        elif opcao == 8:                    #Convolução mxn
            print('8')
        elif opcao == 9:                    #Filtro mediana
            print('9')
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
