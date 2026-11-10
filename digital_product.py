"""DigitalProduct specialization."""
import math
from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if (isinstance(download_size, bool)
                or not isinstance(download_size, (int, float))
                or not math.isfinite(download_size) or download_size <= 0):
            raise ValueError("download_size must be finite and positive.")
        self.__download_size = download_size

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.download_size:g} MB")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally by download."
