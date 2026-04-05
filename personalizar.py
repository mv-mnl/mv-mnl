import xml.etree.ElementTree as ET
import sys
import os
import requests
from io import BytesIO
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

try:
    from PIL import Image
except ImportError:
    print("Falta instalar Pillow. Ejecuta: venv/bin/pip install Pillow")
    sys.exit(1)

# Configuración leida desde el archivo .env o valores por defecto
USER_CONFIG = {
    "GITHUB_USER": os.getenv("USER_NAME", "mv-mnl"),
    "NAME_HEADER": os.getenv("NAME_HEADER", "manuel@mv-mnl"),
    "OS": os.getenv("OS", "Arch Linux (Hyprland)"),
    "HOST": os.getenv("HOST", "Custom Build"),
    "KERNEL": os.getenv("KERNEL", "Linux"),
    "IDE": os.getenv("IDE", "Neovim, VSCode"),
    "LANG_PROG": os.getenv("LANG_PROG", "Python, Bash, JS, C++"),
    "LANG_COMP": os.getenv("LANG_COMP", "HTML, CSS, JSON"),
    "LANG_REAL": os.getenv("LANG_REAL", "Spanish, English"),
    "HOBBY_SW": os.getenv("HOBBY_SW", "Tiling WMs, Dotfiles, Scripting"),
    "HOBBY_HW": os.getenv("HOBBY_HW", "PC Building"),
    "HOBBY_OTH": os.getenv("HOBBY_OTH", "Music, Gaming"),
    "EMAIL_PERS": os.getenv("EMAIL_PERS", "manuel@example.com"),
    "EMAIL_WORK": os.getenv("EMAIL_WORK", "manuel.work@example.com"),
    "INSTA": os.getenv("INSTA", "mv.mnl"),
    "DISCORD": os.getenv("DISCORD", "mv-mnl")
}

def get_github_avatar_ascii(username, width=39, height=25):
    """Descarga el avatar de Github y lo convierte a arte ASCII"""
    print(f"Descargando foto de perfil de GitHub para {username}...")
    try:
        req = requests.get(f"https://api.github.com/users/{username}")
        req.raise_for_status()
        avatar_url = req.json().get("avatar_url")
        
        req_img = requests.get(avatar_url)
        img = Image.open(BytesIO(req_img.content)).convert("L") # L = escala de grises
        
        # Redimensionar (el ancho debe ser mayor que el alto porque los caracteres en terminal no son cuadrados)
        img = img.resize((width, height))
        
        pixels = img.getdata()
        
        # Caracteres de oscuro a claro (invertido para modo oscuro)
        ascii_chars = "@%#*+=-:. "
        
        new_pixels = [ascii_chars[pixel // 26] for pixel in pixels]
        new_pixels_count = len(new_pixels)
        
        ascii_image = ["".join(new_pixels[index:(index+width)]) for index in range(0, new_pixels_count, width)]
        return ascii_image
    except Exception as e:
        print(f"No se pudo descargar o convertir el avatar: {e}")
        return None

def replace_text_in_line(root, search_str, replace_str):
    for element in root.iter():
        if element.tag.endswith('tspan') and element.text and search_str in element.text:
            element.text = replace_str

def update_svg(in_filename, out_filename, ascii_lines):
    print(f"Actualizando {out_filename}... a partir de {in_filename} con configuraciones de tu .env")
    try:
        ET.register_namespace('', "http://www.w3.org/2000/svg")
        tree = ET.parse(in_filename)
        root = tree.getroot()

        replace_text_in_line(root, "viktor@serhiienko", USER_CONFIG["NAME_HEADER"])
        replace_text_in_line(root, "Linux (Pop!_OS 22.04 LTS)", USER_CONFIG["OS"])
        replace_text_in_line(root, "None, Inc.", USER_CONFIG["HOST"])
        replace_text_in_line(root, "Student (Paul Cornu High School) Operator", USER_CONFIG["KERNEL"])
        replace_text_in_line(root, "VIM 8.2.2121, VSCode 1.114.0", USER_CONFIG["IDE"])
        replace_text_in_line(root, "Rust, Python, NextJS, C++", USER_CONFIG["LANG_PROG"])
        replace_text_in_line(root, "HTML, CSS, JSON, LaTeX", USER_CONFIG["LANG_COMP"])
        replace_text_in_line(root, "English, French, Russian, German", USER_CONFIG["LANG_REAL"])
        replace_text_in_line(root, "Programming Projects, Learning ML", USER_CONFIG["HOBBY_SW"])
        replace_text_in_line(root, "Embedded Systems, Arduino Projects", USER_CONFIG["HOBBY_HW"])
        replace_text_in_line(root, "Loving learning Maths, Physics ect..", USER_CONFIG["HOBBY_OTH"])
        replace_text_in_line(root, "viktorserhiienko12@gmail.com", USER_CONFIG["EMAIL_PERS"])
        replace_text_in_line(root, "viktorsrhk@gmail.com", USER_CONFIG["EMAIL_WORK"])
        replace_text_in_line(root, "viktor_srhk", USER_CONFIG["INSTA"])
        
        # Insertar foto ASCII
        if ascii_lines:
            for text in root.findall(".//{http://www.w3.org/2000/svg}text"):
                if text.get("class") == "ascii":
                    # Limpiar las lineas viejas
                    for child in list(text):
                        text.remove(child)
                    
                    # Agregar las nuevas lineas convertidas dinámicamente
                    # El diseño original empezaba en y=30 y subía en 20 para cada linea
                    start_y = 30
                    for line in ascii_lines:
                        tspan = ET.Element("tspan", {"x": "15", "y": str(start_y)})
                        tspan.text = line
                        text.append(tspan)
                        start_y += 20

        tree.write(out_filename, encoding="utf-8", xml_declaration=True)
        print(f"¡{out_filename} actualizado con éxito!")
    except Exception as e:
        print(f"Error procesando {in_filename}: {e}")

if __name__ == "__main__":
    print("Script de personalización de plantilla usando variables .env")
    ascii_art = get_github_avatar_ascii(USER_CONFIG["GITHUB_USER"])
    
    update_svg("template_dark.svg", "dark_mode.svg", ascii_art)
    update_svg("template_light.svg", "light_mode.svg", ascii_art)
