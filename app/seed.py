from decimal import Decimal

from app.extensions import db
from app.models.product import Product


def seed_products():
    if Product.query.count() > 0:
        return

    products = [
        Product(
            name="SpeedVolt 60W USB-C Cable",
            category="Cables",
            price=Decimal("6.99"),
            wholesale_price=Decimal("4.75"),
            badge="60W Fast",
            image=None,
            description="Braided USB-C cable built for fast charging and daily wholesale use.",
            feature_1="60W Fast Charging",
            feature_2="Braided Nylon",
            feature_3="USB-C to USB-C",
            min_qty=5,
        ),
        Product(
            name="SpeedVolt 45W Wall Charger",
            category="Chargers",
            price=Decimal("14.99"),
            wholesale_price=Decimal("9.50"),
            badge="Best Seller",
            image=None,
            description="Compact wall charger for fast and reliable charging.",
            feature_1="45W Output",
            feature_2="Compact Design",
            feature_3="Wholesale Ready",
            min_qty=3,
        ),
        Product(
            name="SpeedVolt MagSafe Car Holder",
            category="Car Accessories",
            price=Decimal("11.99"),
            wholesale_price=Decimal("7.25"),
            badge="MagSafe",
            image=None,
            description="Strong magnetic car holder with premium grip and clean design.",
            feature_1="Strong Magnet",
            feature_2="Car Mount",
            feature_3="360 Degree Rotation",
            min_qty=3,
        ),
        Product(
            name="SpeedVolt 10000mAh Power Bank",
            category="Power Banks",
            price=Decimal("24.99"),
            wholesale_price=Decimal("17.00"),
            badge="Portable Power",
            image=None,
            description="Slim power bank designed for daily mobile charging.",
            feature_1="10000mAh",
            feature_2="Portable",
            feature_3="Fast Charging",
            min_qty=2,
        ),
    ]

    db.session.add_all(products)
    db.session.commit()
