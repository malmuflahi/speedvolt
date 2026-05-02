from flask import Blueprint, render_template
from app.models.product import Product

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    products = Product.query.filter_by(is_active=True).limit(4).all()
    return render_template("index.html", products=products)