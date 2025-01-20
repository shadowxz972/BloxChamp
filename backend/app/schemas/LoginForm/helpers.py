import re

from ...constants import MIN_LENGTH_PASSWORD, MAX_LENGTH_PASSWORD


def validar_password(value: str) -> str:
    print(value)
    if len(value) < MIN_LENGTH_PASSWORD:
        raise ValueError(f"La contraseña debe tener al menos {MIN_LENGTH_PASSWORD} caracteres.")
    if len(value) > 255:
        raise ValueError(f"La contraseña debe ser menor que {MAX_LENGTH_PASSWORD} caracteres.")
    if not re.search(r'[A-Z]', value):
        raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r'[a-z]', value):
        raise ValueError("La contraseña debe contener al menos una letra minúscula.")
    if not re.search(r'\d', value):
        raise ValueError("La contraseña debe contener al menos un número.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValueError("La contraseña debe contener al menos un carácter especial.")
    return value
