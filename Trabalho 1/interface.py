from tkinter import Tk #Graphical User Interface
from tkinter.filedialog import askopenfilename
from PIL import Image

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


if __name__ == '__main__':
	main()