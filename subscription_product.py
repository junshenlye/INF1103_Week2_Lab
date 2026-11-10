"""SubscriptionProduct specialization."""
from product import Product
from supplier import Supplier


class SubscriptionProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, duration_months: int) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if (isinstance(duration_months, bool)
                or not isinstance(duration_months, int)
                or duration_months <= 0):
            raise ValueError("duration_months must be a positive whole number.")
        self.__duration_months = duration_months

    @property
    def duration_months(self) -> int:
        return self.__duration_months

    def display_information(self) -> None:
        super().display_information()
        print(f"Duration Months: {self.duration_months:g} months")

    def get_fulfilment_info(self) -> str:
        return "Digital access for the subscription duration."
