FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema para procesar imágenes (OpenCV, etc.) y copiar resto de archivos 
RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY extractores.py .
COPY database/ ./database/

# Exponer puerto de Streamlit
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando de ejecución
ENTRYPOINT ["streamlit", "run", "app.py"]
