import pandas as pd
import numpy as np
import logging
from datetime import datetime
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


def transform_df(products):
    """Menggabungkan semua transformasi data menjadi satu fungsi."""
    try:
        # Dataframe dari data produk
        df = pd.DataFrame(products)

        # Hapus baris dengan title invalid
        df = df[df['Title'].str.lower() != 'unknown product']

        # Transformasi Price
        df['Price'] = df['Price'].replace(r'[^\d.]', '', regex=True)
        df['Price'] = df['Price'].replace('', np.nan).astype(float) * 16000
        df.dropna(subset=['Price'], inplace=True)

        # Transformasi Rating
        df['Rating'] = df['Rating'].astype(str).replace(r'[^0-9\.]', '', regex=True)
        df['Rating'] = df['Rating'].replace('', np.nan).infer_objects(copy=False)
        df.dropna(subset=['Rating'], inplace= True)

        df['Rating'] = df['Rating'].astype(float)

        # Transformasi Colors
        df['Colors'] = df['Colors'].astype(str).replace(r'\D', '', regex=True)
        df['Colors'] = df['Colors'].replace('', np.nan).infer_objects(copy=False)
        df.dropna(subset=['Colors'], inplace=True)

        df['Colors'] = df['Colors'].astype(int)

        # Transformasi Size
        df['Size'] = df['Size'].replace(r'Size:\s*', '', regex=True)
        df['Size'] = df['Size'].replace('', np.nan)
        df.dropna(subset=['Size'], inplace= True)

        # Transformasi Gender
        df['Gender'] = df['Gender'].astype(str).replace(r'Gender:\s*', '', regex=True)
        df.dropna(subset=['Gender'], inplace= True)

        # Hapus Duplikat dan Null
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)

        # Menambahkan kolom Timestamp
        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return df
    except Exception as e:
        logging.error(f"Transformasi data gagal: {e}")
        raise