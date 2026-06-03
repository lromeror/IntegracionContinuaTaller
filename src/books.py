import json
import os

DB_FILE = "library_db.json"

def init_db():
    """Asegura que el archivo JSON exista con una estructura inicial."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"books": [], "members": [], "loans": []}, f, indent=4)

def register_book(title, code):
    """Registra un libro en el catálogo con un título y un código único."""
    init_db()
    
    # 1. Leer los datos actuales
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    
    # 2. Validar que el código sea único (Regla del PDF)
    for book in data["books"]:
        if book["code"] == code:
            raise ValueError(f"Error: El código de libro '{code}' ya está registrado.")
    
    # 3. Crear el nuevo objeto libro y agregarlo
    new_book = {
        "title": title,
        "code": code
    }
    data["books"].append(new_book)
    
    # 4. Guardar los cambios de vuelta en el JSON
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
    return f"Libro '{title}' registrado exitosamente con el código {code}."