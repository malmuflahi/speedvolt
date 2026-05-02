let cart = [];

try {
    cart = JSON.parse(localStorage.getItem("speedvolt_cart")) || [];
} catch (error) {
    cart = [];
}

function safeNumber(value, fallback = 0) {
    const number = Number(value);
    return Number.isFinite(number) ? number : fallback;
}

function safeInteger(value, fallback = 0) {
    const number = parseInt(value, 10);
    return Number.isFinite(number) ? number : fallback;
}

function escapeHTML(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function saveCart() {
    localStorage.setItem("speedvolt_cart", JSON.stringify(cart));
    renderCart();
}

function addProductFromButton(button) {
    let product;

    try {
        product = JSON.parse(button.dataset.product);
    } catch (error) {
        return;
    }

    const productId = safeInteger(product.id);
    const minQty = Math.max(safeInteger(product.min_qty, 1), 1);
    const qtyInput = document.getElementById(`qty-${productId}`);
    const requestedQty = safeInteger(qtyInput?.value, minQty);
    const quantity = Math.max(requestedQty, minQty);

    if (!productId) return;

    const existing = cart.find(item => safeInteger(item.id) === productId);

    if (existing) {
        existing.quantity = safeInteger(existing.quantity) + quantity;
    } else {
        cart.push({
            id: productId,
            name: product.name,
            price: safeNumber(product.wholesale_price),
            quantity: quantity,
            min_qty: minQty
        });
    }

    saveCart();
    openCart();
}

function updateQuantity(productId, change) {
    const id = safeInteger(productId);
    const item = cart.find(item => safeInteger(item.id) === id);
    if (!item) return;

    item.quantity = safeInteger(item.quantity) + change;

    if (item.quantity < safeInteger(item.min_qty, 1)) {
        item.quantity = safeInteger(item.min_qty, 1);
    }

    saveCart();
}

function removeItem(productId) {
    const id = safeInteger(productId);
    cart = cart.filter(item => safeInteger(item.id) !== id);
    saveCart();
}

function cartSubtotal() {
    return cart.reduce((sum, item) => {
        return sum + safeNumber(item.price) * safeInteger(item.quantity);
    }, 0);
}

function cartCount() {
    return cart.reduce((sum, item) => sum + safeInteger(item.quantity), 0);
}

function cartPayload() {
    return cart
        .map(item => ({
            id: safeInteger(item.id),
            quantity: safeInteger(item.quantity)
        }))
        .filter(item => item.id > 0 && item.quantity > 0);
}

function renderCart() {
    const itemsBox = document.getElementById("cartItems");
    const cartCountEl = document.getElementById("cartCount");
    const mobileCountEl = document.getElementById("mobileCartCount");
    const subtotalEl = document.getElementById("cartSubtotal");
    const mobileTotalEl = document.getElementById("mobileCartTotal");

    if (!itemsBox) return;

    if (cart.length === 0) {
        itemsBox.innerHTML = `
            <div class="cart-empty">
                <h4>Your cart is empty</h4>
                <p>Add wholesale products to begin an order.</p>
            </div>
        `;
    } else {
        itemsBox.innerHTML = cart.map(item => {
            const id = safeInteger(item.id);
            const name = escapeHTML(item.name);
            const price = safeNumber(item.price);
            const quantity = safeInteger(item.quantity);

            return `
                <div class="cart-item">
                    <div>
                        <strong>${name}</strong>
                        <p>$${price.toFixed(2)} x ${quantity}</p>
                    </div>

                    <div class="qty-controls">
                        <button type="button" onclick="updateQuantity(${id}, -1)">-</button>
                        <span>${quantity}</span>
                        <button type="button" onclick="updateQuantity(${id}, 1)">+</button>
                    </div>

                    <button class="remove-btn" type="button" onclick="removeItem(${id})">
                        Remove
                    </button>
                </div>
            `;
        }).join("");
    }

    const subtotal = cartSubtotal().toFixed(2);
    const count = cartCount();

    if (cartCountEl) cartCountEl.textContent = count;
    if (mobileCountEl) mobileCountEl.textContent = count;
    if (subtotalEl) subtotalEl.textContent = subtotal;
    if (mobileTotalEl) mobileTotalEl.textContent = subtotal;
}

function openCart() {
    document.getElementById("cartDrawer")?.classList.add("open");
    document.getElementById("cartOverlay")?.classList.add("open");
}

function closeCart() {
    document.getElementById("cartDrawer")?.classList.remove("open");
    document.getElementById("cartOverlay")?.classList.remove("open");
}

document.addEventListener("DOMContentLoaded", renderCart);

function renderCheckoutReview() {
    const checkoutItems = document.getElementById("checkoutItems");
    const checkoutTotal = document.getElementById("checkoutTotal");

    if (!checkoutItems || !checkoutTotal) return;

    if (cart.length === 0) {
        checkoutItems.innerHTML = `
            <div class="cart-empty">
                <h4>No items in cart</h4>
                <p>Go back to products and add items first.</p>
            </div>
        `;
        checkoutTotal.textContent = "0.00";
        return;
    }

    checkoutItems.innerHTML = cart.map(item => {
        const name = escapeHTML(item.name);
        const price = safeNumber(item.price);
        const quantity = safeInteger(item.quantity);

        return `
            <div class="review-item">
                <div>
                    <strong>${name}</strong>
                    <p>${quantity} pcs x $${price.toFixed(2)}</p>
                </div>
                <strong>$${(quantity * price).toFixed(2)}</strong>
            </div>
        `;
    }).join("");

    checkoutTotal.textContent = cartSubtotal().toFixed(2);
}

const checkoutForm = document.getElementById("checkoutForm");

if (checkoutForm) {
    checkoutForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const message = document.getElementById("checkoutMessage");
        const formData = new FormData(checkoutForm);
        const payloadCart = cartPayload();

        if (payloadCart.length === 0) {
            message.textContent = "Your cart is empty.";
            message.className = "form-message error";
            return;
        }

        const payload = {
            business_name: formData.get("business_name"),
            name: formData.get("name"),
            phone: formData.get("phone"),
            address: formData.get("address"),
            payment_method: formData.get("payment_method"),
            notes: formData.get("notes"),
            cart: payloadCart
        };

        message.textContent = "Creating order...";
        message.className = "form-message";

        try {
            const placeOrderUrl = checkoutForm.dataset.placeOrderUrl || "/place-order";
            const response = await fetch(placeOrderUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (!result.success) {
                message.textContent = result.message || "Order failed.";
                message.className = "form-message error";
                return;
            }

            localStorage.removeItem("speedvolt_cart");
            cart = [];

            window.location.href = result.invoice_url;

        } catch (error) {
            message.textContent = "Something went wrong. Please try again.";
            message.className = "form-message error";
        }
    });
}

document.addEventListener("DOMContentLoaded", renderCheckoutReview);
