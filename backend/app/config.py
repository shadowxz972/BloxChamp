import os
from pathlib import Path

def get_env_variable(name, optional=False):
    value = os.getenv(name)
    print(f"{name} = {value}")
    if value is None and not optional:
        raise EnvironmentError(f"La variable de entorno '{name}' no esta definida.")
    return value


ENV: str = get_env_variable("ENVIRONMENT", True) or "development"



if ENV == "development":
    import dotenv

    dotenv.load_dotenv(".env.python")
    print("cargando variables de entorno...")

ROOT_PATH = Path(__file__).parent # root del backend

port_env = get_env_variable("PORT", True)
PORT: int = int(port_env) if port_env else 5000
SECRET_KEY: str = get_env_variable("SECRET_KEY")
ALGORITHM: str = get_env_variable("ALGORITHM")
MYSQL_ROOT_PASSWORD:str = get_env_variable("MYSQL_ROOT_PASSWORD",True)
MYSQL_DATABASE:str = get_env_variable("MYSQL_DATABASE",True) or "BloxChamp"
DOMAIN:str = get_env_variable("DOMAIN",True) or f"http://localhost:{PORT}"