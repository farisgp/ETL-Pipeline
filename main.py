import pandas as pd
from utils.extract import scrape_products
from utils.transform import transform_df
from utils.load import load_to_postgresql, load_to_csv, load_to_google_sheets
def main():
    """Fungsi utama untuk keseluruhan proses scraping hingga menyimpannya."""
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    FIRST_PAGE_URL = 'https://fashion-studio.dicoding.dev/'
    all_product_data = scrape_products(BASE_URL, FIRST_PAGE_URL)
    if all_product_data:
        DataFrame = transform_df(all_product_data)   
        print(DataFrame)
    else:
        print("Tidak ada data yang ditemukan.")
    transform = transform_df(all_product_data)
    df = pd.DataFrame(transform)
    print(df)

    load_to_postgresql(df)
    load_to_csv(df)
    load_to_google_sheets(df)
 
 
if __name__ == '__main__':
    main()