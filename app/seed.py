from decimal import Decimal

from app.extensions import db
from app.models.product import Product


def seed_products():
    products = [
        {
            "name": "SpeedVolt 60W USB-C Cable",
            "category": "Cables",
            "price": Decimal("6.99"),
            "wholesale_price": Decimal("4.75"),
            "badge": "60W Fast",
            "image": "/static/images/brand/IMG_0130.jpeg",
            "description": "Braided USB-C cable built for fast charging and daily wholesale use.",
            "feature_1": "60W Fast Charging",
            "feature_2": "Braided Nylon",
            "feature_3": "USB-C to USB-C",
            "min_qty": 5,
        },
        {
            "name": "SpeedVolt 45W Wall Charger",
            "category": "Chargers",
            "price": Decimal("14.99"),
            "wholesale_price": Decimal("9.50"),
            "badge": "Best Seller",
            "image": "/static/images/brand/IMG_0137.jpeg",
            "description": "Compact wall charger for fast and reliable charging.",
            "feature_1": "45W Output",
            "feature_2": "Compact Design",
            "feature_3": "Wholesale Ready",
            "min_qty": 3,
        },
        {
            "name": "SpeedVolt MagSafe Car Holder",
            "category": "Car Accessories",
            "price": Decimal("11.99"),
            "wholesale_price": Decimal("7.25"),
            "badge": "MagSafe",
            "image": "/static/images/brand/IMG_0129.jpeg",
            "description": "Strong magnetic car holder with premium grip and clean design.",
            "feature_1": "Strong Magnet",
            "feature_2": "Car Mount",
            "feature_3": "360 Degree Rotation",
            "min_qty": 3,
        },
        {
            "name": "SpeedVolt 10000mAh Power Bank",
            "category": "Power Banks",
            "price": Decimal("24.99"),
            "wholesale_price": Decimal("17.00"),
            "badge": "Portable Power",
            "image": "/static/images/brand/IMG_0150.jpeg",
            "description": "Slim power bank designed for daily mobile charging.",
            "feature_1": "10000mAh",
            "feature_2": "Portable",
            "feature_3": "Fast Charging",
            "min_qty": 2,
        },
    ]

    for product_data in products:
        product = Product.query.filter_by(name=product_data["name"]).first()

        if product is None:
            product = Product(**product_data)
            db.session.add(product)
            continue

        for key, value in product_data.items():
            setattr(product, key, value)

    db.session.commit()
