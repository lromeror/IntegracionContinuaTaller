import pytest
import os
import json
from src.books import register_book, DB_FILE

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Limpia el archivo de base de datos antes y después de cada prueba."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    yield
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

def test_register_book_success():
    """Prueba que un libro se registre correctamente."""
    result = register_book("El Aleph", "B001")
    assert "registrado exitosamente" in result
    
    # Verificar que se guardó en el JSON
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    assert len(data["books"]) == 1
    assert data["books"][0]["title"] == "El Aleph"
    assert data["books"][0]["code"] == "B001"

def test_register_book_duplicate_code():
    """Prueba que no se permita registrar dos libros con el mismo código."""
    # Registrar el primer libro
    register_book("El Aleph", "B001")
    
    # Intentar registrar otro libro con el mismo código debe lanzar ValueError
    with pytest.raises(ValueError) as excinfo:
        register_book("Ficciones", "B001")
        
    assert "ya está registrado" in str(excinfo.value)