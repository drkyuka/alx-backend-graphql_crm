import os
import random
import sys
from datetime import datetime, timedelta
from decimal import Decimal

# Add the project directory to the Python path to allow imports from the crm app
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_graphql_crm.settings")
import django

django.setup()

# Import models now that the Django environment is configured
from crm.models import Customer, Order, Product


def clear_database():
    """Delete all existing data from the database."""
    print("Clearing existing data...")
    Order.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()
    print("Database cleared successfully.")


def create_customers():
    """Create 17 unique customers."""
    print("Creating 17 customers...")

    customers_data = [
        {
            "name": "Alice Johnson",
            "email": "alice.johnson@email.com",
            "phone": "+1-555-0101",
        },
        {"name": "Bob Smith", "email": "bob.smith@email.com", "phone": "+1-555-0102"},
        {
            "name": "Carol Davis",
            "email": "carol.davis@email.com",
            "phone": "+1-555-0103",
        },
        {
            "name": "David Wilson",
            "email": "david.wilson@email.com",
            "phone": "+1-555-0104",
        },
        {"name": "Emma Brown", "email": "emma.brown@email.com", "phone": "+1-555-0105"},
        {
            "name": "Frank Miller",
            "email": "frank.miller@email.com",
            "phone": "+1-555-0106",
        },
        {
            "name": "Grace Taylor",
            "email": "grace.taylor@email.com",
            "phone": "+1-555-0107",
        },
        {
            "name": "Henry Anderson",
            "email": "henry.anderson@email.com",
            "phone": "+1-555-0108",
        },
        {"name": "Ivy Thomas", "email": "ivy.thomas@email.com", "phone": "+1-555-0109"},
        {
            "name": "Jack Jackson",
            "email": "jack.jackson@email.com",
            "phone": "+1-555-0110",
        },
        {"name": "Kate White", "email": "kate.white@email.com", "phone": "+1-555-0111"},
        {
            "name": "Liam Harris",
            "email": "liam.harris@email.com",
            "phone": "+1-555-0112",
        },
        {"name": "Mia Martin", "email": "mia.martin@email.com", "phone": "+1-555-0113"},
        {
            "name": "Noah Garcia",
            "email": "noah.garcia@email.com",
            "phone": "+1-555-0114",
        },
        {
            "name": "Olivia Rodriguez",
            "email": "olivia.rodriguez@email.com",
            "phone": "+1-555-0115",
        },
        {"name": "Paul Lewis", "email": "paul.lewis@email.com", "phone": "+1-555-0116"},
        {
            "name": "Quinn Walker",
            "email": "quinn.walker@email.com",
            "phone": "+1-555-0117",
        },
    ]

    customers = []
    for customer_data in customers_data:
        customer = Customer.objects.create(**customer_data)
        customers.append(customer)

    print(f"Created {len(customers)} customers successfully.")
    return customers


def create_products():
    """Create 26 unique products."""
    print("Creating 26 products...")

    products_data = [
        {
            "name": "Laptop Pro",
            "price": Decimal("1299.99"),
        },
        {
            "name": "Wireless Mouse",
            "price": Decimal("29.99"),
        },
        {
            "name": "Mechanical Keyboard",
            "price": Decimal("89.99"),
        },
        {
            "name": "4K Monitor",
            "price": Decimal("399.99"),
        },
        {
            "name": "Smartphone",
            "price": Decimal("799.99"),
        },
        {
            "name": "Wireless Headphones",
            "price": Decimal("199.99"),
        },
        {
            "name": "Tablet",
            "price": Decimal("349.99"),
        },
        {
            "name": "Webcam HD",
            "price": Decimal("79.99"),
        },
        {
            "name": "USB-C Hub",
            "price": Decimal("49.99"),
        },
        {
            "name": "Portable SSD",
            "price": Decimal("129.99"),
        },
        {
            "name": "Bluetooth Speaker",
            "price": Decimal("59.99"),
        },
        {
            "name": "Smartwatch",
            "price": Decimal("299.99"),
        },
        {
            "name": "Wireless Charger",
            "price": Decimal("39.99"),
        },
        {
            "name": "Gaming Chair",
            "price": Decimal("249.99"),
        },
        {
            "name": "Desk Lamp",
            "price": Decimal("34.99"),
        },
        {
            "name": "Printer",
            "price": Decimal("149.99"),
        },
        {
            "name": "Router",
            "price": Decimal("179.99"),
        },
        {
            "name": "Power Bank",
            "price": Decimal("44.99"),
        },
        {
            "name": "Microphone",
            "price": Decimal("89.99"),
        },
        {
            "name": "Cable Management",
            "price": Decimal("19.99"),
        },
        {
            "name": "Monitor Stand",
            "price": Decimal("54.99"),
        },
        {
            "name": "Laptop Stand",
            "price": Decimal("39.99"),
        },
        {
            "name": "Phone Case",
            "price": Decimal("24.99"),
        },
        {
            "name": "Stylus Pen",
            "price": Decimal("29.99"),
        },
        {
            "name": "Card Reader",
            "price": Decimal("14.99"),
        },
        {
            "name": "Ethernet Cable",
            "price": Decimal("12.99"),
        },
    ]

    products = []
    for product_data in products_data:
        product = Product.objects.create(**product_data)
        products.append(product)

    print(f"Created {len(products)} products successfully.")
    return products


