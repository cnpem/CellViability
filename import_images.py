# Importa o módulo imageio.v3 para leitura de imagens
import imageio.v3 as iio

# Importa glob para buscar arquivos com padrões nos nomes
import glob

# Importa os para manipulação de diretórios e caminhos
import os


def encontrar_imagens_tiff(base_dir):
    """
    Procura por arquivos de imagem com extensão .tif ou .tiff em uma pasta base e suas subpastas.

    Parâmetro:
        base_dir (str): Caminho da pasta onde a busca será feita.

    Retorno:
        dict: Um dicionário onde as chaves são índices e os valores são caminhos completos para os arquivos de imagem encontrados.
    """
    # Busca por todos os arquivos .tiff em todas as subpastas (recursive=True)
    tiff_files = glob.glob(os.path.join(base_dir, "**", "*.tiff"), recursive=True)

    # Adiciona também os arquivos com extensão .tif
    tiff_files += glob.glob(os.path.join(base_dir, "**", "*.tif"), recursive=True)

    # Cria um dicionário associando cada caminho a um índice (0, 1, 2, ...)
    return {i: path for i, path in enumerate(tiff_files)}


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


