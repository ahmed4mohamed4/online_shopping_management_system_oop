"""
system.py

Defines the ShoppingSystem class.
"""

from typing import Optional

from models import Category, Product, PhysicalProduct
from customers import Customer
from orders import Order, OrderItem


class ShoppingSystem:
    """
    # Central system coordinating the whole application
    ## Attributes:
    - categories: List of all product categories
    - products: List of all products in the catalog
    - customers: List of all registered customers
    - orders: List of all orders placed in the system
    - next_order_id: Counter for generating unique order IDs
    """

    def __init__(self):

        self.__categories: list[Category] = []
        self.__products: list[Product] = []
        self.__customers: list[Customer] = []
        self.__orders: list[Order] = []

        self.__next_order_id = 1

    # ---------- Getters ----------

    def get_categories(self) -> list[Category]:
        return self.__categories

    def get_products(self) -> list[Product]:
        return self.__products

    def get_customers(self) -> list[Customer]:
        return self.__customers

    def get_orders(self) -> list[Order]:
        return self.__orders

    # ---------- Category management ----------

    def add_category(
        self,
        category: Category
    ) -> None:

        if not isinstance(category, Category):
            raise ValueError(
                "Invalid category object."
            )

        self.__categories.append(category)

    # ---------- Product management ----------

    def add_product(
        self,
        product: Product
    ) -> None:

        if not isinstance(product, Product):
            raise ValueError(
                "Invalid product object."
            )

        self.__products.append(product)

    def remove_product(self, product_id: int) -> bool:
        """Remove a product from the catalog

        Refuses to remove a product that is still referenced by a pending order
        """

        for order in self.__orders:

            if order.get_status() != Order.STATUS_PENDING:
                continue

            for item in order.get_items():
                if item.get_product().get_product_id() == product_id:
                    return False

        for product in self.__products:

            if (
                product.get_product_id()
                == product_id
            ):
                self.__products.remove(product)
                return True

        return False

    def update_product(self, product_id: int, **kwargs) -> bool:

        for product in self.__products:

            if product.get_product_id() != product_id:
                continue

            for key, value in kwargs.items():

                if key == "product_id":
                    product.set_product_id(value)

                elif key == "name":
                    product.set_name(value)

                elif key == "price":
                    product.set_price(value)

                elif key == "category":
                    product.set_category(value)

                else:
                    return False

            return True

        return False

    def search_product(
        self,
        name: str,
        min_price: float = 0.0,
        max_price: float = float('inf')
    ) -> list[Product]:
        """Advanced search by name and price range."""
        name_lower = name.lower()
        results = []

        for product in self.__products:
            if (
                name_lower in product.get_name().lower() and
                min_price <= product.get_price() <= max_price
            ):
                results.append(product)

        return results

    # ---------- Customer management ----------

    def register_customer(self, customer: Customer) -> None:

        if not isinstance(customer, Customer):
            raise ValueError(
                "Invalid customer object."
            )

        self.__customers.append(customer)

    # ---------- Order management ----------

    def create_order(
        self,
        customer_id: int
    ) -> tuple[Optional[Order], str]:
        """Create an order from the customer's current cart.

        Returns (order, message): order is None on failure. Runs in two
        explicit phases so no state is mutated unless every line item is
        confirmed available first:

          Phase 1 - validate every cart item (no side effects yet).
          Phase 2 - build the order and deduct stock, now that we know
                    the whole cart can be fulfilled.
        """

        customer = self._find_customer(customer_id)

        if customer is None:
            return None, f"Customer id {customer_id} not found."

        cart = customer.get_cart()
        cart_items = cart.get_items()

        if not cart_items:
            return (
                None,
                f"Cannot create order: "
                f"{customer.get_name()}'s cart is empty."
            )

        # ---- Phase 1: validate everything before touching any state ----
        for cart_item in cart_items:

            product = cart_item.get_product()
            quantity = cart_item.get_quantity()

            if not product.is_available(quantity):
                return (
                    None,
                    f"Product '{product.get_name()}' is not available "
                    f"in the requested quantity."
                )

        # ---- Phase 2: everything checked out, now build + mutate ----
        order_items: list[OrderItem] = [
            OrderItem(
                cart_item.get_product(),
                cart_item.get_quantity(),
                cart_item.get_product().get_price()
            )
            for cart_item in cart_items
        ]

        for order_item in order_items:

            product = order_item.get_product()

            if isinstance(product, PhysicalProduct):
                product.update_stock(-order_item.get_quantity())

        order = Order(
            self.__next_order_id,
            customer,
            order_items
        )

        self.__next_order_id += 1

        self.__orders.append(order)
        customer.add_order(order)
        cart.clear_cart()

        return order, "Order created successfully."

    def cancel_order(
        self,
        order_id: int
    ) -> tuple[bool, str]:
        """Cancel an order by id. Returns (success, message)."""

        for order in self.__orders:

            if order.get_order_id() == order_id:
                return order.cancel_order()

        return False, f"Order id {order_id} not found."

    # ---------- Display helpers ----------

    def display_products(self) -> str:

        if not self.__products:
            return "No products available."

        lines = ["Products:"]

        for product in self.__products:
            lines.append(f"  {product.get_details()}")

        return "\n".join(lines)

    def display_customers(self) -> str:

        if not self.__customers:
            return "No customers registered."

        lines = ["Customers:"]

        for customer in self.__customers:
            lines.append(
                f"  [{customer.get_customer_id()}] "
                f"{customer.get_name()} "
                f"({customer.get_email()})"
            )

        return "\n".join(lines)

    def display_orders(self) -> str:

        if not self.__orders:
            return "No orders placed."

        lines = ["Orders:"]

        for order in self.__orders:
            lines.append(order.display_order())

        return "\n".join(lines)

    # ----------- Generate System ------------

    def generate_system_report(self) -> str:
        """Generates advanced analytics including total revenue and top spender."""
        if not self.__orders:
            return "No orders processed yet."

        total_revenue = 0.0
        customer_spending: dict[str, float] = {}

        for order in self.__orders:
            if order.get_status() == Order.STATUS_CANCELLED:
                continue
                
            o_total = order.get_total()
            c_name = order.get_customer().get_name()
            
            total_revenue += o_total
            customer_spending[c_name] = customer_spending.get(c_name, 0.0) + o_total

        top_customer = max(customer_spending, key=customer_spending.get) if customer_spending else "None"
        top_spending = customer_spending.get(top_customer, 0.0)

        lines = [
            "\n" + "=" * 80,
            "  SMART SYSTEM ANALYTICS REPORT (Added by System Engineer)",
            "=" * 80,
            f"Total Registered Customers : {len(self.__customers)}",
            f"Total Products in Catalog  : {len(self.__products)}",
            f"Total Orders Processed   : {len(self.__orders)}",
            f"Total Valid Revenue      : ${total_revenue:,.2f}",
            f"Top Spender              : {top_customer} (${top_spending:,.2f})",
            "=" * 80
        ]
        return "\n".join(lines)

    # ---------- Internal helpers ----------

    def _find_customer(
        self,
        customer_id: int
    ) -> Optional[Customer]:

        for customer in self.__customers:

            if (
                customer.get_customer_id()
                == customer_id
            ):
                return customer

        return None