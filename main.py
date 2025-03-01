import matplotlib.pyplot as plt
import argparse
from rich.console import Console
from rich.prompt import Prompt
import utils
import filters
import Bordas.bordas as bordas

import Utils.utils_imagem as ut_img

# Variáveis para passagem de argumentos via terminal
parser = argparse.ArgumentParser()

# Argumento para salvar a imagem na pasta de resultados
SAVE = parser.add_argument('--save', action='store_true', help='Salvar a imagem na pasta de resultados')


def metodo_canny(imagem_escolhida, tipo, filtro, m_threshold1, n_threshold2):
    
    # Leitura da imagem
    Imagem_Original = ut_img.leitura_Imagem('./imagens/{}'.format(imagem_escolhida))    

    # Aplica a detecção de bordas de Canny
    Imagem_Filtrada_Gauss, Imagem_Filtrada_Normalizada, Imagem_Threshold_High, Imagem_Threshold_Low, Imagem_Final = bordas.Canny(Imagem_Original, m_threshold1, n_threshold2)

    # Realiza a plotagem das imagens
    ut_img.plotagem_imagem(Imagem_Original, Imagem_Filtrada_Gauss, Imagem_Filtrada_Normalizada, Imagem_Threshold_High, Imagem_Threshold_Low, Imagem_Final)
    
    # Salva a imagem na pasta de resultados
    if SAVE:
        ut_img.salvar_imagem(Imagem_Binaria, './resultados/{}_{}_{}_{}x{}.png'.format(tipo,imagem,filtro,m,n))

if __name__ == '__main__':
    
    # Inicializa a console
    console = Console()
    
    # Lista as imagens disponíveis na pasta
    imagens_disponiveis = ut_img.lista_imagens_pasta('./imagens', console)
    
    # Escolhe uma imagem para aplicar o método de Canny
    imagem_escolhida = ut_img.escolher_imagens(imagens_disponiveis, console)
    
    # Define as limiares m e n, para o método de Canny, escolhidas pelo usuário
    m_threshold1 = float(Prompt.ask('Digite o [bold purple]valor[/bold purple] da [bold purple]limiar inferior[/bold purple] [cyan](m)[/cyan] [green](default 0.3)[/green]', default=0.3))
    n_threshold2 = float(Prompt.ask('Digite o [bold purple]valor[/bold purple] da [bold purple]limiar superior[/bold purple] [cyan](n)[/cyan] [green](default 0.7)[/green]', default=0.7))
    
    metodo_canny(imagem_escolhida ,'canny', 'Gaussian', m_threshold1, n_threshold2)