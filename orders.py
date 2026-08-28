"""
orders.py

Defines Order and OrderItem classes.
"""

from typing import Optional, TYPE_CHECKING

from models import Product


if TYPE_CHECKING:
    from customers import Customer


class OrderItem:
    """
    # Represents a line item within a finalized order
    ## Attributes:
    - product: Product object associated with this order item
    - quantity: Number of units of the product in this order item
    - unit_price: Price per unit of the product at the time of order
    """

    def __init__ (self, product: Product, quantity: int, unit_price: Optional[float] = None):
        self.set_product (product)
        self.set_quantity (quantity)
        self.set_unit_price (unit_price)

    # Getters
    def get_product (self) -> Product:
        return self.__product

    def get_quantity (self) -> int:
        return self.__quantity

    def get_unit_price (self) -> float:
        return self.__unit_price

    # Setters
    def set_product (self, new_product: Product) -> None:

        if not isinstance (new_product, Product):
            raise ValueError ("Invalid product object.")

        self.__product = new_product

    def set_quantity (self, new_quantity: int) -> None:

        if new_quantity <= 0:
            raise ValueError ("Quantity must be positive.")

        self.__quantity = new_quantity

    def set_unit_price (self,new_price: float) -> None:

        if new_price < 0:
            raise ValueError ("Unit price cannot be negative.")

        self.__unit_price = new_price

    # Methods
    def calculate_subtotal (self) -> float:
        return self.__unit_price * self.__quantity

    def __repr__(self) -> str:
        return (
            f"OrderItem("
            f"product='{self.__product.get_name()}', "
            f"qty={self.__quantity})"
        )


class Order:
    """
    # Represents a placed order
    ## Attributes:
    - order_id: Unique identifier for the order
    - customer: Customer object who placed the order
    - items: List of OrderItem objects in the order
    - status: Current status of the order (pending, cancelled, completed)
    - total: Total cost of the order
    """

    STATUS_PENDING = "pending"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"

    def __init__ (self, order_id: int, customer: "Customer", items: Optional[list[OrderItem]] = None):
        self.set_order_id (order_id)
        self.__customer = customer

        self.__items: list[OrderItem] = items if items is not None else []

        self.__status = self.STATUS_PENDING
        self.__total = self.calculate_total ()

    # Getters
    def get_order_id(self) -> int:
        return self.__order_id

    def get_customer(self) -> "Customer":
        return self.__customer

    def get_items(self) -> list[OrderItem]:
        return self.__items

    def get_status(self) -> str:
        return self.__status

    def get_total(self) -> float:
        return self.__total

    # Setters
    def set_order_id (self, new_id: int) -> None:
        if new_id < 0:
            raise ValueError ("Order ID cannot be negative.")

        self.__order_id = new_id

    def set_customer (self, new_customer: "Customer") -> None:
        if not isinstance (new_customer, Customer):
            raise ValueError ("Invalid customer object.")

        self.__customer = new_customer

    def set_status (self, new_status: str) -> None:

        valid_statuses = {
            self.STATUS_PENDING,
            self.STATUS_CANCELLED,
            self.STATUS_COMPLETED
        }

        if new_status.lower () not in valid_statuses:
            raise ValueError ("Invalid order status.")

        self.__status = new_status

    # Methods
    def add_item (self, item: OrderItem) -> None:

        if not isinstance(item, OrderItem):
            raise ValueError("Invalid order item.")

        self.__items.append(item)
        self.calculate_total ()

    def calculate_total(self) -> float:

        self.__total = sum (item.calculate_subtotal () for item in self.__items)

        return self.__total

    def display_order(self) -> str:

        lines = [
            f"Order #{self.__order_id} - "
            f"Customer: "
            f"{self.__customer.get_name()} - "
            f"Status: {self.__status}"
        ]

        for item in self.__items:

            product = item.get_product()

            lines.append(
                f"  - {product.get_name()} "
                f"x{item.get_quantity()} "
                f"@ ${item.get_unit_price():.2f} "
                f"= ${item.calculate_subtotal():.2f}"
            )

        lines.append(
            f"Total: ${self.calculate_total():.2f}"
        )

        return "\n".join(lines)

    def cancel_order(self) -> tuple[bool, str]:

        if self.__status == self.STATUS_CANCELLED:
            return (
                False,
                f"Order #{self.__order_id} is already cancelled."
            )

        self.__status = self.STATUS_CANCELLED

        for item in self.__items:

            product = item.get_product()

            if hasattr (product, "update_stock"):
                product.update_stock(
                    item.get_quantity()
                )

        return (
            True,
            f"Order #{self.__order_id} cancelled successfully."
        )

    def __repr__(self) -> str:
        return (
            f"Order("
            f"id={self.__order_id}, "
            f"customer='{self.__customer.get_name()}', "
            f"status='{self.__status}')"
        )