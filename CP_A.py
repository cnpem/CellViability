# %%
import os
from PIL import Image
import matplotlib.pyplot as plt
from skimage import measure
import cellpose.models
import bioio
import numpy as np
import import_images
import torch

# %%
base_dir = "/home/kayllany.oliveira/remote-repos/CellViability/data/17 Resultados HTS SLEV/SLEV HTS TargetMol/S_1_R1[10270]/2022-04-11T161022Z[10923]"

# Encontra todas as imagens .tif
image_paths = import_images.encontrar_imagens_tiff(base_dir)

# Cria pasta de saída
output_dir = os.path.join(os.getcwd(), "resultados", "cellpose")
os.makedirs(output_dir, exist_ok=True)

# Inicializa modelo Cellpose-SAM
model = cellpose.models.CellposeModel(gpu=True, model_type='nuclei')

# Loop por cada imagem
for idx, img_path in image_paths.items():
    print(f"Processando {img_path} ...")
    
    # Carrega imagem usando seu script
    img = bioio.BioImage(img_path)
    image = img.data[0,0,0]

    # ---------- Inferência ----------
    masks, flows, styles = model.eval(
        image,
        channels=[0,0],
        diameter=15,
        do_3D=False
    )

    # Converte máscaras para inteiro long (PyTorch safe)
    if isinstance(masks, torch.Tensor):
        masks = masks.long().cpu().numpy()

    # Nome original da imagem
    nome_original = os.path.splitext(os.path.basename(img_path))[0]

    # ---------- Salva máscara rotulada como PNG grayscale ----------
    mask_labeled_uint16 = masks.astype(np.uint16)  # preserva rótulos > 255
    mask_path_labels = os.path.join(output_dir, f"{nome_original}_mask_labels.png")
    Image.fromarray(mask_labeled_uint16).save(mask_path_labels, format='PNG')
    print(f"Máscara rotulada salva em: {mask_path_labels}")

    # ---------- Cria overlay apenas com contornos ----------
    fig, ax = plt.subplots()
    ax.imshow(image, cmap='gray')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # remove margens

    for cell_label in np.unique(masks):
        if cell_label == 0:
            continue
        cell_mask = masks == cell_label
        contours = measure.find_contours(cell_mask, 0.5)
        for contour in contours:
            ax.plot(contour[:, 1], contour[:, 0], linewidth=1, color='lime')

    ax.axis('off')
    overlay_path = os.path.join(output_dir, f"{nome_original}_overlay_contorno.png")
    plt.savefig(overlay_path, dpi=600, transparent=True)
    plt.close(fig)
    print(f"Overlay com contorno salvo em: {overlay_path}")

    print(f"Máscaras processadas: {np.unique(masks)}")

print("Processamento concluído para todas as imagens.")
# %%

