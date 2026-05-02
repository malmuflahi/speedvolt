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
            "image": "/static/images/brand2/IMG_0133.jpeg",
            "description": "Braided USB-C cable built for fast charging and daily wholesale use.",
            "feature_1": "60W Fast Charging",
            "feature_2": "Braided Nylon",
            "feature_3": "USB-C to USB-C",
            "min_qty": 5,
            "is_active": True,
        },
        {
            "name": "SpeedVolt 65W Car Charger",
            "category": "Chargers",
            "price": Decimal("18.99"),
            "wholesale_price": Decimal("11.25"),
            "badge": "65W PD",
            "image": "/static/images/brand2/IMG_0147.jpeg",
            "description": "High-output car charger with dual-port fast charging for daily drivers.",
            "feature_1": "65W Output",
            "feature_2": "Compact Design",
            "feature_3": "Wholesale Ready",
            "min_qty": 3,
            "is_active": True,
        },
        {
            "name": "SpeedVolt In-Car Smartphone Holder",
            "category": "Car Accessories",
            "price": Decimal("11.99"),
            "wholesale_price": Decimal("7.25"),
            "badge": "360 Degree",
            "image": "/static/images/brand2/IMG_3746.jpeg",
            "description": "Adjustable in-car holder with secure suction and smooth rotation.",
            "feature_1": "Dashboard Mount",
            "feature_2": "Car Mount",
            "feature_3": "360 Degree Rotation",
            "min_qty": 3,
            "is_active": True,
        },
        {
            "name": "SpeedVolt Vacuum Suction Magnetic Bracket",
            "category": "Car Accessories",
            "price": Decimal("16.99"),
            "wholesale_price": Decimal("10.50"),
            "badge": "Magnetic",
            "image": "/static/images/brand2/IMG_3748.jpeg",
            "description": "Premium magnetic bracket with vacuum suction and one-handed operation.",
            "feature_1": "Magnetic Attraction",
            "feature_2": "Vacuum Suction",
            "feature_3": "Multi-angle",
            "min_qty": 3,
            "is_active": True,
        },
        {
            "name": "SpeedVolt 10000mAh Power Bank",
            "category": "Power Banks",
            "price": Decimal("24.99"),
            "wholesale_price": Decimal("17.00"),
            "badge": "Magnetic",
            "image": "/static/images/brand2/IMG_4151.jpeg",
            "description": "Magnetic wireless power bank with built-in wires and secure chips.",
            "feature_1": "10000mAh",
            "feature_2": "Built-in Wire",
            "feature_3": "Wireless Charging",
            "min_qty": 2,
            "is_active": True,
        },
        {
            "name": "SpeedVolt 2.4A iPhone Cable",
            "category": "Cables",
            "price": Decimal("5.99"),
            "wholesale_price": Decimal("3.85"),
            "badge": "2.4A",
            "image": "/static/images/brand2/IMG_0134.jpeg",
            "description": "Fast charging cable for iPhone buyers with compact retail packaging.",
            "feature_1": "2.4A Output",
            "feature_2": "iPhone Compatible",
            "feature_3": "3.3 Feet",
            "min_qty": 5,
            "is_active": True,
        },
        {
            "name": "SpeedVolt Stereo Music Earphone",
            "category": "Earphones",
            "price": Decimal("9.99"),
            "wholesale_price": Decimal("5.95"),
            "badge": "Wired Audio",
            "image": "/static/images/brand2/IMG_3745.jpeg",
            "description": "Wired stereo earphones with mic control and clean retail packaging.",
            "feature_1": "HD Microphone",
            "feature_2": "Type-C Control",
            "feature_3": "Stereo Sound",
            "min_qty": 4,
            "is_active": True,
        },
    ]

    product_names = [product_data["name"] for product_data in products]
    Product.query.filter(~Product.name.in_(product_names)).update(
        {"is_active": False},
        synchronize_session=False,
    )

    for product_data in products:
        product = Product.query.filter_by(name=product_data["name"]).first()

        if product is None:
            product = Product(**product_data)
            db.session.add(product)
            continue

        for key, value in product_data.items():
            setattr(product, key, value)

    db.session.commit()
