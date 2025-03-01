import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.prompt import Prompt
import os

# Leitura da imagem
def leitura_Imagem(nome):
    print(nome)
    imagem = mpimg.imread(nome)
    return imagem

# Realiza a plotagem das imagens com o matplotlib
def plotagem_imagem(Imagem_Original, Imagem_Filtrada_Gauss, Imagem_Filtrada_Normalizada, Imagem_Threshold_High, Imagem_Threshold_Low, Imagem_Final):
    
    # Cria uma figura com todos os subplots
    fig, axs = plt.subplots(3, 3, figsize=(15,10))
    
    # Plota a imagem original
    axs[0,0].imshow(Imagem_Original, cmap='gray')
    axs[0,0].set_title('Imagem Original')
    
    # Plota a imagem filtrada com o filtro de Gauss
    axs[0,1].imshow(Imagem_Filtrada_Gauss, cmap='gray')
    axs[0,1].set_title('Imagem Filtrada com Filtro de Gauss')
    
    # Plota a imagem filtrada normalizada
    axs[0,2].imshow(Imagem_Filtrada_Normalizada, cmap='gray')
    axs[0,2].set_title('Imagem Filtrada Normalizada')
    
    # Plota a imagem com o threshold alto
    axs[1,0].imshow(Imagem_Threshold_High, cmap='gray')
    axs[1,0].set_title('Imagem com Threshold Alto')
    
    # Plota a imagem com o threshold baixo
    axs[1,1].imshow(Imagem_Threshold_Low, cmap='gray')
    axs[1,1].set_title('Imagem com Threshold Baixo')
    
    # Plota a imagem final
    axs[1,2].imshow(Imagem_Final, cmap='gray')
    axs[1,2].set_title('Imagem Final')
    
    # Remove os eixos das imagens
    for ax in axs.flat:
        ax.axis('off')
    
    # Exibe a figura
    plt.show()
    
def salvar_imagem(Imagem_Binaria, nome):
    
    plt.imsave(nome, Imagem_Binaria, cmap='Greys')
    
def lista_imagens_pasta(pasta, console):
    
    # Lista as imagens disponíveis na pasta
    imagens = [f for f in os.listdir(pasta)]
    
    # Exibe as imagens disponíveis na pasta
    console.print('Imagens disponíveis na pasta:', imagens)
    
    # Printa as imagens
    for i, imagem in enumerate(imagens):
        console.print('{}. {}'.format(i+1, imagem))
        
    return imagens

def escolher_imagens(imagens, console):
    
    # Escolhe uma imagem para aplicar o método de Otsu
    while True:
        escolha = int(Prompt.ask('Escolha uma imagem para aplicar o método de Otsu:', console=console))
        
        if escolha > 0 and escolha <= len(imagens):
            return imagens[escolha-1]
        else:
            console.print('Escolha inválida. Tente novamente.')
    