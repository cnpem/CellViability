# %%
import os
import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from skimage import measure
from cellpose import models
import import_images  # seu script de carregar imagens

# %%
# Caminho da pasta com imagens
base_dir = "/home/kayllany.oliveira/remote-repos/CellViability/data/17 Resultados HTS SLEV/SLEV HTS TargetMol/S_1_R1[10270]/2022-04-11T161022Z[10923]"

# Encontra todas as imagens .tif
image_paths = import_images.encontrar_imagens_tiff(base_dir)

# Cria pasta de saída
output_dir = os.path.join(os.getcwd(), "resultados", "cellpose_sam")
os.makedirs(output_dir, exist_ok=True)

# Inicializa modelo Cellpose-SAM
modelo = models.CellposeModel(
    gpu=True,
    pretrained_model='cpsam',
)

# Loop por cada imagem
for idx, img_path in image_paths.items():
    print(f"Processando {img_path} ...")
    
    # Carrega imagem usando seu script
    img = import_images.carregar_imagem_por_indice(image_paths, idx)
    if img is None:
        print("Falha ao carregar imagem, pulando...")
        continue
    
    # Avaliação (grayscale, sem rescale)
    masks, flows, styles = modelo.eval(
        [img],
        channels=[0, 0],
        diameter=15,
        flow_threshold=1,
        cellprob_threshold=1.5,
        compute_masks=True,
    )

    # Nome original da imagem
    nome_original = os.path.splitext(os.path.basename(img_path))[0]

    # ---------- Salva máscara rotulada como PNG grayscale ----------
    mask_labeled_uint16 = masks[0].astype(np.uint16)
    mask_path_labels = os.path.join(output_dir, f"{nome_original}_mask_labels.png")
    Image.fromarray(mask_labeled_uint16).save(mask_path_labels, format='PNG')
    print(f"Máscara rotulada salva em: {mask_path_labels}")

    # ---------- Cria overlay apenas com contornos ----------
    fig, ax = plt.subplots()
    ax.imshow(img, cmap='gray')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # remove margens

    for cell_label in np.unique(masks[0]):
        if cell_label == 0:
            continue
        cell_mask = masks[0] == cell_label
        contours = measure.find_contours(cell_mask, 0.5)
        for contour in contours:
            ax.plot(contour[:, 1], contour[:, 0], linewidth=1, color='lime')  # contorno verde

    ax.axis('off')
    overlay_path = os.path.join(output_dir, f"{nome_original}_overlay_contorno.png")
    plt.savefig(overlay_path, dpi=600, transparent=True)
    plt.close(fig)
    print(f"Overlay com contorno salvo em: {overlay_path}")

print("Processamento concluído para todas as imagens.")
# %%