def create_orders(customers, products):
    """Create orders ensuring 90% of products appear in multiple orders."""
    print("Creating orders to ensure 90% of products appear multiple times...")

    # Calculate how many products need to be in multiple orders (90% of 26 = 23.4, so 24 products)
    products_in_multiple_orders = int(len(products) * 0.9)
    if products_in_multiple_orders < len(products) * 0.9:
        products_in_multiple_orders += 1

    print(
        f"Target: {products_in_multiple_orders} products should appear in multiple orders"
    )

    # Track product usage
    product_usage = {product.id: 0 for product in products}
    orders = []

    # Create orders with strategic product distribution
    order_count = 0

    # First pass: Create orders that include many products to ensure coverage
    for i in range(15):  # Create 15 larger orders
        customer = random.choice(customers)

        # Create order with random date in the last 6 months
        order_date = datetime.now() - timedelta(days=random.randint(1, 180))

        order = Order.objects.create(
            customer=customer, total_amount=Decimal("0.00"), order_date=order_date
        )

        # Select 3-8 random products for this order
        num_products = random.randint(3, 8)
        selected_products = random.sample(products, num_products)

        total_amount = Decimal("0.00")
        for product in selected_products:
            quantity = random.randint(1, 3)
            order.products.add(product, through_defaults={"quantity": quantity})
            total_amount += product.price * quantity
            product_usage[product.id] += 1

        order.total_amount = total_amount
        order.save()
        orders.append(order)
        order_count += 1

    # Second pass: Ensure products that haven't appeared in multiple orders get more coverage
    products_needing_coverage = [
        product for product in products if product_usage[product.id] < 2
    ]

    while (
        len([p for p in products if product_usage[p.id] >= 2])
        < products_in_multiple_orders
    ):
        customer = random.choice(customers)
        order_date = datetime.now() - timedelta(days=random.randint(1, 180))

        order = Order.objects.create(
            customer=customer, total_amount=Decimal("0.00"), order_date=order_date
        )

        # Focus on products that need more coverage
        if products_needing_coverage:
            # Select 2-4 products that need coverage plus 1-3 random products
            needed_products = random.sample(
                products_needing_coverage,
                min(random.randint(2, 4), len(products_needing_coverage)),
            )
            random_products = random.sample(
                [p for p in products if p not in needed_products], random.randint(1, 3)
            )
            selected_products = needed_products + random_products
        else:
            # Just select random products
            selected_products = random.sample(products, random.randint(2, 5))

        total_amount = Decimal("0.00")
        for product in selected_products:
            quantity = random.randint(1, 2)
            order.products.add(product, through_defaults={"quantity": quantity})
            total_amount += product.price * quantity
            product_usage[product.id] += 1

        order.total_amount = total_amount
        order.save()
        orders.append(order)
        order_count += 1

        # Update products needing coverage
        products_needing_coverage = [
            product for product in products if product_usage[product.id] < 2
        ]

    # Third pass: Add a few more random orders for variety
    for i in range(5):
        customer = random.choice(customers)
        order_date = datetime.now() - timedelta(days=random.randint(1, 180))

        order = Order.objects.create(
            customer=customer, total_amount=Decimal("0.00"), order_date=order_date
        )

        # Select 1-4 random products
        selected_products = random.sample(products, random.randint(1, 4))

        total_amount = Decimal("0.00")
        for product in selected_products:
            quantity = random.randint(1, 2)
            order.products.add(product, through_defaults={"quantity": quantity})
            total_amount += product.price * quantity
            product_usage[product.id] += 1

        order.total_amount = total_amount
        order.save()
        orders.append(order)
        order_count += 1

    # Calculate final statistics
    products_in_multiple = len([p for p in products if product_usage[p.id] >= 2])
    percentage = (products_in_multiple / len(products)) * 100

    print(f"Created {order_count} orders successfully.")
    print(
        f"Products appearing in multiple orders: {products_in_multiple}/{len(products)} ({percentage:.1f}%)"
    )

    # Print detailed statistics
    print("\nProduct usage statistics:")
    for product in products:
        usage_count = product_usage[product.id]
        print(f"  {product.name}: {usage_count} orders")

    return orders


def main():
    """Main function to populate the database."""
    print("Starting database population...")
    print("=" * 50)

    # Clear existing data
    clear_database()

    # Create customers
    customers = create_customers()

    # Create products
    products = create_products()

    # Create orders
    orders = create_orders(customers, products)

    print("=" * 50)
    print("Database population completed successfully!")
    print("Summary:")
    print(f"  - Customers: {len(customers)}")
    print(f"  - Products: {len(products)}")
    print(f"  - Orders: {len(orders)}")

    # Final verification using the correct relationship name
    products_in_multiple = (
        Product.objects.filter(order_products__in=Order.objects.all())
        .annotate(order_count=django.db.models.Count("order_products", distinct=True))
        .filter(order_count__gte=2)
        .count()
    )

    percentage = (products_in_multiple / len(products)) * 100
    print(
        f"  - Products in multiple orders: {products_in_multiple}/{len(products)} ({percentage:.1f}%)"
    )


if __name__ == "__main__":
    main()
