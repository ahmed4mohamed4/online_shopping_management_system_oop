"""
models.py

Defines:
- Category
- Product
- PhysicalProduct
- DigitalProduct
"""


from typing import Optional


class Category:
    """
    # Represents a product category
    ## Attributes:
    - category_id: Unique identifier for the category.
    - name: Name of the category.
    - description: Description of the category.
    """

    def __init__ (
        self,
        category_id: int,
        name: str,
        description: str
    ):
        # self.__category_id = category_id
        # self.__name = name
        # self.__description = description
        
        self.set_category_id (category_id)
        self.set_name (name)
        self.set_description (description)

    # Getters
    def get_category_id (self) -> int:
        return self.__category_id

    def get_name (self) -> str:
        return self.__name

    def get_description (self) -> str:
        return self.__description

    # Setters
    def set_category_id (self, new_id: int) -> None:
        if new_id < 0:
            raise ValueError ("Category ID cannot be negative.")

        self.__category_id = new_id

    def set_name (self, new_name: str) -> None:
        if not new_name or new_name.strip () == "":
            raise ValueError ("Category name cannot be empty.")

        self.__name = new_name
    
    def set_description (self, new_description: str) -> None:
        if not new_description or new_description.strip() == "":
            raise ValueError ("Category description cannot be empty.")

        self.__description = new_description

    # Methods

    def update_name (self, new_name: str) -> None:
        self.set_name (new_name)

    def update_description (self, new_description: str) -> None:
        self.set_description (new_description)

    def __repr__ (self) -> str:
        return (
            f"Category("
            f"id={self.__category_id}, "
            f"name='{self.__name}')"
        )

    def __str__ (self) -> str:
        return self.__name


class Product:
    """
    # Represents a generic product
    ## Attributes:
    - product_id: Unique identifier for the product.
    - name: Name of the product.
    - price: Price of the product.
    - category: Category to which the product belongs.
    """

    def __init__ (
        self,
        product_id: int,
        name: str,
        price: float,
        category: Optional [Category] = None
    ):
        self.set_product_id (product_id)
        self.set_name (name)
        self.set_price (price)
        self.set_category (category)

    # Getters
    def get_product_id (self) -> int:
        return self.__product_id

    def get_name (self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_category(self) -> Optional[Category]:
        return self.__category

    # Setters

    def set_product_id (self, new_id: int) -> None:
        if new_id < 0:
            raise ValueError("Product ID cannot be negative.")

        self.__product_id = new_id

    def set_name (self, new_name: str) -> None:
        if not new_name or new_name.strip() == "":
            raise ValueError("Product name cannot be empty.")

        self.__name = new_name

    def set_price(self, new_price: float) -> None:
        if new_price < 0:
            raise ValueError("Price cannot be negative.")

        self.__price = new_price

    def set_category(
        self,
        new_category: Optional[Category]
    ) -> None:
        if new_category is not None and not isinstance(
            new_category,
            Category
        ):
            raise ValueError ("Invalid category object.")

        self.__category = new_category

    # Methods
    def get_details (self) -> str:
        category_name = (
            self.__category.get_name () if self.__category else "Uncategorized"
        )

        return (
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Category: {category_name}"
        )

    def update_price (self, new_price: float) -> None:
        self.set_price (new_price)

    def is_available (self, quantity: int) -> bool:
        return quantity > 0

    def __repr__(self) -> str:
        return (
            f"Product("
            f"id={self.__product_id}, "
            f"name='{self.__name}')"
        )

    def __str__(self) -> str:
        return self.__name


class PhysicalProduct(Product):
    """
    # Represents a physical product with stock and weight
    ## Inherits from Product
    ## Attributes:
    - stock_quantity: Number of items available in stock.
    - weight: Weight of the product in kilograms.
    """

    def __init__(
        self,
        product_id: int,
        name: str,
        price: float,
        category: Optional[Category] = None,
        stock_quantity: int = 0,
        weight: float = 0.0
    ):
        super ().__init__ (
            product_id,
            name,
            price,
            category
        )

        self.set_stock_quantity (stock_quantity)
        self.set_weight (weight)

    # Getters
    def get_stock_quantity (self) -> int:
        return self.__stock_quantity

    def get_weight (self) -> float:
        return self.__weight

    # Setters
    def set_stock_quantity(self, new_stock: int) -> None:
        if new_stock < 0:
                raise ValueError("Stock quantity cannot be negative.")

        self.__stock_quantity = new_stock

    def set_weight(self, new_weight: float) -> None:
        if new_weight < 0:
            raise ValueError("Weight cannot be negative.")

        self.__weight = new_weight

    # Methods

    def update_stock(self, quantity: int) -> None:
        """
        + quantity: The number of items to add (positive) or remove (negative) from stock.
        """
        new_stock = self.__stock_quantity + quantity

        if new_stock < 0:
            raise ValueError("Stock quantity cannot go negative.")

        self.__stock_quantity = new_stock

    def get_details (self) -> str:
        base = super ().get_details ()

        return (
            f"{base} | "
            f"Physical | "
            f"Stock: {self.__stock_quantity} | "
            f"Weight: {self.__weight}kg"
        )

    def is_available (self, quantity: int) -> bool:
        return 0 < quantity <= self.__stock_quantity


class DigitalProduct(Product):
    """
    Represents a digital product.
    ## Inherits from Product
    ## Attributes:
    - file_size: Size of the file in megabytes.
    - file_format: Format of the file (e.g., PDF, DOC).
    - download_url: URL where the file can be downloaded.
    """

    def __init__(
        self,
        product_id: int,
        name: str,
        price: float,
        category: Optional[Category] = None,
        file_size: float = 0.0,
        file_format: str = "",
        download_url: str = ""
    ):
        super().__init__(
            product_id,
            name,
            price,
            category
        )

        self.set_file_size(file_size)
        self.set_file_format(file_format)
        self.set_download_url(download_url)

    # Getters

    def get_file_size(self) -> float:
        return self.__file_size

    def get_file_format(self) -> str:
        return self.__file_format

    def get_download_url(self) -> str:
        return self.__download_url

    # Setters

    def set_file_size(self, new_size: float) -> None:
        if new_size < 0:
            raise ValueError("File size cannot be negative.")

        self.__file_size = new_size

    def set_file_format(self, new_format: str) -> None:
        if not new_format or new_format.strip() == "":
            raise ValueError("File format cannot be empty.")

        self.__file_format = new_format

    def set_download_url(self, new_url: str) -> None:
        if not new_url or new_url.strip() == "":
            raise ValueError("Download URL cannot be empty.")

        self.__download_url = new_url

    # Methods

    def get_details (self) -> str:
        base = super ().get_details ()

        return (
            f"{base} | "
            f"Digital | "
            f"Format: {self.__file_format} | "
            f"Size: {self.__file_size}MB"
        )


if __name__ == "__main__":
    # Example usage
    electronics = Category(1, "Electronics", "Electronic gadgets and devices")
    laptop = PhysicalProduct(101, "Laptop", 999.99, electronics,
                              stock_quantity=10, weight=2.5)

    books = Category (2, "Books", "Various kinds of books")
    ebook = DigitalProduct (201, "Python Programming Guide", 19.99, books,
                            file_size=15.5, file_format="PDF",
                            download_url="https://example.com/downloads/python-guide.pdf")

    print(laptop.get_details())
    print(ebook.get_details())