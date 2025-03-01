import numpy as np
import cv2
from scipy.signal import convolve2d

# Função para aplicar o filtro gaussiano
def gaussian_kernel(size, sigma=1):
    
    # Converte o tamanho do kernel para um inteiro e calcula metade do tamanho
    # Isso é feito porque o kernel é simétrico em torno do centro
    size = int(size) // 2

    # Cria uma grade de coordenadas x e y usando np.mgrid
    # Isso gera dois arrays 2D representando as coordenadas x e y de cada ponto no kernel
    # O intervalo vai de -size a size (inclusive), criando um grid quadrado
    x, y = np.mgrid[-size:size+1, -size:size+1]

    # Calcula a constante de normalização do kernel Gaussiano
    # A fórmula é 1 / (2 * pi * sigma^2), que garante que a soma total do kernel seja 1
    normal = 1 / (2.0 * np.pi * sigma**2)

    # Calcula o kernel Gaussiano usando a fórmula:
    # G(x, y) = (1 / (2 * pi * sigma^2)) * exp(-(x^2 + y^2) / (2 * sigma^2))
    # Aqui, x^2 + y^2 representa a distância ao quadrado de cada ponto ao centro do kernel
    g = np.exp(-((x**2 + y**2) / (2.0 * sigma**2))) * normal

    # Retorna o kernel Gaussiano calculado
    return g

# Função para aplicar o filtro gaussiano
def apply_gaussian_filter(image, kernel_size, sigma):
    
    # Criar o kernel gaussiano usando a função gaussian_kernel
    # O kernel_size define o tamanho do kernel (por exemplo, 5x5)
    # O sigma controla a dispersão do filtro Gaussiano
    kernel = gaussian_kernel(kernel_size, sigma)
    
    # Obter as dimensões do kernel (altura e largura)
    kernel_height, kernel_width = kernel.shape
    
    # Calcular o padding necessário para aplicar o filtro nas bordas da imagem
    # O padding é metade da altura e largura do kernel, arredondado para baixo
    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    # Aplicar o padding na imagem original
    # O padding é adicionado ao redor da imagem para que o filtro possa ser aplicado nas bordas
    # O modo 'constant' preenche as bordas com um valor constante (padrão é 0)
    padded_image = np.pad(image, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant')
    
    # Inicializar a imagem de saída com o mesmo formato da imagem original
    output = np.zeros_like(image)

    # Percorrer cada pixel da imagem original
    for i in range(image.shape[0]):  # Loop sobre as linhas da imagem
        for j in range(image.shape[1]):  # Loop sobre as colunas da imagem
            # Aplicar o filtro Gaussiano no pixel atual
            # Extrair a região da imagem que corresponde ao tamanho do kernel
            # Multiplicar a região pelo kernel e somar os resultados
            output[i, j] = np.sum(padded_image[i:i+kernel_height, j:j+kernel_width] * kernel)

    # Retornar a imagem filtrada
    return output

def sobel_filters(image):
    
    # Define os kernels de Sobel para detecção de bordas
    # Kx é o kernel de Sobel para detecção de bordas horizontais
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    
    # Ky é o kernel de Sobel para detecção de bordas verticais
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float32)

    # Aplica a convolução da imagem com o kernel Kx para detectar bordas horizontais
    # O modo 'same' garante que a saída tenha o mesmo tamanho da imagem original
    Ix = convolve2d(image, Kx, mode='same')
    
    # Aplica a convolução da imagem com o kernel Ky para detectar bordas verticais
    Iy = convolve2d(image, Ky, mode='same')

    # Calcula a magnitude do gradiente combinando Ix e Iy
    # A função np.hypot calcula a hipotenusa, que é a magnitude do gradiente
    G = np.hypot(Ix, Iy)
    
    # Normaliza a magnitude do gradiente para o intervalo [0, 255]
    G = G / G.max() * 255

    # Calcula a direção do gradiente usando a função np.arctan2
    # A direção do gradiente indica a orientação das bordas na imagem
    theta = np.arctan2(Iy, Ix)

    # Retorna a magnitude do gradiente (G) e a direção do gradiente (theta)
    return G, theta

