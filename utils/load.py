from sqlalchemy import create_engine
import pandas as pd
# import gspread
import os
import logging
from dotenv import load_dotenv

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

load_dotenv()

def load_to_postgresql(df, table_name='product'):
    try:
        username = os.getenv('DB_USER')
        password = os.getenv('DB_PASS')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        database = os.getenv('DB_NAME')
        
        required_vars = {
            'DB_USER': username,
            'DB_PASS': password,
            'DB_HOST': host,
            'DB_PORT': port,
            'DB_NAME': database
        }

        missing_vars = [var for var, value in required_vars.items() if value is None or value == '']
        if missing_vars: raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")
        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke PostgreSQL table '{table_name}'.")

    except Exception as e:
        print(f"Gagal menyimpan ke PostgreSQL: {e}")

def load_to_csv(df, filename="fashion_products.csv"):
    df.to_csv(filename, index=False)

def load_to_google_sheets(df):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    try:
        creds = Credentials.from_service_account_file(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'), scopes=SCOPES)

        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        sheet.values().clear(
            spreadsheetId=os.getenv('GOOGLE_SHEET_ID'),
            range='Sheet1'
        ).execute()

        data = [df.columns.tolist()] + df.values.tolist()

        sheet.values().update(
            spreadsheetId=os.getenv('GOOGLE_SHEET_ID'),
            range='Sheet1!A1',
            valueInputOption='RAW',
            body={'values': data}
        ).execute()

        logging.info("✅ Data berhasil disimpan ke Google Sheets.")
        print("✅ Data berhasil disimpan ke Google Sheets.")

    except Exception as e:
        logging.error(f"❌ Gagal menyimpan ke Google Sheets: {e}")
        print(f"❌ Gagal menyimpan ke Google Sheets: {e}")
