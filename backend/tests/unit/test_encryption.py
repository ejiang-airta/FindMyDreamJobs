# File: backend/tests/unit/test_encryption.py
# Tests for Fernet encryption/decryption of OAuth tokens
import pytest
from app.services.jdi.encryption import encrypt_token, decrypt_token


class TestEncryption:
    """Tests for token encryption and decryption."""

    def test_encrypt_decrypt_roundtrip(self):
        plaintext = "my-secret-refresh-token-12345"
        ciphertext = encrypt_token(plaintext)
        decrypted = decrypt_token(ciphertext)
        assert decrypted == plaintext

    def test_ciphertext_differs_from_plaintext(self):
        plaintext = "my-token"
        ciphertext = encrypt_token(plaintext)
        assert ciphertext != plaintext

    def test_different_plaintexts_different_ciphertexts(self):
        ct1 = encrypt_token("token-1")
        ct2 = encrypt_token("token-2")
        assert ct1 != ct2

    def test_empty_string_roundtrip(self):
        ciphertext = encrypt_token("")
        assert decrypt_token(ciphertext) == ""

    def test_unicode_roundtrip(self):
        plaintext = "token-with-unicode-\u00e9\u00e8"
        ciphertext = encrypt_token(plaintext)
        assert decrypt_token(ciphertext) == plaintext

    def test_long_token_roundtrip(self):
        plaintext = "x" * 5000
        ciphertext = encrypt_token(plaintext)
        assert decrypt_token(ciphertext) == plaintext
