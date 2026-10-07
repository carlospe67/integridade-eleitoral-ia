"""Autenticacao Google para BigQuery e Google Drive."""
import json
import os
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.cloud import bigquery
from google.cloud import storage

SCOPES = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/devstorage.read_write",
]

TOKEN_FILE = Path(os.environ.get("HOME", "~")) / ".google_token.json"

def authenticate():
    """Authenticate using saved credentials or interactive flow."""
    creds = None
    
    if TOKEN_FILE.exists():
        print("Encontrando token salvo anterior...")
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Renovando credenciais expiradas...")
            creds.refresh(Request())
        else:
            print("\n" + "=" * 60)
            print("AUTENTICACAO GOOGLE - NECESSARIA")
            print("=" * 60)
            print("\nPara autenticar, siga os passos abaixo:")
            print("1. Vá para: https://console.cloud.google.com/apis/credentials")
            print("2. Crie um OAuth 2.0 Client ID (Tipo: Aplicativo de desktop)")
            print("3. Copie o Client ID e Client Secret")
            print("4. Cole abaixo:")
            
            client_id = input("\nClient ID: ").strip()
            client_secret = input("Client Secret: ").strip()
            
            from google_auth_oauthlib.flow import Flow
            
            client_config = {
                "installed": {
                    "client_id": client_id,
                    "project_id": "ai-course-project",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": client_secret,
                    "redirect_uris": ["http://localhost"]
                }
            }
            
            flow = Flow.from_client_config(
                client_config,
                scopes=SCOPES,
                redirect_uri="http://localhost"
            )
            
            auth_url, _ = flow.authorization_url(
                access_type="offline",
                include_granted_scopes="true",
                prompt="consent",
                login_hint="carlosp@id.uff.br"
            )
            
            print(f"\n1. Abra este URL no navegador:")
            print(f"\n   {auth_url}\n")
            print("2. Faça login com carlosp@id.uff.br")
            print("3. Autorize o acesso")
            print("4. Cole o codigo de autorizacao:")
            
            code = input("\nCodigo: ").strip()
            flow.fetch_token(code=code)
            creds = flow.credentials
        
        # Save credentials for future use
        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print(f"\nCredenciais salvas em: {TOKEN_FILE}")
    
    return creds

def test_bigquery(creds):
    """Test BigQuery connection with a simple query."""
    try:
        client = bigquery.Client(credentials=creds)
        print(f"\nBigQuery conectado com projeto: {client.project}")
        
        # Test simple query
        query = """
        SELECT 
          ano,
          COUNT(*) as total_rows
        FROM `basedosdados.br_tse_eleicoes.resultados_candidato_secao`
        WHERE ano = 2022
          AND sigla_uf = 'RJ'
        GROUP BY ano
        LIMIT 1
        """
        
        print("\nTestando consulta ao BigQuery...")
        query_job = client.query(query)
        results = query_job.result()
        for row in results:
            print(f"  Ano: {row.ano}, Total de linhas: {row.total_rows}")
        
        return True
    except Exception as e:
        print(f"\nErro ao testar BigQuery: {e}")
        return False

def test_drive(creds):
    """Test Google Drive connection."""
    try:
        storage_client = storage.Client(credentials=creds)
        buckets = list(storage_client.list_buckets(max_results=1))
        print(f"\nDrive/GCS conectado. Buckets encontrados: {len(buckets)}")
        return True
    except Exception as e:
        print(f"\nErro ao testar Drive: {e}")
        return False

if __name__ == "__main__":
    try:
        creds = authenticate()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(TOKEN_FILE)
        
        print("\n" + "=" * 60)
        print("TESTANDO CONEXOES")
        print("=" * 60)
        
        bq_ok = test_bigquery(creds)
        drive_ok = test_drive(creds)
        
        if bq_ok and drive_ok:
            print("\nAUTENTICACAO CONCLUIDA COM SUCESSO!")
        else:
            print("\nAutenticacao parcial - verifique as permissões.")
            sys.exit(1)
    except Exception as e:
        print(f"\nErro durante a autenticacao: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)