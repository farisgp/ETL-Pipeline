import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from utils.extract import fetching_content, extract_product_data, scrape_products


@patch("utils.extract.requests.Session")
def test_fetching_content_success(mock_session):
    """Test jika fetching_content berhasil mengembalikan konten"""
    mock_response = MagicMock()
    mock_response.content = b"""
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Test Product</h3>
                    <div class="price-container">$10</div>
                    <p>Rating: 5 stars</p>
                    <p>Colors: Red, Blue</p>
                    <p>Size: M, L</p>
                    <p>Gender: Unisex</p>
                </div>
            </body>
        </html>
        """
    mock_response.raise_for_status.return_value = None

    mock_session_instance = MagicMock()
    mock_session_instance.get.return_value = mock_response
    mock_session.return_value = mock_session_instance

    result = fetching_content("https://fashion-studio.dicoding.dev/")
    assert result == b"""
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Test Product</h3>
                    <div class="price-container">$10</div>
                    <p>Rating: 5 stars</p>
                    <p>Colors: Red, Blue</p>
                    <p>Size: M, L</p>
                    <p>Gender: Unisex</p>
                </div>
            </body>
        </html>
        """

def test_extract_product_data_complete():
    """Test ekstraksi data produk lengkap."""
    html = """
    <div class="product-details">
        <h3 class="product-title">Cool Jacket</h3>
        <p>Rating: 4.8</p>
        <div class="price-container">$120</div>
        <p>Colors: Red, Blue</p>
        <p>Size: M, L</p>
        <p>Gender: Unisex</p>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_="product-details")

    product = extract_product_data(article)

    assert product["Title"] == "Cool Jacket"
    assert product["Rating"] == "Rating: 4.8"
    assert product["Price"] == "$120"
    assert "Colors" in product["Colors"]
    assert "Size" in product["Size"]
    assert "Gender" in product["Gender"]


def test_extract_product_data_incomplete():
    """Test jika beberapa elemen hilang, tetap aman dan tidak error."""
    html = """
    <div class="product-details">
        <h3 class="product-title">Simple T-shirt</h3>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_="product-details")

    product = extract_product_data(article)

    assert product["Title"] == "Simple T-shirt"
    assert product["Price"] == "Price Unavailable"
    assert product["Rating"] == "Not Rated"
    assert product["Colors"] == "No Color Info"
    assert product["Size"] == "No Size Info"
    assert product["Gender"] == "No Gender Info"

@patch("utils.extract.fetching_content")
def test_scrape_products_multiple_pages(mock_fetching_content):
    """Test scraping multi-halaman dengan tombol next."""
    # Halaman 1
    html_page_1 = """
    <html>
        <body>
            <div class="product-details">
                <h3 class="product-title">Product A</h3>
                <div class="price-container">$10</div>
            </div>
            <li class="page-item next"><a href="#">Next</a></li>
        </body>
    </html>
    """
    # Halaman 2
    html_page_2 = """
    <html>
        <body>
            <div class="product-details">
                <h3 class="product-title">Product B</h3>
                <div class="price-container">$20</div>
            </div>
        </body>
    </html>
    """

    mock_fetching_content.side_effect = [html_page_1, html_page_2]

    result = scrape_products(
        base_url="https://fashion-studio.dicoding.dev/page{}",
        first_page_url="https://fashion-studio.dicoding.dev/",
        start_page=2,
        delay=0
    )

    assert len(result) == 2
    assert result[0]["Title"] == "Product A"
    assert result[1]["Title"] == "Product B"


@patch("utils.extract.fetching_content")
def test_scrape_products_no_content(mock_fetching_content):
    """Test jika tidak ada konten HTML yang diambil."""
    mock_fetching_content.return_value = None

    result = scrape_products(
        base_url="https://fashion-studio.dicoding.dev/page{}",
        first_page_url="https://fashion-studio.dicoding.dev/",
        start_page=2,
        delay=0
    )

    assert result == []
