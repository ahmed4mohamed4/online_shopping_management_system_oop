"""
cart.py

Defines Cart and CartItem classes.
"""


from models import Product


class CartItem:
    """
    # Represents a product and its quantity in a cart
    ## Attributes:
    - product: The product object.
    - quantity: The quantity of the product in the cart.
    """

    def __init__(
        self,
        product: Product,
        quantity: int = 1
    ):

        self.set_product (product)
        self.set_quantity (quantity)

    # Getters
    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    # Setters

    def set_product(self, new_product: Product) -> None:
        if not isinstance(new_product, Product):
            raise ValueError("Invalid product object.")

        self.__product = new_product

    def set_quantity(self, new_quantity: int) -> None:
        if new_quantity <= 0:
            raise ValueError("Quantity must be positive.")

        self.__quantity = new_quantity

    # Methods
    def calculate_subtotal (self) -> float:
        return self.__product.get_price () * self.__quantity

    def update_quantity (self, quantity: int) -> None:
        self.set_quantity (quantity)

    def __repr__(self) -> str:
        return (
            f"CartItem("
            f"product='{self.__product.get_name()}', "
            f"qty={self.__quantity})"
        )


class Cart:
    """
    # Represents a customer's shopping cart
    ## Attributes:
    - items: A list of CartItem objects in the cart.
    """

    def __init__(self):
        self.__items: list[CartItem] = []

    # Getter
    def get_items(self) -> list[CartItem]:
        return self.__items

    # Setters
    def set_items(self, new_items: list[CartItem]) -> None:
        if not isinstance(new_items, list):
            raise ValueError ("Items must be a list of CartItem objects.")

        for item in new_items:
            if not isinstance(item, CartItem):
                raise ValueError("All items must be CartItem objects.")

        self.__items = new_items

    # Methods
    def add_item(self, product: Product, quantity: int = 1) -> None:

        if not isinstance (product, Product):
            raise ValueError("Invalid product object.")

        if quantity <= 0:
            raise ValueError("Quantity must be positive." )

        for item in self.__items:

            if item.get_product().get_product_id() == product.get_product_id(): # Check if the product is available or not.
                item.set_quantity (item.get_quantity() + quantity)
                return

        self.__items.append(
            CartItem(product, quantity)
        )

    def remove_item(self, product_id: int) -> None:
        self.__items = [item for item in self.__items if item.get_product().get_product_id() != product_id]

    def update_item_quantity (self, product_id: int, quantity: int) -> None:

        for item in self.__items:

            if (item.get_product().get_product_id() == product_id):
                item.update_quantity (quantity)
                return

        raise ValueError (
            f"Product id {product_id} "
            f"not found in cart."
        )

    def calculate_total (self) -> float:
        return sum (item.calculate_subtotal () for item in self.__items)

    def display_cart (self) -> str:

        if not self.__items:
            return "Cart is empty."

        lines = ["Cart contents:"]

        for item in self.__items:

            product = item.get_product ()

            lines.append(
                f"  - {product.get_name()} "
                f"x{item.get_quantity()} = "
                f"${item.calculate_subtotal():.2f}"
            )

        lines.append(
            f"Total: ${self.calculate_total():.2f}"
        )

        return "\n".join (lines)

    def clear_cart(self) -> None:
        self.__items = []

    def __repr__(self) -> str:
        return (
            f"Cart(items={len(self.__items)})"
        )