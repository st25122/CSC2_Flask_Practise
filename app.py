import json

from flask import Flask, flash, redirect, render_template, request, session, url_for


app = Flask(__name__)
app.secret_key = "flower-shop-learning-key"


def load_data():
    """Load flower and add-on data from the JSON files."""
    with open("data/flowers.json", "r", encoding="utf-8") as flowers_file:
        flowers = json.load(flowers_file)

    with open("data/addons.json", "r", encoding="utf-8") as addons_file:
        addons = json.load(addons_file)

    return flowers, addons


def calculate_total(cart):
    """Calculate the total price for every item currently in the cart."""
    total = 0

    for item in cart.values():
        total += item["price"] * item["quantity"]

    return total


@app.route("/")
def index():
    """Show the home page, flowers, add-ons, and current cart."""
    flowers, addons = load_data()
    cart = session.get("cart", {})
    total = calculate_total(cart)

    return render_template(
        "index.html",
        flowers=flowers,
        addons=addons,
        cart=cart,
        total=total,
    )


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    """Add a selected flower and quantity to the session cart."""
    flowers, addons = load_data()
    flower_name = request.form.get("flower")
    quantity = int(request.form.get("quantity", 1))

    selected_flower = None
    for flower in flowers:
        if flower["name"] == flower_name:
            selected_flower = flower

    if selected_flower is None:
        flash("That flower could not be found.", "error")
        return redirect(url_for("index"))

    if quantity < 1:
        flash("Please choose a quantity of at least 1.", "error")
        return redirect(url_for("index"))

    cart = session.get("cart", {})

    if flower_name in cart:
        cart[flower_name]["quantity"] += quantity
    else:
        cart[flower_name] = {
            "quantity": quantity,
            "price": selected_flower["price"],
            "image": selected_flower["image"],
        }

    session["cart"] = cart
    session.modified = True
    flash(f"{quantity} {flower_name} added to your cart.", "success")

    return redirect(url_for("index"))


@app.route("/remove_from_cart/<item>")
def remove_from_cart(item):
    """Remove one flower type from the session cart."""
    cart = session.get("cart", {})

    if item in cart:
        cart.pop(item)
        session["cart"] = cart
        session.modified = True
        flash(f"{item} removed from your cart.", "success")
    else:
        flash("That item was not in your cart.", "error")

    return redirect(url_for("index"))


@app.route("/about")
def about():
    """Show information about the flower shop."""
    return render_template("about.html")


@app.route("/order_history")
def order_history():
    """Show a placeholder order history page."""
    return render_template("order_history.html")


@app.route("/invoices")
def invoices():
    """Show a placeholder invoices page."""
    return render_template("invoices.html")


@app.route("/test")
def test():
    """Show a simple test page for checking the Flask app."""
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
