from hmac import compare_digest

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from app.models.order import Order

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.before_request
def require_admin_login():
    if request.endpoint == "admin.login":
        return None

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login", next=request.path))

    return None


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        password = request.form.get("password", "")
        expected_password = current_app.config.get("ADMIN_PASSWORD", "")

        if expected_password and compare_digest(password, expected_password):
            session["admin_logged_in"] = True
            next_url = request.args.get("next") or url_for("admin.orders")

            if not next_url.startswith("/") or next_url.startswith("//"):
                next_url = url_for("admin.orders")

            return redirect(next_url)

        error = "Incorrect admin password."

    return render_template("admin_login.html", error=error)


@admin_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.login"))


@admin_bp.route("/orders")
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin_orders.html", orders=orders)
