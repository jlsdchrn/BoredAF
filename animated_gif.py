from PIL import Image, ImageSequence
import requests
from bs4 import BeautifulSoup
import os
import shutil

def get_terminal_size():
    """Récupère les dimensions du terminal."""
    size = shutil.get_terminal_size()
    return size.columns, size.lines

def resize_frame(frame, max_width, max_height):
    """Redimensionne le frame tout en gardant le ratio."""
    original_width, original_height = frame.size
    aspect_ratio = original_width / original_height
    
    # Redimensionner en fonction des contraintes
    if original_width > max_width or original_height > max_height:
        if max_width / aspect_ratio <= max_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
    else:
        new_width, new_height = original_width, original_height

    return frame.resize((new_width, new_height))

import requests
import os

def download_gif(url, save_path="temp.gif"):
    """Télécharge directement un GIF depuis une URL."""
    current_folder = os.path.dirname(os.path.abspath(__file__))
    full_save_path = os.path.join(current_folder, save_path)

    # Si le fichier existe déjà, le réutiliser
    if os.path.exists(full_save_path):
        return full_save_path

    # Télécharger le fichier directement
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(full_save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"GIF téléchargé avec succès : {full_save_path}")
    return full_save_path


#def download_gif(url, save_path="temp.gif"):
    """Download a gif from an url."""
    current_folder = os.path.dirname(os.path.abspath(__file__))
    full_save_path = os.path.join(current_folder, save_path)
    response = requests.get(url, stream=True)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check if the GIF already exists
    if os.path.exists(full_save_path):
        return full_save_path
    
    # Find the direct GIF link
    gif_tag = soup.find("meta", property="og:image")
    if gif_tag:
        gif_url = gif_tag["content"]
        # Download the GIF
        gif_response = requests.get(gif_url)
        # Ensure the GIF request was successful
        gif_response.raise_for_status()  
        print(save_path)
        # Save the GIF locally
        with open(save_path, "wb") as file:
            file.write(gif_response.content)
        
        print("GIF downloaded successfully as 'among_us_twerk.gif'")
    else:
        print("Could not find the GIF link on the page.")
    if response.status_code == 200:
        with open(full_save_path, "wb") as f:
            f.write(response.content)
        return full_save_path
    else:
        raise Exception(f"Erreur lors du téléchargement : {response.status_code}")

#def extract_gif_frames(gif_path,file_name):
    """Extrait les frames d'un GIF et les convertit en ASCII."""
    frames = []
    max_width,max_height = get_terminal_size()
    with Image.open(gif_path) as gif:
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("L")  # Niveaux de gris
            frame = resize_frame(frame, max_width, max_height//2)
            #frame = frame.resize((max_width, int(max_width * frame.height / frame.width)))
            frame_data = list(frame.getdata())  # Convert to list
            ascii_frame = "\n".join(
                "".join(" " if pixel > 128 else "#" for pixel in frame_data[i:i + frame.width])
                for i in range(0, len(frame_data), frame.width)
            )
            frames.append(ascii_frame)
    with open(file_name, "w") as f:
        f.write("\n\n".join(frames))
    os.remove(gif_path) 
    return 
def extract_gif_frames(gif_path, file_name):
    """Extrait les frames d'un GIF et les convertit en ASCII avec une palette de caractères."""
    # Palette de caractères ASCII pour différentes intensités
    ascii_chars = ["@@", "##", "88", "&&", "%%", "$$", "**", "++", "==", "--", "::", "..", "  "]
    
    # for dark mode shell
    ascii_chars.reverse()
    
    frames = []
    max_width, max_height = get_terminal_size()
    
    with Image.open(gif_path) as gif:
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("L")  # Convertir en niveaux de gris
            frame = resize_frame(frame, max_width, int(max_height*0.6))
            frame_data = list(frame.getdata())  # Convertir en liste
            
            # Convertir chaque pixel en un caractère basé sur sa luminosité
            ascii_frame = "\n".join(
                "".join(ascii_chars[pixel * (len(ascii_chars) - 1) // 255] for pixel in frame_data[i:i + frame.width])
                for i in range(0, len(frame_data), frame.width)
            )
            frames.append(ascii_frame)
    
    with open(file_name, "w") as f:
        f.write("\n\n".join(frames))
    
    os.remove(gif_path)  # Supprimer le fichier GIF après l'extraction
    return

def extract_frames_from_file(filename):
    frames = []
    with open(filename,"r") as f:
        frames = f.read().split("\n\n")
    return frames
    