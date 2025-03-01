import matplotlib.pyplot as plt
import argparse
from rich.console import Console
import utils
import filters
import bordas
import segmentacao

import Utils.utils_imagem as ut_img

# Variáveis para passagem de argumentos via terminal
parser = argparse.ArgumentParser()

# Argumento para salvar a imagem na pasta de resultados
SAVE = parser.add_argument('--save', action='store_true', help='Salvar a imagem na pasta de resultados')


def metodo_otsu(imagem_escolhida, tipo, filtro, m, n):
    
    # Leitura da imagem
    Imagem_Original = ut_img.leitura_Imagem('./imagens/{}'.format(imagem_escolhida))    

    # Binarização da imagem com o método de Otsu
    Imagem_Binaria = segmentacao.otsu(Imagem_Original) 
    
    # ImgFiltrada = bordas.Derivative(Imagem_Original,tipo, filtro,m,n)
    
    # limiar = 0.1*np.mean(ImgFiltrada)
    # Imagem_Binaria = utils.Threshold(ImgFiltrada,limiar)   

    ##--> OUTRO METODO DE BINARIZACAO
    # Imagem_Binaria = bordas.Canny(Imagem_Original,m,n) 


    # Realiza a plotagem das imagens
    ut_img.plotagem_imagem(Imagem_Original, Imagem_Binaria)
    
    # Salva a imagem na pasta de resultados
    if SAVE:
        ut_img.salvar_imagem(Imagem_Binaria, './resultados/{}_{}_{}_{}x{}.png'.format(tipo,imagem,filtro,m,n))

if __name__ == '__main__':
    
    # Inicializa a console
    console = Console()
    
    # Lista as imagens disponíveis na pasta
    imagens_disponiveis = ut_img.lista_imagens_pasta('./imagens', console)
    
    # Escolhe uma imagem para aplicar o método de Otsu
    imagem_escolhida = ut_img.escolher_imagens(imagens_disponiveis, console)
    
    metodo_otsu(imagem_escolhida ,'otsu','Gaussian', 0.3, 0.7)