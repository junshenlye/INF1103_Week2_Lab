"""DigitalProduct specialization."""
import math
from product import Product

class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        if isinstance(download_size, bool) or not isinstance(download_size, (int, float)) or not math.isfinite(download_size) or download_size <= 0:
            raise ValueError("download_size must be finite and positive.")
        self.__download_size = download_size

    @property
    def download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.download_size:g} MB")
        print(self.get_fulfilment_info())

    def get_fulfilment_info(self):
        return "Delivered digitally by download."
