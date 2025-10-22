from PIL import Image
import numpy as np
import pandas as pd
import faiss
from pathlib import Path

# Carpetas
IMAGES_FOLDER = Path("../images")  # imágenes de entrenamiento
DB_PATH = Path("../database")
DB_PATH.mkdir(exist_ok=True)

# Archivos
DB_FILE = "db.csv"
INDEX_FILE = "extract_rgb_histogram.index"

# Función de ejemplo (histograma RGB)
def extract_rgb_histogram(img, size=(224,224)):
    img = img.resize(size)
    img_np = np.array(img)
    hist_r = np.histogram(img_np[:,:,0], bins=16, range=(0,255))[0]
    hist_g = np.histogram(img_np[:,:,1], bins=16, range=(0,255))[0]
    hist_b = np.histogram(img_np[:,:,2], bins=16, range=(0,255))[0]
    hist = np.concatenate([hist_r,hist_g,hist_b]).astype(np.float32)
    hist /= np.linalg.norm(hist) + 1e-6
    return hist.reshape(1,-1)

# Extraer descriptores
features = []
image_files = []

for img_path in sorted(IMAGES_FOLDER.glob("*.*")):
    img = Image.open(img_path).convert("RGB")
    feat = extract_rgb_histogram(img)
    features.append(feat)
    image_files.append(img_path.name)

features = np.vstack(features).astype(np.float32)
faiss.normalize_L2(features)

# Crear índice FAISS
index = faiss.IndexFlatL2(features.shape[1])
index.add(features)
faiss.write_index(index, str(DB_PATH / INDEX_FILE))

# Guardar CSV
pd.DataFrame({'image': image_files}).to_csv(DB_PATH / DB_FILE, index=False)

print(f"✅ FAISS index y CSV creados con {len(image_files)} imágenes")
print(features.shape)
print(index.code_size)