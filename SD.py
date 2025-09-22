# %%
import os
import numpy as np
import import_images
from csbdeep.utils import normalize
from stardist.models import StarDist2D
import matplotlib.pyplot as plt
from skimage.segmentation import find_boundaries
from skimage.io import imsave

# %%
# Carrega o modelo pré-treinado
model = StarDist2D.from_pretrained('2D_versatile_fluo')

# Caminho da pasta com imagens
base_dir = "/home/kayllany.oliveira/remote-repos/CellViability/data/17 Resultados HTS SLEV/SLEV HTS TargetMol/S_1_R1[10270]"

# Lista todas as imagens da pasta e cria dicionário
image_paths = import_images.encontrar_imagens_tiff(base_dir)

# Cria pasta de saída
output_dir = os.path.join(os.getcwd(), "resultados", "stardist")
os.makedirs(output_dir, exist_ok=True)

# Loop por todas as imagens
for idx, img_path in image_paths.items():
    print(f"Processando {img_path} ...")
    
    # Carrega a imagem
    image = import_images.carregar_imagem_por_indice(image_paths, idx)
    if image is None:
        print("Falha ao carregar a imagem, pulando...")
        continue

    # Normalização para [0,1]
    img_float = image.astype(np.float32)
    img_float -= img_float.min()
    maxv = img_float.max()
    if maxv > 0:
        img_float /= maxv
    image_norm = img_float

    # Predição do modelo
    labels, details = model.predict_instances(normalize(image))

    # Nome base do arquivo
    nome_original = os.path.splitext(os.path.basename(img_path))[0]

    # ---------- Salva máscara rotulada como uint16 ----------
    mask_path = os.path.join(output_dir, f"{nome_original}_mask_labels.png")
    imsave(mask_path, labels.astype(np.uint16))
    print(f"Máscara rotulada salva em: {mask_path}")

    # ---------- Cria overlay com contorno vermelho ----------
    image_rgb = np.stack([image_norm, image_norm, image_norm], axis=-1)
    contornos = find_boundaries(labels, mode='outer')
    overlay_contorno = image_rgb.copy()
    overlay_contorno[contornos] = np.array([1.0, 0.0, 0.0], dtype=np.float32)

    contorno_path = os.path.join(output_dir, f"{nome_original}_contorno.png")
    plt.imsave(contorno_path, overlay_contorno)
    print(f"Overlay com contorno vermelho salvo em: {contorno_path}")

    # ---------- Salva subplot para visualização ----------
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].imshow(image_norm, cmap="gray")
    ax[0].axis("off")
    ax[0].set_title("Input image")

    ax[1].imshow(overlay_contorno)
    ax[1].axis("off")
    ax[1].set_title("Contours")

    subplot_path = os.path.join(output_dir, f"{nome_original}_subplot_contorno.png")
    plt.savefig(subplot_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Subplot salvo em: {subplot_path}")

print("Processamento concluído para todas as imagens.")
# %%
