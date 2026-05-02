from decimal import Decimal

from app.extensions import db
from app.models.customer import Customer
from app.models.order import Order, OrderItem
from app.models.product import Product


class OrderService:
    @staticmethod
    def create_order(data, cart_items):
        if not isinstance(cart_items, list) or not cart_items:
            raise ValueError("Cart is empty.")

        customer = Customer(
            business_name=data.get("business_name"),
            name=data.get("name"),
            phone=data.get("phone"),
            address=data.get("address"),
        )

        order = Order(
            customer=customer,
            payment_method=data.get("payment_method"),
            notes=data.get("notes"),
            subtotal=Decimal("0.00"),
            total=Decimal("0.00"),
            status="New",
        )

        subtotal = Decimal("0.00")

        for item in cart_items:
            try:
                product_id = int(item.get("id", 0))
                quantity = int(item.get("quantity", 0))
            except (TypeError, ValueError):
                raise ValueError("Invalid cart item.")

            if product_id <= 0 or quantity <= 0:
                raise ValueError("Invalid item quantity.")

            product = Product.query.filter_by(id=product_id, is_active=True).first()

            if product is None:
                raise ValueError("Product is not available.")

            if quantity < product.min_qty:
                raise ValueError(
                    f"{product.name} minimum quantity is {product.min_qty}."
                )

            unit_price = product.wholesale_price
            line_total = quantity * unit_price
            subtotal += line_total

            order.items.append(
                OrderItem(
                    product_id=product.id,
                    product_name=product.name,
                    quantity=quantity,
                    unit_price=unit_price,
                    line_total=line_total,
                )
            )

        order.subtotal = subtotal
        order.total = subtotal

        db.session.add(order)
        db.session.commit()

        return order
