import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.prompt import Prompt
import os
import cv2

# Leitura da imagem
def leitura_Imagem(nome):
    imagem = cv2.imread(nome)
    return imagem

# Realiza a plotagem das imagens com o matplotlib
def plotagem_imagem(Imagem_Original, Imagem_Filtrada_Gauss, Imagem_magnitude_gradiente, Imagem_direcao_gradiente, Imagem_Threshold_High):
    
    # Cria uma figura com todos os subplots
    fig, axs = plt.subplots(1, 5, figsize=(20, 10))
    
    # Adiciona as imagens aos subplots
    axs[0].imshow(Imagem_Original, cmap='gray')
    axs[0].set_title('Imagem Original')
    
    axs[1].imshow(Imagem_Filtrada_Gauss, cmap='gray')
    axs[1].set_title('Imagem Filtrada com Filtro Gaussiano')
    
    axs[2].imshow(Imagem_magnitude_gradiente, cmap='gray')
    axs[2].set_title('Magnitude do Gradiente')
    
    axs[3].imshow(Imagem_direcao_gradiente, cmap='gray')
    axs[3].set_title('Direção do Gradiente')
    
    axs[4].imshow(Imagem_Threshold_High, cmap='gray')
    axs[4].set_title('Imagem com Limiar Alto')
     
    # Remove os eixos das imagens
    for ax in axs.flat:
        ax.axis('off')
    
    # Exibe a figura
    plt.show()
  
# Salva a imagem na pasta de resultados  
def salvar_imagem(Imagem_Binaria, nome):
    
    plt.imsave(nome, Imagem_Binaria, cmap='Greys')
    
# Lista as imagens disponíveis na pasta
def lista_imagens_pasta(pasta, console):
    
    # Lista as imagens disponíveis na pasta
    imagens = [f for f in os.listdir(pasta)]
    
    # Printa as imagens
    for i, imagem in enumerate(imagens):
        console.print('{}. {}'.format(i+1, imagem))
        
    return imagens

# Escolhe uma imagem para aplicar o método de Canny
def escolher_imagens(imagens, console):
    
    # Escolhe uma imagem para aplicar o método de Otsu
    while True:
        escolha = int(Prompt.ask('Escolha uma imagem para aplicar o método de Canny:', console=console))
        
        if escolha > 0 and escolha <= len(imagens):
            return imagens[escolha-1]
        else:
            console.print('Escolha inválida. Tente novamente.')