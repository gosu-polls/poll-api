import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import os
import pandas as pd

class GoogleSheet:
    _conn = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(__class__, cls).__new__(cls)
            scopes = ['https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/drive']

            keyfile_dict = {"type": "service_account",
                            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                            "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
                            "private_key": os.getenv("GOOGLE_PRIVATE_KEY"),
                            "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
                            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                            "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL")
                        }

            credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, 
                                                                       scopes=scopes)

            
            cls._conn = gspread.authorize(credentials) 
        return cls._instance
    
    @classmethod
    # def ReadData(cls, db_name: str, table_name: str = 'Sheet1', filters: dict = {}) -> pd.DataFrame:
    # def ReadData(cls, data: dict = {}) -> pd.DataFrame:
    def ReadData(cls, identifier: dict = {}, filters: dict = {}) -> pd.DataFrame:

        try:
            spreadsheet = cls._conn.open_by_key(identifier['db_name'])
            # spreadsheet = cls._conn.open_by_key(data['db_name'])
            worksheet = spreadsheet.worksheet(identifier['table_name'] if 'table_name' in identifier else 'Sheet1')
            # worksheet = spreadsheet.worksheet(data['table_name'] if 'table_name' in data else 'Sheet1')
            df = pd.DataFrame(worksheet.get_all_records())
            filters = identifier['filters'] if 'filters' in identifier else {}
            # filters = data['filters'] if 'filters' in data else {}
            for key in filters:
                if key in df.columns:
                    df = df[df[key] == filters[key]]
            return df
        except:
            raise


    
    @classmethod
    def WriteData(cls, identifier: dict = {}, data = pd.DataFrame):
        try:
            spreadsheet = cls._conn.open_by_key(identifier['db_name'])
            worksheet = spreadsheet.worksheet(identifier['table_name'] if 'table_name' in identifier else 'Sheet1')
            worksheet.clear()
            set_with_dataframe(worksheet=worksheet, 
                               dataframe=data, 
                               include_index=False,
                               include_column_header=True, 
                               resize=True)
        except Exception as err:
            print(err)
            raise
