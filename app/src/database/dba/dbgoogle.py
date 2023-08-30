import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import os
from os import environ as env
import pandas as pd

class GoogleSheet:
    _conn = None
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(__class__, cls).__new__(cls)
            scopes = ['https://www.googleapis.com/auth/spreadsheets',
                      'https://www.googleapis.com/auth/drive']

            # private_key = os.getenv("GOOGLE_PRIVATE_KEY")
            # private_key = private_key.replace("||", "\n")
            # print(f'The replaced ones is {private_key}')
            # print(f'{os.getenv("GOOGLE_PRIVATE_KEY")}')
            # print(f'{env["GOOGLE_PRIVATE_KEY"]}')
            keyfile_dict = {"type": "service_account",
                            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
                            "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID"),
                            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCeSW2QBrZolii2\n7hcW0U9AoNYE2SaPpWdIZBePTxkOo5bfMQjvwnmiWwP4bxD4uV+o/Rdx44Cci1Jw\n5YZtNqolslMQ9vtf96425RWojgXhl779vPUW/HmyTo9I471XA0tFa5A00cZs2KA0\n5COEoe+8qGqlIB6moSvDzyMwmGrWJrPm4rv4NaLudawClTMhH3UEwliN+ATvtq3e\nkOwNQyJ1hP0d9eT4+u1fkNOvmestaXRN1NQbicc/vQmGgDkIrgyjzrWnHk6JY/Wd\n0Zt2/tBK6zAci7bSPXSa1XeofYchf/JM/N/zJFBm/qQqiLsE9RVWrzhy6Roq2xe1\nUkTJWYcVAgMBAAECgf44P8UQ8GcRprgbIynxM5eN0rspsTB/hmc9ZvZPBjTwTcD7\nxTfw9B+WuYbnQVC+g3SL2O7OKIXfECDEwJqiLlTQuJEUafnsWLE+co4yJlSymvtc\nry6CQjt/ARln6M7aYeREX/7fXIPR1rU3pczZ1J9bVE2WRLZ4efwzA5AyT/x+SwSe\nluxrnEZCa6fUDPskjMP389Dk6CwOekk1LGjqqKzdjfUaDjOYAWMagN4+bbzvy0w1\n5S33Ov/L8b/6umXRC0zsNlWXKDAL/39v2t5IrC2mUeYspJCZk9aljIV5x4qQOgaG\n1WYJlmxVkh+GNeXn9X2t3B1Q7kkAkRLFeFr1AQKBgQDNkzDwiJEj26M6ziBScX7j\nB/28nP8MOD4nhd/ZjwcKIGMEnzbGY6Eli/i2t4WJwvZyriW1BN6AWT01N1ck6Lu/\n8RjcQPXGEdmi3K/TMclZGJNzCG+mLtuy0YUoYVLnNmHTAFmvt91aG9/B54fb8bia\n+81wiOpFp3+fASbViQqJIQKBgQDFHNcwg4RXphde88WG3+aH1BzV8p1ILO5fANS1\nYmapbK91nasdNnm5UXYgy5O6lAVSNQdn6K5mipUYwjVcM16ZMTNkWQ3SJrv7gFvN\n/H1ztfukfFCsa6WKets5TVTk0+UWsTdIz0gcs3BhtgkfootLeby9Lepy3Wo8TGIt\nZOZ7dQKBgQChrppXE5HTefMvVN7m+IyrUqWlqnSNz85Sl2AvY+ZNeJtoDzCtZ75e\nIXBDhKNqbgQWvhC6BlJY79bL+/J1/PVtSNocoJqsZW2eQaOnnwiVIlcVqhTlxwTT\n5yWrVKA3aPYXVbc0FI/rRvD9OHQJ8FsYyeISGBzpG4usKuO4HkhDAQKBgHbTkBY6\n8ok0I1qmcimAyKSRhmCjxZVBIOI8yf4et+zjDFNHHWSa9n51UVUr5H7RxPNt7G0D\npD9Ew+UNDsXqYdjQBD82QFKz7xcKpk1jLO2Yg38BQlDvA/ibX5UHvWnFI5Gue7l0\n2/ARbGo7JvzfLEHvvYv+Jhvgxq5bDcR300oRAoGBAJPIYTAZfSA506XnoWxz1FeU\nKMSL0izaWaztLhwcWEA+2rIN0yOYognZ0dlcjpH1S2UO+qCcX87m18MBa/JdZ4fn\nhRxeNNX8+T6ftdyDRG96SGE4GG8ltAqoT3lTpAH2urcsrBpUAqOMYUEpyXzWyjx6\n3I+YHyl2EuajYCDAGSDl\n-----END PRIVATE KEY-----\n",
                            "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
                            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                            "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_X509_CERT_URL")
                        }
            # for k in keyfile_dict:
            #     print(f'{k} -> {keyfile_dict[k]}')
            credentials = None
            try:
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, 
                                                                       scopes=scopes)
            except Exception as err:
                print(f'Erorr while running ServiceAccountCredentials.from_json_keyfile_dict {str(err)}')
            
            print(f'The credentials are {credentials}')
            try:
                cls._conn = gspread.authorize(credentials) 
            except Exception as err:
                print(f'Erorr while running gspread.authorize {str(err)}')
        return cls._instance
    
    @classmethod
    # def ReadData(cls, db_name: str, table_name: str = 'Sheet1', filters: dict = {}) -> pd.DataFrame:
    # def ReadData(cls, data: dict = {}) -> pd.DataFrame:
    def ReadData(cls, identifier: dict = {}, filters: dict = {}) -> pd.DataFrame:

        try:
            spreadsheet = None
            try:
                spreadsheet = cls._conn.open_by_key(identifier['db_name'])
            except Exception as err:
                print(f'Error while cls._conn.open_by_key is performed {str(err)}')

            worksheet = None
            try:
                worksheet = spreadsheet.worksheet(identifier['table_name'] if 'table_name' in identifier else 'Sheet1')
            except Exception as err:
                print(f'Error while spreadsheet.worksheet is performed {str(err)}')
                
            df = pd.DataFrame(worksheet.get_all_records())
            for key in filters:
                if key in df.columns:
                    df = df[df[key] == filters[key]]
            return df
        except Exception as err:
            print(f'Error while ReadData is performed {str(err)}')
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
