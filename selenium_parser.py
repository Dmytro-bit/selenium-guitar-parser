
from random import randint

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class SeleniumParser:
    def __init__(self):
        self._driver = webdriver.Firefox()
        self._wait = WebDriverWait(self._driver, 5)

    def __del__(self):
        self._driver.quit()

    def get_products_urls(self, url: str) -> tuple[list[str], str]:
        self._driver.get(url)
        self._wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "fx-product-list-entry"))
        )
        items = self._driver.find_elements(By.CLASS_NAME, "fx-product-list-entry")
        links_to_product = []

        file_title = (
            self._driver.find_element(By.CLASS_NAME, "header-headline__label")
            .text.strip()
            .replace("/", "__")
        )

        for item in items:
            product_url = item.find_element(By.TAG_NAME, "a").get_attribute("href")
            links_to_product.append(product_url)
        return links_to_product, file_title

    def generate_data_file(
            self, file_name: str, links_to_product: list[str], params_keys: list[str]
    ) -> None:
        data = []
        for index, url in enumerate(links_to_product):
            item_data = {}

            try:
                self._driver.get(url)
                self._wait.until(EC.presence_of_element_located((By.CLASS_NAME, "price")))
                name_div = self._driver.find_element(
                    By.CLASS_NAME, "fx-content-product__main"
                )
                name = name_div.find_element(By.TAG_NAME, "h1").text

                item_data["name"] = name
                item_data["price"] = self._driver.find_element(
                    By.CLASS_NAME, "price"
                ).text[1:]
                item_data["quantity"] = randint(1, 30)

                try:
                    item_data["rating"] = self._driver.find_element(
                        By.CLASS_NAME, "rating__value"
                    ).text
                except:
                    item_data["rating"] = None

                features = self._driver.find_elements(By.CLASS_NAME, "keyfeature")
                features_dict = {}
                for feature in features:
                    try:
                        feature_name = feature.find_element(
                            By.CLASS_NAME, "keyfeature__label"
                        ).text
                        feature_value = feature.find_element(
                            By.CLASS_NAME, "fx-text--bold"
                        ).text

                        if feature_name in params_keys:
                            features_dict[feature_name] = feature_value
                    except:
                        continue

                item_data["features"] = features_dict
                del features_dict

                images = self._driver.find_elements(By.CLASS_NAME, "ZoomImagePicture")

                images_list = []
                for image in images:
                    image_url = image.find_element(By.TAG_NAME, "img").get_attribute(
                        "src"
                    )
                    images_list.append(image_url)

                item_data["images"] = images_list
                del images_list

                data.append(item_data)

                print(f"Scraped: {name}")

            except Exception as e:
                print(f"Skipping item {index + 1} due to error: {e}")

        df = pd.DataFrame(data)
        df.to_csv(f"shop_data/{file_name}.csv", index=False)
