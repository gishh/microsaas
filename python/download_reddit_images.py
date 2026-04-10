import requests
from bs4 import BeautifulSoup
import os
import re

# Configuración
POST_URL = "http://www.reddit.com/r/stormkingsthunder/comments/u8j5ow/ultimate_skt_battlemaps_collection/"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
DOWNLOAD_FOLDER = "skt_battlemaps"

# Crear carpeta de descarga si no existe
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Obtener el HTML del post
response = requests.get(POST_URL, headers=HEADERS)
soup = BeautifulSoup(response.text, 'html.parser')

# Buscar todos los enlaces en el post
links = []
for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    # Filtrar enlaces de imágenes comunes (Imgur, Google Drive, etc.)
    if any(ext in href.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', 'imgur', 'drive.google', 'dropbox']):
        links.append(href)

# Función para descargar imágenes
def download_image(url, filename):
    try:
        if 'imgur.com' in url and not any(url.endswith(ext) for ext in ['.jpg', '.png', '.jpeg']):
            url += '.jpg'  # Intenta forzar extensión en Imgur
        
        response = requests.get(url, headers=HEADERS, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"✅ Descargado: {filename}")
        else:
            print(f"❌ Error al descargar {url} (Código: {response.status_code})")
    except Exception as e:
        print(f"❌ Error en {url}: {str(e)}")

# Descargar cada imagen
for i, url in enumerate(links):
    # Extraer nombre del archivo de la URL o generar uno
    filename = os.path.join(DOWNLOAD_FOLDER, f"map_{i+1}.jpg")
    download_image(url, filename)

print("🎉 ¡Descarga completada! Revisa la carpeta:", DOWNLOAD_FOLDER)