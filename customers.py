"""
customers.py

Defines the Customer class.
"""


from typing import TYPE_CHECKING

from cart import Cart
from models import Product

if TYPE_CHECKING:
    from orders import Order


class Customer:

    def __init__ (self,customer_id: int, name: str, email: str,phone: str = ""):
        self.__customer_id = customer_id
        self.__name = name
        self.__email = email
        self.__phone = phone

        self.__cart: Cart = Cart()
        self.__orders: list["Order"] = []

    # Getters
    def get_customer_id(self) -> int:
        return self.__customer_id

    def get_name(self) -> str:
        return self.__name

    def get_email(self) -> str:
        return self.__email

    def get_phone(self) -> str:
        return self.__phone

    def get_cart(self) -> Cart:
        return self.__cart

    def get_order_history(self) -> list["Order"]:
        return self.__orders

    # Setters

    def set_customer_id(self, new_id: int) -> None:
        if new_id < 0:
            raise ValueError(
                "Customer ID cannot be negative."
            )

        self.__customer_id = new_id

    def set_name(self, new_name: str) -> None:
        if not new_name or new_name.strip() == "":
            raise ValueError(
                "Customer name cannot be empty."
            )

        self.__name = new_name

    def set_email(self, new_email: str) -> None:
        if not new_email or new_email.strip() == "":
            raise ValueError(
                "Customer email cannot be empty."
            )

        self.__email = new_email

    def set_phone(self, new_phone: str) -> None:
        self.__phone = new_phone

    def set_cart(self, new_cart: Cart) -> None:
        if not isinstance(new_cart, Cart):
            raise ValueError(
                "Invalid cart object."
            )

        self.__cart = new_cart

    # Methods

    def add_order(self, order: "Order") -> None:
        self.__orders.append(order)

    def add_to_cart(
        self,
        product: Product,
        quantity: int = 1
    ) -> None:
        self.__cart.add_item(
            product,
            quantity
        )

    def remove_from_cart(
        self,
        product_id: int
    ) -> None:
        self.__cart.remove_item(product_id)

    def __repr__(self) -> str:
        return (
            f"Customer("
            f"id={self.__customer_id}, "
            f"name='{self.__name}')"
        )

    def __str__(self) -> str:
        return self.__name