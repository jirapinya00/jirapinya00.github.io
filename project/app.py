from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data - Replace this with a database in a real-world application
inventory = {
    1: {"name": "Item1", "price": 10.99, "quantity": 20},
    2: {"name": "Item2", "price": 5.99, "quantity": 15},
    3: {"name": "Item3", "price": 8.50, "quantity": 10},
}

cart = {}


@app.route('/')
def index():
    return render_template('index.html', inventory=inventory, cart=cart)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 0))
    if 1 <= quantity <= inventory[product_id]['quantity']:
        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            cart[product_id] = {
                'name': inventory[product_id]['name'],
                'price': inventory[product_id]['price'],
                'quantity': quantity,
            }
        inventory[product_id]['quantity'] -= quantity

    return redirect(url_for('index'))


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if product_id in cart:
        inventory[product_id]['quantity'] += cart[product_id]['quantity']
        del cart[product_id]

    return redirect(url_for('index'))


@app.route('/checkout')
def checkout():
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('checkout.html', cart=cart, total=total)


if __name__ == '__main__':
    app.run(debug=True)
