import os
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from utils.load import load_to_postgresql, load_to_csv, load_to_google_sheets


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Title": ["Kaos Polos"],
        "Price": [100000],
        "Rating": [4.5]
    })


@patch("utils.load.create_engine")
def test_load_to_postgresql_success(mock_engine, sample_df, monkeypatch):
    """Pastikan data berhasil dikirim ke PostgreSQL dengan env lengkap."""
    # Set environment variable dummy
    monkeypatch.setenv("DB_USER", "user")
    monkeypatch.setenv("DB_PASS", "pass")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "testdb")

    mock_connection = MagicMock()
    mock_engine.return_value = mock_connection

    # Mock to_sql agar tidak benar-benar terhubung ke DB
    with patch.object(pd.DataFrame, "to_sql", return_value=None) as mock_to_sql:
        load_to_postgresql(sample_df, "product_test")
        mock_to_sql.assert_called_once()
        mock_engine.assert_called_once()


def test_load_to_postgresql_missing_env(sample_df, monkeypatch):
    """Pastikan fungsi menangani environment variable yang hilang."""
    # Kosongkan semua variabel env
    for var in ["DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", "DB_NAME"]:
        monkeypatch.delenv(var, raising=False)

    with patch("builtins.print") as mock_print:
        load_to_postgresql(sample_df)
        mock_print.assert_any_call(
            "Gagal menyimpan ke PostgreSQL: Missing environment variables: DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME"
        )


def test_load_to_csv(tmp_path, sample_df):
    """Pastikan file CSV dibuat dengan benar."""
    csv_file = tmp_path / "test_products.csv"
    load_to_csv(sample_df, filename=str(csv_file))
    assert csv_file.exists()
    df_loaded = pd.read_csv(csv_file)
    pd.testing.assert_frame_equal(df_loaded, sample_df)


@patch("utils.load.build")
@patch("utils.load.Credentials.from_service_account_file")
def test_load_to_google_sheets_success(mock_creds, mock_build, sample_df, monkeypatch):
    """Pastikan data berhasil dikirim ke Google Sheets."""
    # Set environment variable dummy
    monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "dummy.json")
    monkeypatch.setenv("GOOGLE_SHEET_ID", "sheet123")

    mock_service = MagicMock()
    mock_sheet = MagicMock()
    mock_service.spreadsheets.return_value = mock_sheet
    mock_build.return_value = mock_service

    load_to_google_sheets(sample_df)

    mock_build.assert_called_once()
    mock_creds.assert_called_once()
    mock_sheet.values.assert_called()