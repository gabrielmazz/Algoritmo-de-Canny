import numpy as np
import utils
import filters

def otsu(imagem):
    
    # Verifica se a imagem é colorida e converte para escala de cinza
    if len(imagem.shape) > 2:
        imagem = imagem[:, :, 0]  # Usa apenas o primeiro canal (vermelho) para escala de cinza
    
    # Obtém as dimensões da imagem
    altura, largura = imagem.shape
    
    # Cria a imagem binária de retorno com o mesmo tamanho da imagem original
    imagemRetorno = np.zeros((altura, largura))
    
    # Calcula o histograma da imagem
    hist, _ = np.histogram(imagem, bins=256, range=(0, 256))
    
    # Normaliza o histograma para obter as probabilidades
    prob = hist / hist.sum()
    
    # Inicializa variáveis para o cálculo do limiar ótimo
    limiar_otimo = 0
    variancia_max = 0
    
    # Itera sobre todos os possíveis limiares
    for k in range(1, 255):
        
        # Probabilidade acumulada da classe 1
        probAcumulada = np.sum(prob[:k])
        
        # Média acumulada da classe 1
        if probAcumulada > 0:
            medAcumulada = np.sum(np.arange(k) * prob[:k]) / probAcumulada
        else:
            medAcumulada = 0
        
        # Média global da imagem
        mediaGlobal = np.mean(imagem)
        
        # Calcula a variância entre as classes
        q = probAcumulada * (1 - probAcumulada)
        if q == 0:  # Evita divisão por zero
            continue
        
        variancia = ((mediaGlobal * probAcumulada - medAcumulada) ** 2) / q
        
        # Atualiza o limiar ótimo se a variância for maior
        if variancia > variancia_max:
            variancia_max = variancia
            limiar_otimo = k
    
    # Cria a imagem binária com base no limiar ótimo
    for x in range(altura):
        for y in range(largura):
            if imagem[x, y] > limiar_otimo:
                imagemRetorno[x, y] = 0
            else:
                imagemRetorno[x, y] = 1
    
    return imagemRetorno
            
def limirizacaoLocal(imagem, tipoMedia = 'local', n = 20, a = 0, b = 1 ): 
    limit = int(n/2)
    aux = np.shape(imagem)
    
    if np.size(aux) > 2:
        imagem = imagem[:,:,0]
        aux = np.shape(imagem) 

    segmImg = np.zeros(aux)
    for j in range(0, aux[0]):
        for i in range(0, aux[1]):
            area = imagem[utils.increment(-limit,j,aux[0]):utils.increment(limit,j,aux[0]), utils.increment(-limit,i,aux[1]):utils.increment(limit,i,aux[1])]
            Txy = a*np.var(area) + b*(np.mean(area) if tipoMedia == 'local' else np.mean(imagem))
            segmImg[j][i] = 1 if imagem[j][i] > Txy else 0
    return segmImg

# def dividirFundirRegioes(imagem)
#   TODO
#   usará os metodos dividiRegiao e uniRegiao em utils