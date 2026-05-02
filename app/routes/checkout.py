from flask import abort, Blueprint, render_template, request, jsonify, session, url_for
from app.models.order import Order
from app.services.order_service import OrderService
from app.services.invoice_service import InvoiceService

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.route("/checkout")
def checkout():
    return render_template("checkout.html")


@checkout_bp.route("/place-order", methods=["POST"])
def place_order():
    data = request.get_json() or {}

    required = ["name", "phone", "address", "payment_method", "cart"]

    for field in required:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"{field} is required."
            }), 400

    try:
        order = OrderService.create_order(data, data["cart"])
        recent_order_ids = session.get("recent_order_ids", [])
        recent_order_ids.append(order.id)
        session["recent_order_ids"] = recent_order_ids[-5:]

        return jsonify({
            "success": True,
            "message": "Order created successfully.",
            "order_id": order.id,
            "invoice_url": url_for("checkout.invoice", order_id=order.id)
        })

    except Exception as error:
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400


@checkout_bp.route("/invoice/<int:order_id>")
def invoice(order_id):
    order = Order.query.get_or_404(order_id)
    recent_order_ids = session.get("recent_order_ids", [])

    if not session.get("admin_logged_in") and order.id not in recent_order_ids:
        abort(404)

    invoice_id = InvoiceService.format_order_id(order.id)

    return render_template(
        "invoice.html",
        order=order,
        invoice_id=invoice_id
    )
