import os
import base64
import hashlib
from typing import Any

SECRET_KEY = os.environ.get("APP_SECRET_KEY", "gigbid-production-secure-key-2026")

def encrypt_token(plain_token: str) -> str:
    """Symmetric XOR-based token obfuscation/encryption using secret key."""
    if not plain_token:
        return ""
    key_bytes = hashlib.sha256(SECRET_KEY.encode()).digest()
    token_bytes = plain_token.encode()
    encrypted = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(token_bytes)])
    return base64.b64encode(encrypted).decode()

def decrypt_token(encrypted_token: str) -> str:
    """Decrypts token stored in user vault."""
    if not encrypted_token:
        return ""
    try:
        key_bytes = hashlib.sha256(SECRET_KEY.encode()).digest()
        cipher_bytes = base64.b64decode(encrypted_token.encode())
        decrypted = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(cipher_bytes)])
        return decrypted.decode()
    except Exception:
        return ""

class UserStore:
    def __init__(self):
        self.users: dict[str, dict[str, Any]] = {
            "reviewer": {
                "username": "reviewer",
                "persona_id": "ai_engineer",
                "display_name": "Reviewer Account (Alex Rivera Persona)",
                "hourly_rate_usd": 65.0,
                "min_project_budget_usd": 400.0,
                "weekly_connects_budget": 80,
                "connected_marketplace": "gigsim",
                "autonomy_level": "semi-autonomous",
                "encrypted_token": encrypt_token("seed-reviewer-token")
            }
        }

    def get_user(self, username: str) -> dict[str, Any] | None:
        return self.users.get(username)

    def set_user(self, username: str, data: dict[str, Any]):
        self.users[username] = data

user_store = UserStore()
