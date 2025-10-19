from crm.models import Customer, Product

Customer.objects.get_or_create(name="Alice", email="alice@example.com")
Product.objects.get_or_create(name="Phone", price=299.99, stock=20)
Product.objects.get_or_create(name="Headphones", price=59.99, stock=50)
print("✅ Seed data created!")
