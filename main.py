import matplotlib.pyplot as plt
import argparse
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress
import Bordas.bordas as bordas
import cv2
import Utils.utils_imagem as ut_img
import Utils.utils_code as ut_code
import time
import Utils.library_checker as lib_checker

# Variáveis para passagem de argumentos via terminal
parser = argparse.ArgumentParser()

# Argumento para salvar a imagem na pasta de resultados
SAVE = parser.add_argument('--save', action='store_true', help='Salvar a imagem na pasta de resultados')
INFO = parser.add_argument('--info', action='store_true', help='Exibir o tempo de execução')
URL_IMAGE = parser.add_argument('--url', type=str, help='URL da imagem para usar no algoritmo')

def metodo_canny(imagem_escolhida, tipo, filtro, low_threshold_ratio, high_threshold_ratio, sigma):
    
    # Inicializa a variável de tempo
    tempo_inicio = time.time()
    
    with Progress() as progress:
    
        # Adiciona uma tarefa barra de progresso
        task = progress.add_task("[cyan]Processando...", total=3)
        
        # Leitura da imagem
        progress.update(task, advance=1, description='[cyan]Lendo a imagem...')
        Imagem_Original = cv2.imread('./imagens/{}'.format(imagem_escolhida), cv2.IMREAD_GRAYSCALE)

        time.sleep(1)

        # Aplica a detecção de bordas de Canny
        progress.update(task, advance=1, description='[cyan]Aplicando o método de Canny...')
        Imagem_Filtrada_Gauss, Imagem_magnitude_gradiente, Imagem_direcao_gradiente, Imagem_Threshold_High = bordas.Canny(Imagem_Original, 5, sigma, low_threshold_ratio, high_threshold_ratio)

        time.sleep(1)
        
        # Calcula o tempo de execução
        tempo_execucao = time.time() - tempo_inicio - 2

        # Realiza a plotagem das imagens
        progress.update(task, advance=1, description='[cyan]Plotando as imagens...')
        ut_img.plotagem_imagem(Imagem_Original, Imagem_Filtrada_Gauss, Imagem_magnitude_gradiente, Imagem_direcao_gradiente, Imagem_Threshold_High)
        
    time.sleep(1)
    ut_code.clear_terminal()
    
     # Deleta a imagem baixada
    if args.url:
        ut_img.deletar_imagem(imagem_escolhida)
        
    # Exibe o tempo de execução
    if args.info:
        ut_code.print_infos_table(tempo_execucao, tipo, filtro, low_threshold_ratio, high_threshold_ratio, sigma, imagem_escolhida)
        
    # Salva a imagem na pasta de resultados
    if args.save:
        ut_img.salvar_imagem(Imagem_Threshold_High, './resultados/{}_{}_{}_{}_{}_{}.png'.format(tipo, filtro, low_threshold_ratio, high_threshold_ratio, sigma, imagem_escolhida))
        
if __name__ == '__main__':
    
    # Verifica se o usuário passou uma URL de imagem
    args = parser.parse_args()
    
    # Verifica se todas as bibliotecas estão instaladas
    lib_checker.check_library()
    
    # Funções triviais
    ut_code.clear_terminal()
    ut_code.print_title()
    
     # Baixa a imagem da URL
    if args.url:
        ut_img.download_imagem(args)
    
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