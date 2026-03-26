import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone
import jwt

import os
from dotenv import load_dotenv


load_dotenv()

access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
secret_key = os.getenv("SECRET_KEY")
algo = os.getenv("ALGORITHM", "HS256")



def hash_password(password: str) -> str:
    """
    Hash un mot de passe avec PBKDF2-HMAC-SHA256.

    Format stocké :
        pbkdf2_sha256$iterations$salt$hash
    """
    iterations = 100000
    salt = os.urandom(16).hex()

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    ).hex()

    return f"pbkdf2_sha256${iterations}${salt}${password_hash}"


def verify_password(password: str, stored_value: str) -> bool:
    """
    Vérifie qu'un mot de passe correspond bien au hash stocké.
    """
    try:
        algorithm_name, iterations_str, salt, stored_hash = stored_value.split("$")
        if algorithm_name != "pbkdf2_sha256":
            return False

        computed_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            int(iterations_str),
        ).hex()

        return hmac.compare_digest(computed_hash, stored_hash)
    except (ValueError, AttributeError):
        return False



def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Crée un vrai JWT signé.

    On copie le dictionnaire reçu puis on ajoute une date d'expiration.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=access_token_expire_minutes)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algo)


def decode_access_token(token: str) -> dict:
    """
    Décode et vérifie un JWT.

    Si la signature est invalide ou si le token est expiré, PyJWT lèvera une
    exception que le code appelant pourra gérer.
    """
    return jwt.decode(token, secret_key, algorithms=[algo])