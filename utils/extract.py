import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
# from transform import transform_df 

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}


def fetching_content(url):
    """Mengambil konten HTML dari URL yang diberikan."""
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None


def extract_product_data(article):
    """Mengambil data fashion berupa Title, Price, Rating, Colors, Size, Gender (element html)."""
    try:
        title_tag = article.find('h3', class_='product-title')
        title = title_tag.text.strip() if title_tag else 'Unknown Title'
        rating_tag = article.find('p', string=lambda text: text and 'Rating' in text)
        rating = rating_tag.text.strip() if rating_tag else 'Not Rated'
        price_tag = article.find('div', class_='price-container')
        price = price_tag.text.strip() if price_tag else 'Price Unavailable'
        colors_tag = article.find('p', string=lambda text: text and 'Colors' in text)
        colors = colors_tag.text.strip() if colors_tag else 'No Color Info'
        size_tag = article.find('p', string=lambda text: text and 'Size' in text)
        size = size_tag.text.strip() if size_tag else 'No Size Info'
        gender_tag = article.find('p', string=lambda text: text and 'Gender' in text)
        gender = gender_tag.text.strip() if gender_tag else 'No Gender Info'

        products= {
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Colors': colors,
            'Size': size,
            'Gender': gender
        }

        return products
    except Exception as e:
        print(f"[ERROR] Gagal memproses elemen produk: {e}")
        return None


def scrape_products(base_url, first_page_url, start_page=2, delay=1):
    """Fungsi utama untuk mengambil keseluruhan data, mulai dari requests hingga menyimpannya dalam variabel data."""
    data = []
    page_number = start_page

    try:
        print(f"Scraping halaman pertama: {first_page_url}")
        content = fetching_content(first_page_url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            div_element = soup.find_all('div', class_='product-details')
            for div in div_element:
                try:
                    product = extract_product_data(div)
                    data.append(product)
                except Exception as e:
                    print(f"[ERROR] Gagal memproses produk di halaman pertama: {e}")
        else:
            print("Gagal mengambil halaman pertama, lanjut ke halaman 2.")
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan pada halaman pertama: {e}")

    while True:
        url = base_url.format(page_number)
        print(f"Scraping halaman: {url}")

        try:
            content = fetching_content(url)
            if content:
                soup = BeautifulSoup(content, "html.parser")
                div_element = soup.find_all('div', class_='product-details')

                for div in div_element:
                    try:
                        product = extract_product_data(div)
                        data.append(product)
                    except Exception as e:
                        print(f"[ERROR] Gagal memproses produk di halaman {page_number}: {e}")

                next_button = soup.find('li', class_='page-item next')
                if next_button:
                    page_number += 1
                    time.sleep(delay)  
                else:
                    print("Tidak ada tombol next, scraping selesai.")
                    break
            else:
                print(f"[WARNING] Tidak ada konten yang diambil dari {url}. Menghentikan scraping.")
                break
        except Exception as e:
            print(f"[ERROR] Terjadi kesalahan saat scraping {url}: {e}")
            break

    print(f"Total produk berhasil diambil: {len(data)}")
    return data

