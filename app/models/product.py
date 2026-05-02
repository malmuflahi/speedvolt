from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(180), nullable=False)
    category = db.Column(db.String(80), nullable=False)

    price = db.Column(db.Numeric(10, 2), nullable=False)
    wholesale_price = db.Column(db.Numeric(10, 2), nullable=False)

    badge = db.Column(db.String(80), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)

    feature_1 = db.Column(db.String(120), nullable=True)
    feature_2 = db.Column(db.String(120), nullable=True)
    feature_3 = db.Column(db.String(120), nullable=True)

    min_qty = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": float(self.price),
            "wholesale_price": float(self.wholesale_price),
            "badge": self.badge,
            "image": self.image,
            "description": self.description,
            "features": [
                self.feature_1,
                self.feature_2,
                self.feature_3,
            ],
            "min_qty": self.min_qty,
        }
