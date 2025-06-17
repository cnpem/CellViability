# Importa o módulo imageio.v3 para leitura de imagens
import imageio.v3 as iio

# Importa glob para buscar arquivos com padrões nos nomes
import glob

# Importa os para manipulação de diretórios e caminhos
import os

def encontrar_imagens_tiff(base_dir):
    arquivos_encontrados = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith('.tif'):  # para aceitar .tif ou .TIF
                caminho_completo = os.path.join(root, file)
                print(caminho_completo)  # debug para ver os arquivos
                arquivos_encontrados.append(caminho_completo)

    # ordenar a lista para consistência
    arquivos_encontrados.sort()

    # converter para dicionário índice: caminho
    return {i: path for i, path in enumerate(arquivos_encontrados)}


def carregar_imagem_por_indice(image_paths, indice):
    """
    Carrega uma imagem a partir do índice fornecido, com base no dicionário de caminhos de imagem.

    Parâmetros:
        image_paths (dict): Dicionário com índices e caminhos de imagem.
        indice (int): Índice da imagem que se deseja carregar.

    Retorno:
        ndarray ou None: Retorna a imagem como array se o índice for válido, senão retorna None.
    """
    # Verifica se o índice existe no dicionário
    if indice in image_paths:
        # Carrega a imagem do caminho correspondente
        image = iio.imread(image_paths[indice])

        # Mostra qual imagem foi carregada e suas dimensões (altura, largura, canais)
        print(f"Imagem carregada: {image_paths[indice]} - Dimensão: {image.shape}")
        return image
    else:
        # Caso o índice seja inválido, mostra mensagem de erro
        print(f"Índice {indice} inválido. Total de imagens disponíveis: {len(image_paths)}")
        return None


# Bloco principal que roda apenas se o script for executado diretamente (não quando importado como módulo)
if __name__ == "__main__":
    # Define a pasta atual como base para busca de imagens
    base_dir = os.getcwd()

    # Encontra todas as imagens .tif e .tiff na pasta e subpastas
    image_paths = encontrar_imagens_tiff(base_dir)

    # Exibe a quantidade total de imagens encontradas
    print(f"Total de imagens encontradas: {len(image_paths)}")

    # Exemplo de uso: tenta carregar a imagem de índice 0
    carregar_imagem_por_indice(image_paths, 0)


