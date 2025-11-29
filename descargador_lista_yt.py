import yt_dlp
import warnings
warnings.filterwarnings("ignore")


def buscar_youtube(query):
    if(query == ""):
        return None

    ydl_opts = {
        "default_search": "ytsearch1",   # buscar y devolver 1 resultado
        "no_warnings": True,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)

        if "entries" not in info or len(info["entries"]) == 0:
            return None
        return info["entries"][0]["webpage_url"]

def descargar_audio(url, nombre_archivo):
    ydl_opts = {
        'ffmpeg_location': r"C:\ffmpeg\ffmpeg-2025-11-27-git-61b034a47c-full_build\bin",
        "no_warnings": True,
        "format": "bestaudio/best",  # Elige el mejor audio disponible
        "outtmpl": "descargas/"+nombre_archivo,   # Nombre del archivo de salida
        "postprocessors": [
            {  
                "key": "FFmpegExtractAudio",   # Convertir a audio
                "preferredcodec": "mp3",       # Formato MP3
                "preferredquality": "192",     # Calidad (192 kbps es estándar)
            }
        ],
        "quiet": False  # Ponlo en True si no quieres que imprima nada
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def descargar_lista(nombre_archivo):  
    with open(nombre_archivo, "r") as f:
        lineas = f.readlines()
    
    nuevas_lineas = []

    for linea in lineas:
        linea_limpia = linea.strip()
        url = buscar_youtube(linea.strip())

        if(url != None):
            descargar_audio(url, linea_limpia)
            print(url)
            print(linea.strip() + "\n")
            nueva_linea = linea_limpia + " EXITO\n"
        else:
            print("ERROR")
            print(linea.strip() + "\n")
            nueva_linea = linea_limpia + " ERROR\n"
        nuevas_lineas.append(nueva_linea)
                
    with open(nombre_archivo, "w") as f:
        f.writelines(nuevas_lineas)

descargar_lista("lista_canciones.txt")