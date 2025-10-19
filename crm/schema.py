import re
import graphene
from graphene_django import DjangoObjectType
from django.db import transaction
from django.core.exceptions import ValidationError
from crm.models import Customer, Product, Order

# -------------------- TYPES --------------------
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "products", "total_amount", "order_date")


# -------------------- MUTATIONS --------------------
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=False)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        if phone and not re.match(r'^(\+?\d{7,15}|(\d{3}-\d{3}-\d{4}))$', phone):
            raise ValidationError("Invalid phone format")
        customer = Customer.objects.create(name=name, email=email, phone=phone)
        return CreateCustomer(customer=customer, message="Customer created successfully.")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(graphene.JSONString, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @transaction.atomic
    def mutate(self, info, input):
        customers = []
        errors = []

        for data in input:
            try:
                name = data.get("name")
                email = data.get("email")
                phone = data.get("phone", None)

                if not name or not email:
                    raise ValidationError("Name and email are required")
                if Customer.objects.filter(email=email).exists():
                    raise ValidationError(f"Email {email} already exists")
                if phone and not re.match(r'^(\+?\d{7,15}|(\d{3}-\d{3}-\d{4}))$', phone):
                    raise ValidationError(f"Invalid phone format for {email}")

                customers.append(Customer(name=name, email=email, phone=phone))
            except ValidationError as e:
                errors.append(str(e))

        created_customers = Customer.objects.bulk_create(customers)
        return BulkCreateCustomers(customers=created_customers, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(required=False)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise ValidationError("Price must be positive.")
        if stock < 0:
            raise ValidationError("Stock cannot be negative.")
        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime(required=False)

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise ValidationError("Invalid customer ID.")

        if not product_ids:
            raise ValidationError("At least one product must be selected.")

        products = Product.objects.filter(id__in=product_ids)
        if products.count() != len(product_ids):
            raise ValidationError("One or more product IDs are invalid.")

        total_amount = sum([p.price for p in products])
        order = Order.objects.create(
            customer=customer, total_amount=total_amount, order_date=order_date
        )
        order.products.set(products)
        return CreateOrder(order=order)


# -------------------- QUERY --------------------
class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)

    def resolve_all_customers(root, info):
        return Customer.objects.all()

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()


# -------------------- MUTATION --------------------
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
