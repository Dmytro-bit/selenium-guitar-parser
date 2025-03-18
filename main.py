import os

from selenium_parser import SeleniumParser

if __name__ == "__main__":

    os.makedirs("shop_data", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    selenium_parser = SeleniumParser()

    site_link_list = [
        "https://www.thomann.de/ie/1-4_size_classical_guitars.html",
        "https://www.thomann.de/ie/3-4_size_classical_guitars.html"
    ]

    params_keys = ['Colour', 'Top', 'Pickup System', 'Scale', 'Cutaway', 'Back and Sides', "Nut width in mm", 'Hardcase']

    for item in site_link_list:
        products_urls, title = selenium_parser.get_products_urls(url=item)
        selenium_parser.generate_data_file(title, products_urls, params_keys)

    print("End of script")
