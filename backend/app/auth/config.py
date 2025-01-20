from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# Instancia para manejar el hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema para extraer el token desde el cliente
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