def non_max_suppression(G, theta):
    
    # Obtém as dimensões da imagem de magnitude do gradiente (G)
    M, N = G.shape
    
    # Inicializa uma matriz de zeros com o mesmo tamanho da imagem para armazenar o resultado
    Z = np.zeros((M, N), dtype=np.float32)
    
    # Converte a direção do gradiente (theta) de radianos para graus
    angle = theta * 180. / np.pi
    
    # Ajusta ângulos negativos para o intervalo [0, 180]
    angle[angle < 0] += 180

    # Percorre cada pixel da imagem, exceto as bordas
    for i in range(1, M-1):  # Loop sobre as linhas
        for j in range(1, N-1):  # Loop sobre as colunas
            # Inicializa os valores dos pixels vizinhos (q e r) como 255
            q = 255
            r = 255

            # Verifica a direção do gradiente e define os pixels vizinhos a serem comparados
            # Ângulo 0 ou 180 graus (bordas horizontais)
            if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                q = G[i, j+1]  # Pixel à direita
                r = G[i, j-1]  # Pixel à esquerda
            
            # Ângulo 45 graus (bordas diagonais)
            elif (22.5 <= angle[i,j] < 67.5):
                q = G[i+1, j-1]  # Pixel na diagonal inferior esquerda
                r = G[i-1, j+1]  # Pixel na diagonal superior direita
            
            # Ângulo 90 graus (bordas verticais)
            elif (67.5 <= angle[i,j] < 112.5):
                q = G[i+1, j]  # Pixel abaixo
                r = G[i-1, j]  # Pixel acima
            
            # Ângulo 135 graus (bordas diagonais)
            elif (112.5 <= angle[i,j] < 157.5):
                q = G[i-1, j-1]  # Pixel na diagonal superior esquerda
                r = G[i+1, j+1]  # Pixel na diagonal inferior direita

            # Verifica se o pixel atual é um máximo local na direção do gradiente
            if (G[i,j] >= q) and (G[i,j] >= r):
                Z[i,j] = G[i,j]  # Mantém o valor do pixel
            else:
                Z[i,j] = 0  # Suprime o pixel (define como 0)

    # Retorna a imagem após a supressão de não-máximos
    return Z

def hysteresis_thresholding(image, low_threshold_ratio, high_threshold_ratio):
    
    # Calcula os limiares alto e baixo com base nos valores máximos da imagem
    high_threshold = image.max() * high_threshold_ratio
    low_threshold = high_threshold * low_threshold_ratio

    # Obtém as dimensões da imagem
    M, N = image.shape
    
    # Inicializa uma matriz de zeros com o mesmo tamanho da imagem para armazenar o resultado
    res = np.zeros((M, N), dtype=np.float32)
    
    # Define os valores para pixels fracos e fortes
    weak = np.float32(25)  # Valor para pixels fracos
    strong = np.float32(255)  # Valor para pixels fortes

    # Identifica os pixels que são fortes (acima do limiar alto)
    strong_i, strong_j = np.where(image >= high_threshold)
    
    # Identifica os pixels que são fracos (entre os limiares baixo e alto)
    weak_i, weak_j = np.where((image <= high_threshold) & (image >= low_threshold))

    # Atribui os valores fortes e fracos à matriz de resultado
    res[strong_i, strong_j] = strong  # Pixels fortes
    res[weak_i, weak_j] = weak  # Pixels fracos

    # Percorre cada pixel da imagem, exceto as bordas
    for i in range(1, M-1):  # Loop sobre as linhas
        for j in range(1, N-1):  # Loop sobre as colunas
            # Verifica se o pixel atual é fraco
            if (res[i,j] == weak):
                # Verifica se algum dos 8 vizinhos é forte
                if ((res[i+1, j-1] == strong) or (res[i+1, j] == strong) or (res[i+1, j+1] == strong)
                    or (res[i, j-1] == strong) or (res[i, j+1] == strong)
                    or (res[i-1, j-1] == strong) or (res[i-1, j] == strong) or (res[i-1, j+1] == strong)):
                    # Se algum vizinho for forte, o pixel atual é promovido a forte
                    res[i,j] = strong
                else:
                    # Caso contrário, o pixel é suprimido (definido como 0)
                    res[i,j] = 0

    # Retorna a imagem após a limiarização com histerese
    return res

def Canny(image, kernel_size, sigma, low_threshold_ratio, high_threshold_ratio):
    
    # Aplica o filtro gaussiano
    Imagem_Filtrada_Gauss = apply_gaussian_filter(image, kernel_size, sigma)

    # Calcula o gradiente da imagem
    Imagem_magnitude_gradiente, Imagem_direcao_gradiente = sobel_filters(Imagem_Filtrada_Gauss)

    # Aplica a supressão de não-máximos
    Imagem_Suprimida = non_max_suppression(Imagem_magnitude_gradiente, Imagem_direcao_gradiente)

    # Aplica a limiarização por histerese
    Imagem_Threshold_High = hysteresis_thresholding(Imagem_Suprimida, low_threshold_ratio, high_threshold_ratio)

    return Imagem_Filtrada_Gauss, Imagem_magnitude_gradiente, Imagem_direcao_gradiente, Imagem_Threshold_High