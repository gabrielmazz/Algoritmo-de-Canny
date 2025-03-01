import matplotlib.pyplot as plt
import argparse
from rich.console import Console
from rich.prompt import Prompt
import Bordas.bordas as bordas
import cv2
import Utils.utils_imagem as ut_img

# Variáveis para passagem de argumentos via terminal
parser = argparse.ArgumentParser()

# Argumento para salvar a imagem na pasta de resultados
SAVE = parser.add_argument('--save', action='store_true', help='Salvar a imagem na pasta de resultados')

def metodo_canny(imagem_escolhida, tipo, filtro, low_threshold_ratio, high_threshold_ratio, sigma):
    
    # Leitura da imagem
    Imagem_Original = cv2.imread('./imagens/{}'.format(imagem_escolhida), cv2.IMREAD_GRAYSCALE)

    # Aplica a detecção de bordas de Canny
    Imagem_Filtrada_Gauss, Imagem_magnitude_gradiente, Imagem_direcao_gradiente, Imagem_Threshold_High = bordas.Canny(Imagem_Original, 5, sigma, low_threshold_ratio, high_threshold_ratio)

    # Realiza a plotagem das imagens
    ut_img.plotagem_imagem(Imagem_Original, Imagem_Filtrada_Gauss, Imagem_magnitude_gradiente, Imagem_direcao_gradiente, Imagem_Threshold_High)
    
    # Salva a imagem na pasta de resultados
    if SAVE:
        ut_img.salvar_imagem(Imagem_Threshold_High, './resultados/{}_{}_{}_{}x{}.png'.format(tipo,imagem_escolhida,filtro,m,n))

if __name__ == '__main__':
    
    # Inicializa a console
    console = Console()
    
    # Lista as imagens disponíveis na pasta
    imagens_disponiveis = ut_img.lista_imagens_pasta('./imagens', console)
    
    # Escolhe uma imagem para aplicar o método de Canny
    imagem_escolhida = ut_img.escolher_imagens(imagens_disponiveis, console)
    
    # Define as limiares m e n, para o método de Canny, escolhidas pelo usuário
    low_threshold_ratio = float(Prompt.ask('Digite o [bold purple]valor[/bold purple] da [bold purple]limiar inferior[/bold purple] [cyan](m)[/cyan] [green](default 0.05)[/green]', default=0.05))
    high_threshold_ratio = float(Prompt.ask('Digite o [bold purple]valor[/bold purple] da [bold purple]limiar superior[/bold purple] [cyan](n)[/cyan] [green](default 0.09)[/green]', default=0.09))
    sigma = float(Prompt.ask('Digite o [bold purple]valor[/bold purple] do [bold purple]sigma[/bold purple] [cyan](sigma)[/cyan] [green](default 1)[/green]', default=1))
    
    # Aplica o método de Canny
    metodo_canny(imagem_escolhida ,'canny', 'Gaussian', low_threshold_ratio, high_threshold_ratio, sigma)