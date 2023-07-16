import os

class Env:
    def get_env(self) -> dict:
        keyfile_dict = {"type": "service_account",
                "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
                "private_key": os.getenv("GOOGLE_PRIVATE_KEY").replace("\\\\", "\\"),
                "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL")
            }
        return keyfile_dict
    
    def get_settings(self) -> dict:
        cosmos_dict = {
                        'host': os.environ.get('ACCOUNT_HOST', 'https://defaultcosmosdb.documents.azure.com:443/'),
                        'master_key': os.environ.get('ACCOUNT_KEY', 'ZJWCbBprAcwlEer977iHGPL8R3zB0AmVxI2SMkT5lxyPu87cUYj92VoICKQ4cLE93qzdRchUP20bACDbdQ4Pkw=='),
                        'polls_database_id': os.environ.get('COSMOS_DATABASE', 'polls-db'),
                        'cwc_container_id': os.environ.get('COSMOS_CONTAINER', 'cwc'),
                      }
        return cosmos_dict
    