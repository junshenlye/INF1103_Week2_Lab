"""Supplier entity used by products through an association."""


class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not isinstance(supplier_id, str) or not supplier_id.strip():
            raise ValueError("Supplier ID must be non-empty text.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Supplier name must be non-empty text.")
        email = contact_email.strip() if isinstance(contact_email, str) else ""
        if (email.count("@") != 1 or " " in email
                or not all(email.split("@"))):
            raise ValueError("Contact email must be a valid email address.")

        self.__supplier_id = supplier_id.strip().upper()
        self.__name = name.strip()
        self.__contact_email = email.lower()

    @property
    def supplier_id(self) -> str:
        return self.__supplier_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.supplier_id} | Name: {self.name} | "
              f"Email: {self.contact_email}")
