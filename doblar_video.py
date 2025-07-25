import os
import subprocess
import asyncio
from faster_whisper import WhisperModel
from transformers import MarianMTModel, MarianTokenizer
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from TTS.api import TTS

# === Configuración ===
CARPETA_VIDEOS = "videos"
CARPETA_AUDIO = "audio"
CARPETA_SUBTITULOS = "subtitulos"
CARPETA_SALIDA = "salida"
IDIOMA_FUENTE = "en"
IDIOMA_DESTINO = "es"
MODEL_NAME = "Helsinki-NLP/opus-mt-en-es"

# === Preparación de carpetas ===
for carpeta in [CARPETA_AUDIO, CARPETA_SUBTITULOS, CARPETA_SALIDA]:
    os.makedirs(carpeta, exist_ok=True)

# === Traducción ===
print("Cargando modelo de traducción MarianMT...")
tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)
model = MarianMTModel.from_pretrained(MODEL_NAME, local_files_only=True)

def traducir_texto(texto):
    inputs = tokenizer([texto], return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# === Transcripción ===
print("Cargando modelo de transcripción Faster-Whisper...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribir_audio(ruta_audio):
    segments, _ = whisper_model.transcribe(ruta_audio, beam_size=5)
    resultados = []
    for segment in segments:
        resultados.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })
    return resultados

# === Síntesis de voz con Coqui TTS ===
print("Cargando modelo de TTS Coqui...")
tts = TTS(model_name="tts_models/es/mai/tacotron2-DDC", progress_bar=False, gpu=False)

async def sintetizar_segmentos(segmentos, ruta_audio_salida):
    partes = []
    for i, seg in enumerate(segmentos):
        texto = seg["text"]
        print(f"🔊 Sintetizando: {texto}")
        temp_wav = f"temp_segment_{i}.wav"
        tts.tts_to_file(text=texto, file_path=temp_wav)
        partes.append(AudioSegment.from_wav(temp_wav))
        os.remove(temp_wav)
    combinado = sum(partes)
    combinado.export(ruta_audio_salida, format="wav")

# === Flujo principal ===
def main():
    videos = sorted([f for f in os.listdir(CARPETA_VIDEOS) if f.endswith(".mp4")])
    if not videos:
        print("No se encontraron videos.")
        return

    print("=== Selecciona un archivo de video ===")
    for i, video in enumerate(videos):
        print(f"{i + 1}. {video}")
    idx = int(input("Número de archivo: ")) - 1
    video_path = os.path.join(CARPETA_VIDEOS, videos[idx])
    nombre_base = os.path.splitext(os.path.basename(video_path))[0]

    # Extraer audio
    audio_path = os.path.join(CARPETA_AUDIO, f"{nombre_base}.mp3")
    print("🎬 Extrayendo audio...")
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    # Transcribir
    print("📝 Transcribiendo...")
    segmentos = transcribir_audio(audio_path)

    # Traducir
    print("🌐 Traduciendo...")
    for s in segmentos:
        s["text"] = traducir_texto(s["text"])

    # Guardar subtítulos traducidos (opcional)
    srt_path = os.path.join(CARPETA_SUBTITULOS, f"{nombre_base}.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, s in enumerate(segmentos):
            f.write(f"{i+1}\n")
            f.write(f"{formatear_tiempo(s['start'])} --> {formatear_tiempo(s['end'])}\n")
            f.write(f"{s['text']}\n\n")
    print(f"📄 Subtítulos guardados en: {srt_path}")

    # Sintetizar nuevo audio
    ruta_audio_doblado = os.path.join(CARPETA_AUDIO, f"{nombre_base}_es.wav")
    asyncio.run(sintetizar_segmentos(segmentos, ruta_audio_doblado))

    # Reemplazar audio en el video original
    salida_final = os.path.join(CARPETA_SALIDA, f"{nombre_base}_doblado.mp4")
    print("🎥 Combinando video con audio doblado...")
    comando = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", ruta_audio_doblado,
        "-c:v", "copy",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",
        salida_final
    ]
    subprocess.run(comando)
    print(f"✅ Video doblado guardado como: {salida_final}")

def formatear_tiempo(segundos):
    h = int(segundos // 3600)
    m = int((segundos % 3600) // 60)
    s = int(segundos % 60)
    ms = int((segundos - int(segundos)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

if __name__ == "__main__":
    main()
