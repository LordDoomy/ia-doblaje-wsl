#!/bin/bash

echo "🚀 Iniciando configuración del entorno..."

# 1. Actualizar el sistema y herramientas básicas
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv ffmpeg espeak-ng git libsndfile1

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Actualizar pip y wheel
pip install --upgrade pip setuptools wheel

# 4. Instalar librerías de Python necesarias
pip install \
    faster-whisper \
    transformers \
    torch \
    moviepy \
    pydub \
    edge-tts \
    coqui-tts \
    sentencepiece \
    numpy \
    soundfile

# 5. Crear estructura de carpetas
mkdir -p videos audio final transcript subtitulos modelos

# 6. Descargar modelos MarianMT y Coqui TTS
echo "📦 Descargando MarianMT (en-es) y Coqui TTS..."
python3 <<EOF
from transformers import MarianTokenizer, MarianMTModel
from TTS.utils.manage import ModelManager
import os

# MarianMT
os.makedirs("modelos/marianmt", exist_ok=True)
modelo_marian = "Helsinki-NLP/opus-mt-en-es"
tokenizer = MarianTokenizer.from_pretrained(modelo_marian)
model = MarianMTModel.from_pretrained(modelo_marian)
tokenizer.save_pretrained("modelos/marianmt")
model.save_pretrained("modelos/marianmt")

# Coqui TTS
model_manager = ModelManager()
model_manager.download_model("tts_models/es/css10/vits")
EOF

echo "✅ Entorno configurado correctamente."
echo "👉 Para comenzar: activa el entorno con 'source venv/bin/activate'"