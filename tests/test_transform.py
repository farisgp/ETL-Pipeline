import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from utils.transform import transform_df  

def test_transform_df_basic():
    """Pastikan transformasi berjalan dengan benar pada data normal."""
    products = [
        {
            "Title": "Kaos Polos",
            "Price": "$10.5",
            "Rating": "4.5",
            "Colors": "5",
            "Size": "XL",
            "Gender": "Male"
        }
    ]

    df = transform_df(products)

    # Pastikan kolom hasil ada semua
    expected_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'timestamp']
    assert all(col in df.columns for col in expected_columns)

    # Cek tipe data
    assert df['Price'].dtype == float
    assert df['Rating'].dtype == float
    assert df['Colors'].dtype == int
    assert isinstance(df['timestamp'].iloc[0], str)

    # Cek hasil transformasi spesifik
    assert df['Price'].iloc[0] == 10.5 * 16000  # konversi ke rupiah
    assert df['Rating'].iloc[0] == 4.5
    assert df['Colors'].iloc[0] == 5
    assert df['Size'].iloc[0] == "XL"
    assert df['Gender'].iloc[0] == "Male"


def test_transform_df_remove_invalid_title():
    """Pastikan baris dengan title 'unknown product' dihapus."""
    products = [
        {"Title": "Unknown Product", "Price": "$5", "Rating": "Rating: 3", "Colors": "Colors: 2", "Size": "Size : 38", "Gender": "Gender: Female"}
    ]
    df = transform_df(products)
    assert df.empty  # harus terhapus


def test_transform_df_invalid_numeric_fields():
    """Pastikan data dengan Price atau Rating kosong dihapus."""
    products = [
        {"Title": "T-Shirt", "Price": "", "Rating": "Rating: 4.5", "Colors": "Colors: 5", "Size": "Size : L", "Gender": "Gender: Male"},
        {"Title": "T-Shirt", "Price": "$10", "Rating": "", "Colors": "Colors: 5", "Size": "Size : L", "Gender": "Gender: Male"},
    ]
    df = transform_df(products)
    assert df.empty  

def test_transform_df_clean_text_fields():
    """Pastikan teks 'Size :' dan 'Gender:' dibersihkan dengan benar."""
    products = [
        {
            "Title": "Jaket",
            "Price": "$20",
            "Rating": "5",
            "Colors": "10",
            "Size": "M",
            "Gender": "Gender: Female"
        }
    ]

    df = transform_df(products)
    assert df['Size'].iloc[0] == "M"
    assert df['Gender'].iloc[0] == "Female"


def test_transform_df_duplicate_and_null():
    """Pastikan duplikat dan nilai kosong dihapus."""
    products = [
        {
            "Title": "Kaos",
            "Price": "$15",
            "Rating": "Rating: 4",
            "Colors": "Colors: 3",
            "Size": "Size : 40",
            "Gender": "Gender: Male"
        },
        {
            "Title": "Kaos",  
            "Price": "$15",
            "Rating": "Rating: 4",
            "Colors": "Colors: 3",
            "Size": "Size : 40",
            "Gender": "Gender: Male"
        }
    ]
    df = transform_df(products)
    assert len(df) == 1  # duplikat terhapus


def test_transform_df_exception_handling(monkeypatch):
    """Pastikan error di dalam fungsi dilempar ulang."""
    # Paksa pandas.DataFrame untuk memunculkan error
    monkeypatch.setattr(pd, "DataFrame", lambda x: (_ for _ in ()).throw(Exception("DataFrame error")))

    with pytest.raises(Exception, match="DataFrame error"):
        transform_df([])  # harus melempar error

