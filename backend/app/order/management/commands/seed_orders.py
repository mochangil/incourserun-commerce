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
            "--number", default=1, type=int, help="How many orders you want to create"
        )

    def handle(self, *args, **options):
        n = options.get("number")
        all_users = User.objects.all()
        
        for _ in range(n):
            seeder = Seed.seeder()
            faker = Faker('ko_KR')
            status = random.choice(['결제완료', '상품준비중', '배송중', '배송완료'])
            seeder.add_entity(
                Order,
                1,
                {
                    "user": random.choice(all_users),
                    "shipping_name": faker.name(),
                    "shipping_phone": faker.phone_number(),
                    "shipping_zipcode": seeder.faker.zipcode(),
                    "shipping_address": faker.address(),
                    "shipping_address_detail": "",
                    "shipping_request": "",
                    "shipping_status": status,
                    "pay_method": "신용카드",
                    "pay_date": date.today(),
                    "total_price": 0,
                    "delivery_fee": 0,
                    "is_cancelled": False,
                    "created_at": datetime.now()
                }
            )

            created_orders = seeder.execute()
            created_clean = flatten(list(created_orders.values()))
            total_price = 0
            for pk in created_clean:
                order = Order.objects.get(pk=pk)
                order.order_number = order.created_at.strftime("%y%m%d") + str(order.id).zfill(4)
                product_ids = random.sample(range(2,7), random.randint(1,5))
                for i in product_ids:
                    product = Product.objects.get(pk=i)
                    quantity = random.randint(1, 5)
                    OrderProduct.objects.create(
                        order = order,
                        product = product,
                        quantity = quantity,
                        price = product.price, 
                        shipping_status = status,
                        is_cancelled = False
                    )
                    total_price += product.price * quantity
                order.total_price = total_price
                if total_price < 30000:
                    order.delivery_fee = 3000
                order.total_paid = order.total_price + order.delivery_fee
                order.save()

        self.stdout.write(self.style.SUCCESS(f"{n} orders created"))