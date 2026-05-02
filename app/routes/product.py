from flask import Blueprint, render_template, request, jsonify
from app.models.product import Product

product_bp = Blueprint("product", __name__)


@product_bp.route("/products")
def products():
    category = request.args.get("category")
    search = request.args.get("search")
    device = request.args.get("device")

    query = Product.query.filter_by(is_active=True)

    if category:
        query = query.filter(Product.category == category)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if device:
        query = query.filter(
            Product.name.ilike(f"%{device}%")
            | Product.description.ilike(f"%{device}%")
            | Product.feature_1.ilike(f"%{device}%")
            | Product.feature_2.ilike(f"%{device}%")
            | Product.feature_3.ilike(f"%{device}%")
        )

    products = query.all()

    return render_template(
        "products.html",
        products=products,
        category=category,
        search=search,
        device=device,
    )


@product_bp.route("/api/products")
def api_products():
    products = Product.query.filter_by(is_active=True).all()
    return jsonify([product.to_dict() for product in products])