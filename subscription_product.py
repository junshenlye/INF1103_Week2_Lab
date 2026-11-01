"""SubscriptionProduct specialization."""
import math
from product import Product

class SubscriptionProduct(Product):
    def __init__(self, product_id, name, price, stock, duration_months):
        super().__init__(product_id, name, price, stock)
        if isinstance(duration_months, bool) or not isinstance(duration_months, (int, float)) or not math.isfinite(duration_months) or duration_months <= 0:
            raise ValueError("duration_months must be finite and positive.")
        if not isinstance(duration_months, int):
            raise ValueError("duration_months must be a whole number.")
        self.__duration_months = duration_months

    @property
    def duration_months(self):
        return self.__duration_months

    def display_information(self):
        super().display_information()
        print(f"Duration Months: {self.duration_months:g} months")
        print(self.get_fulfilment_info())

    def get_fulfilment_info(self):
        return "Digital access for the subscription duration."
