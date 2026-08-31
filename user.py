"""
user.py

Interactive user interface for the Online Shopping System.

Run:
    python user.py

This file imports all project classes and lets the user test the
complete system through terminal input.
"""

from models import Category, Product, PhysicalProduct, DigitalProduct
from customers import Customer
from cart import Cart, CartItem
from orders import Order, OrderItem
from system import ShoppingSystem


WIDTH = 80


# ============================================================
# Display Helpers
# ============================================================

def banner(title: str) -> None:
    print("\n" + "=" * WIDTH)
    print(f"  {title}")
    print("=" * WIDTH)


def pause() -> None:
    input("\nPress Enter to continue...")


# ============================================================
# Input Helpers
# ============================================================

def read_int(prompt: str, minimum=None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                print(f"Please enter a number >= {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


def read_float(prompt: str, minimum=None) -> float:
    while True:
        try:
            value = float(input(prompt))
            if minimum is not None and value < minimum:
                print(f"Please enter a number >= {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def read_text(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def find_category(system: ShoppingSystem, category_id: int):
    for category in system.get_categories():
        if category.get_category_id() == category_id:
            return category
    return None


def find_product(system: ShoppingSystem, product_id: int):
    for product in system.get_products():
        if product.get_product_id() == product_id:
            return product
    return None


def find_customer(system: ShoppingSystem, customer_id: int):
    for customer in system.get_customers():
        if customer.get_customer_id() == customer_id:
            return customer
    return None


def show_categories(system: ShoppingSystem) -> None:
    if not system.get_categories():
        print("No categories.")
        return

    for category in system.get_categories():
        print(
            f"[{category.get_category_id()}] "
            f"{category.get_name()} - "
            f"{category.get_description()}"
        )


def show_products(system: ShoppingSystem) -> None:
    if not system.get_products():
        print("No products.")
        return

    for product in system.get_products():
        print(product.get_details())


def show_customers(system: ShoppingSystem) -> None:
    if not system.get_customers():
        print("No customers.")
        return

    for customer in system.get_customers():
        print(
            f"[{customer.get_customer_id()}] "
            f"{customer.get_name()} | "
            f"{customer.get_email()} | "
            f"{customer.get_phone()}"
        )


# ============================================================
# Category
# ============================================================

def create_category(system: ShoppingSystem) -> None:
    banner("ADD CATEGORY")

    category_id = read_int("Category ID: ", 0)
    name = read_text("Category name: ")
    description = read_text("Description: ")

    try:
        category = Category(category_id, name, description)
        system.add_category(category)
        print("Category added successfully.")
    except ValueError as error:
        print(f"Error: {error}")


# ============================================================
# Product
# ============================================================

def create_product(system: ShoppingSystem) -> None:
    banner("ADD PRODUCT")

    if not system.get_categories():
        print("Create a category first.")
        return

    show_categories(system)

    product_id = read_int("Product ID: ", 0)
    name = read_text("Product name: ")
    price = read_float("Price: ", 0)
    category_id = read_int("Category ID: ", 0)

    category = find_category(system, category_id)

    if category is None:
        print("Category not found.")
        return

    print("\n1. Physical product")
    print("2. Digital product")

    product_type = read_int("Choose product type: ", 1)

    try:
        if product_type == 1:
            stock = read_int("Stock quantity: ", 0)
            weight = read_float("Weight (kg): ", 0)

            product = PhysicalProduct(
                product_id,
                name,
                price,
                category,
                stock_quantity=stock,
                weight=weight
            )

        elif product_type == 2:
            file_size = read_float("File size (MB): ", 0)
            file_format = read_text("File format (PDF/MP4/etc.): ")
            download_url = read_text("Download URL: ")

            product = DigitalProduct(
                product_id,
                name,
                price,
                category,
                file_size=file_size,
                file_format=file_format,
                download_url=download_url
            )

        else:
            print("Invalid product type.")
            return

        system.add_product(product)
        print("Product added successfully.")

    except ValueError as error:
        print(f"Error: {error}")


# ============================================================
# Customer
# ============================================================

def create_customer(system: ShoppingSystem) -> None:
    banner("REGISTER CUSTOMER")

    customer_id = read_int("Customer ID: ", 0)
    name = read_text("Name: ")
    email = read_text("Email: ")
    phone = input("Phone (optional): ").strip()

    try:
        customer = Customer(
            customer_id,
            name,
            email,
            phone
        )
        system.register_customer(customer)
        print("Customer registered successfully.")
    except ValueError as error:
        print(f"Error: {error}")


# ============================================================
# Cart
# ============================================================

def add_to_cart(system: ShoppingSystem) -> None:
    banner("ADD PRODUCT TO CART")

    if not system.get_customers() or not system.get_products():
        print("You need at least one customer and one product.")
        return

    show_customers(system)
    customer_id = read_int("Customer ID: ", 0)
    customer = find_customer(system, customer_id)

    if customer is None:
        print("Customer not found.")
        return

    show_products(system)
    product_id = read_int("Product ID: ", 0)
    product = find_product(system, product_id)

    if product is None:
        print("Product not found.")
        return

    quantity = read_int("Quantity: ", 1)

    try:
        customer.add_to_cart(product, quantity)
        print("Product added to cart successfully.")
        print("\n" + customer.get_cart().display_cart())
    except ValueError as error:
        print(f"Error: {error}")


def view_cart(system: ShoppingSystem) -> None:
    banner("VIEW CUSTOMER CART")

    show_customers(system)
    customer_id = read_int("Customer ID: ", 0)

    customer = find_customer(system, customer_id)

    if customer is None:
        print("Customer not found.")
        return

    print(customer.get_cart().display_cart())


def update_cart(system: ShoppingSystem) -> None:
    banner("UPDATE CART ITEM")

    show_customers(system)
    customer_id = read_int("Customer ID: ", 0)

    customer = find_customer(system, customer_id)

    if customer is None:
        print("Customer not found.")
        return

    print(customer.get_cart().display_cart())

    product_id = read_int("Product ID: ", 0)
    quantity = read_int("New quantity: ", 1)

    try:
        customer.get_cart().update_item_quantity(
            product_id,
            quantity
        )
        print("Cart updated successfully.")
        print(customer.get_cart().display_cart())
    except ValueError as error:
        print(f"Error: {error}")


def remove_from_cart(system: ShoppingSystem) -> None:
    banner("REMOVE PRODUCT FROM CART")

    show_customers(system)
    customer_id = read_int("Customer ID: ", 0)

    customer = find_customer(system, customer_id)

    if customer is None:
        print("Customer not found.")
        return

    print(customer.get_cart().display_cart())

    product_id = read_int("Product ID: ", 0)
    customer.remove_from_cart(product_id)

    print("Remove operation completed.")
    print(customer.get_cart().display_cart())


# ============================================================
# Search / Product Operations
# ============================================================

def search_products(system: ShoppingSystem) -> None:
    banner("SEARCH PRODUCTS")

    name = input("Search name (empty = all names): ").strip()
    min_price = read_float("Minimum price: ", 0)
    max_price = read_float("Maximum price: ", 0)

    if max_price < min_price:
        print("Maximum price cannot be less than minimum price.")
        return

    results = system.search_product(
        name,
        min_price=min_price,
        max_price=max_price
    )

    if not results:
        print("No products found.")
        return

    print("\nResults:")
    for product in results:
        print(f"  {product.get_details()}")


def update_product(system: ShoppingSystem) -> None:
    banner("UPDATE PRODUCT")

    show_products(system)
    product_id = read_int("Product ID: ", 0)

    product = find_product(system, product_id)

    if product is None:
        print("Product not found.")
        return

    print("\n1. Update name")
    print("2. Update price")
    print("3. Update category")
    print("4. Update product ID")

    choice = read_int("Choose field: ", 1)

    try:
        if choice == 1:
            system.update_product(
                product_id,
                name=read_text("New name: ")
            )

        elif choice == 2:
            system.update_product(
                product_id,
                price=read_float("New price: ", 0)
            )

        elif choice == 3:
            show_categories(system)
            category_id = read_int("New category ID: ", 0)
            category = find_category(system, category_id)

            if category is None:
                print("Category not found.")
                return

            system.update_product(
                product_id,
                category=category
            )

        elif choice == 4:
            new_id = read_int("New product ID: ", 0)
            system.update_product(
                product_id,
                product_id=new_id
            )

        else:
            print("Invalid choice.")
            return

        print("Product updated successfully.")
        print(product.get_details())

    except ValueError as error:
        print(f"Error: {error}")


def stock_operation(system: ShoppingSystem) -> None:
    banner("STOCK OPERATION")

    physical_products = [
        product
        for product in system.get_products()
        if isinstance(product, PhysicalProduct)
    ]

    if not physical_products:
        print("No physical products.")
        return

    for product in physical_products:
        print(
            f"[{product.get_product_id()}] "
            f"{product.get_name()} | "
            f"Stock: {product.get_stock_quantity()}"
        )

    product_id = read_int("Product ID: ", 0)
    product = find_product(system, product_id)

    if not isinstance(product, PhysicalProduct):
        print("This is not a physical product.")
        return

    quantity = read_int(
        "Quantity to add/remove (use negative to remove): "
    )

    try:
        product.update_stock(quantity)
        print(
            f"New stock: {product.get_stock_quantity()}"
        )
    except ValueError as error:
        print(f"Error: {error}")


# ============================================================
# Orders
# ============================================================

def create_order(system: ShoppingSystem) -> None:
    banner("CREATE ORDER")

    show_customers(system)
    customer_id = read_int("Customer ID: ", 0)

    customer = find_customer(system, customer_id)

    if customer is None:
        print("Customer not found.")
        return

    print("\nCurrent cart:")
    print(customer.get_cart().display_cart())

    order, message = system.create_order(customer_id)

    print(f"\n{message}")

    if order is not None:
        print("\nCreated order:")
        print(order.display_order())


def cancel_order(system: ShoppingSystem) -> None:
    banner("CANCEL ORDER")

    if not system.get_orders():
        print("No orders.")
        return

    print(system.display_orders())

    order_id = read_int("Order ID: ", 0)

    success, message = system.cancel_order(order_id)

    print(message)

    if success:
        print("\nUpdated orders:")
        print(system.display_orders())


# ============================================================
# Display / Reports
# ============================================================

def display_all(system: ShoppingSystem) -> None:
    banner("SYSTEM DATA")

    print("\n--- Categories ---")
    show_categories(system)

    print("\n--- Products ---")
    show_products(system)

    print("\n--- Customers ---")
    show_customers(system)

    print("\n--- Orders ---")
    print(system.display_orders())

    print("\n--- Analytics ---")
    print(system.generate_system_report())


def remove_product(system: ShoppingSystem) -> None:
    banner("REMOVE PRODUCT")

    show_products(system)
    product_id = read_int("Product ID: ", 0)

    removed = system.remove_product(product_id)

    if removed:
        print("Product removed successfully.")
    else:
        print(
            "Product could not be removed. "
            "It may not exist or may be referenced by a pending order."
        )


# ============================================================
# Menu
# ============================================================

def print_menu() -> None:
    print(
        """
1.  Add category
2.  Add product
3.  Register customer
4.  Show categories
5.  Show products
6.  Show customers
7.  Add product to cart
8.  View customer cart
9.  Update cart quantity
10. Remove product from cart
11. Search products
12. Update product
13. Stock operation
14. Create order
15. Cancel order
16. Remove product
17. Display complete system data
0.  Exit
"""
    )


def main() -> None:
    system = ShoppingSystem()

    banner("ONLINE SHOPPING SYSTEM - USER MODE")

    while True:
        print_menu()
        choice = read_int("Choose an option: ", 0)

        try:
            if choice == 0:
                banner("GOODBYE")
                print("Program finished successfully.")
                break

            elif choice == 1:
                create_category(system)

            elif choice == 2:
                create_product(system)

            elif choice == 3:
                create_customer(system)

            elif choice == 4:
                banner("CATEGORIES")
                show_categories(system)

            elif choice == 5:
                banner("PRODUCTS")
                show_products(system)

            elif choice == 6:
                banner("CUSTOMERS")
                show_customers(system)

            elif choice == 7:
                add_to_cart(system)

            elif choice == 8:
                view_cart(system)

            elif choice == 9:
                update_cart(system)

            elif choice == 10:
                remove_from_cart(system)

            elif choice == 11:
                search_products(system)

            elif choice == 12:
                update_product(system)

            elif choice == 13:
                stock_operation(system)

            elif choice == 14:
                create_order(system)

            elif choice == 15:
                cancel_order(system)

            elif choice == 16:
                remove_product(system)

            elif choice == 17:
                display_all(system)

            else:
                print("Invalid choice.")

        except (ValueError, TypeError) as error:
            print(f"Operation failed: {error}")

        pause()


if __name__ == "__main__":
    main()
