"""Gera URL de autenticacao Google para ser usado manualmente."""
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/devstorage.read_write",
]

AUTH_URL = "https://accounts.google.com/o/oauth2/auth"

def generate_auth_url():
    """Generate OAuth authorization URL."""
    params = {
        "client_id": "YOUR_CLIENT_ID_HERE",  # Will be replaced
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "login_hint": "carlosp@id.uff.br",
    }
    
    url = f"{AUTH_URL}?{urlencode(params)}"
    
    # Save to file
    auth_file = Path(__file__).parent / "auth_url.txt"
    auth_file.write_text(url, encoding="utf-8")
    
    print(f"URL de autenticacao salva em: {auth_file}")
    print(f"\nAbra este URL no navegador:")
    print(f"\n{url}\n")
    print("Faça login com carlosp@id.uff.br e autorize o acesso.")
    print("Depois, cole o codigo de autorizacao no proximo passo.")

if __name__ == "__main__":
    generate_auth_url()