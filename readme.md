# 🎙️ IA-Doblaje: Doblaje Automático de Vídeos (Inglés → Español)

Este proyecto permite **doblar automáticamente vídeos en inglés al español**, incluyendo:
- Transcripción con timestamps (vía `faster-whisper`)
- Traducción local (vía `MarianMT`)
- Síntesis de voz natural (vía `Coqui TTS`)
- Reconstrucción del vídeo final sincronizado
- Exportación de subtítulos `.srt`

¡Todo se ejecuta localmente, sin dependencias de APIs externas!

---

## 📁 Estructura del Proyecto
ia-doblaje-wsl/
├── videos/ # Carpeta donde colocas tus vídeos originales (.mp4)
├── audio/ # Archivos de audio intermedios (extraído, doblado)
├── final/ # Vídeos doblados generados (.mp4)
├── transcript/ # Transcripciones (.txt)
├── subtitulos/ # Subtítulos en formato .srt
├── doblar_video.py # Script principal de doblaje
├── setup_entorno.py # Script que prepara TODO el entorno
├── README.md # Esta guía


---

## 🚀 Instalación rápida

### ✅ Requisitos previos:
- Tener **WSL2** instalado con una distro como Ubuntu
- Tener **Python 3.10+** instalado en WSL
- Tener conexión a internet durante la instalación

### 🧠 Paso 1: Clona el repositorio

`git clone https://github.com/Lord_Doomy/ia-doblaje-wsl.git`
`cd ia-doblaje-wsl`

### ⚙️ Paso 2: Ejecuta el script de instalación
`python3 setup_entorno.py`

Esto:
- Instala dependencias de sistema (ffmpeg, espeak-ng, etc.)
- Crea entorno virtual venv/
- Instala librerías necesarias (transformers, coqui-tts, faster-whisper, etc.)
- Descarga modelos MarianMT y Coqui para español
- Crea carpetas necesarias

### 🎬 Paso 3: Usa el sistema
1. Copia tus vídeos .mp4 a la carpeta videos/.
2. Ejecuta el script principal:

`python doblar_video.py` 

3. Selecciona el vídeo a doblar.
4. Espera a que el proceso termine. El vídeo doblado se guardará en final/.

### 🧪 Ver carpetas generadas

- transcript/: texto transcrito en inglés + su traducción al español
- subtitulos/: subtítulos .srt sincronizados
- audio/: audios extraídos y doblados
- final/: vídeo doblado final

### 🔧 Personalización

Puedes cambiar la voz en español editando la variable VOZ_COQUI dentro de doblar_video.py, usando una voz instalada localmente con Coqui.

### 📦 ¿Y el requirements.txt?

No lo necesitas si usas setup_entorno.py. Pero si quieres solo instalar las dependencias en un entorno ya configurado:

`pip install -r requirements.txt`

## ❤️ Créditos

    Transcripción: faster-whisper
    Traducción: MarianMT
    Voz: Coqui TTS
    Edición: moviepy

## 🧠 Autor

    Lord_Doomy — Formador Profesional.
    Contribuciones guiadas por ChatGPT y muchos errores corregidos en el camino 😄