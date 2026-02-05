# File: backend/app/services/jdi/encryption.py
# Fernet encryption/decryption for OAuth tokens at rest
import os
import logging
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

# Load encryption key from environment at call time (after load_dotenv has run)
# Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"


def _get_fernet() -> Fernet:
    """Return a Fernet instance. Raises if key is not configured."""
    key = os.getenv("JDI_ENCRYPTION_KEY")
    if not key:
        raise RuntimeError(
            "JDI_ENCRYPTION_KEY environment variable is not set. "
            "Generate one with: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
        )
    return Fernet(key.encode())


def encrypt_token(plaintext: str) -> str:
    """Encrypt a token string and return the ciphertext as a UTF-8 string."""
    f = _get_fernet()
    return f.encrypt(plaintext.encode()).decode()


def decrypt_token(ciphertext: str) -> str:
    """Decrypt a ciphertext string and return the plaintext."""
    f = _get_fernet()
    return f.decrypt(ciphertext.encode()).decode()
