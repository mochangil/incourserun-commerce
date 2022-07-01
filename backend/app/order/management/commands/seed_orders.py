import random
from datetime import date, datetime
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from app.order.models import Order, OrderProduct
from app.user.models import User
from app.product.models import Product

class Command(BaseCommand):

    help = "This command creates orders"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many ordesr you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        faker = Faker('ko_KR')
        all_users = User.objects.all()
        all_products = Product.objects.all()

        seeder.add_entity(
            Order,
            number,
            {
                    "user": random.choice(all_users),
                    "shipping_name": faker.name(),
                    "shipping_phone": faker.phone_number(),
                    "shipping_zipcode": seeder.faker.zipcode(),
                    "shipping_address": faker.address(),
                    "shipping_address_detail": "",
                    "shipping_request": "",
                    "shipping_status": "결제완료",
                    "pay_method": "신용카드",
                    "pay_status": "결제완료",
                    "pay_date": date.today(),
                    "total_price": 27000,
                    "delivery_fee": 0,
                    "is_cancelled": False,
                    "created_at": datetime.now()
            }
        )

        created_orders = seeder.execute()
        created_clean = flatten(list(created_orders.values()))
        for pk in created_clean:
            for i in range(random.randint(3,5)):
                order = Order.objects.get(pk=pk)
                OrderProduct.objects.create(
                    order = order,
                    product = random.choice(all_products),
                    quantity = random.randint(1, 5),
                    price = 27000,
                    shipping_status = "결제완료"
                )
        self.stdout.write(self.style.SUCCESS(f"{number} orders created"))