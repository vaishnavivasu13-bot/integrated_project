from flask import Flask, render_template, request, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'glamcart_secret_key'

# Database initialize
def init_db():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        image TEXT,
        category TEXT
    )''')
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        products = [
            ('Lipstick - Red', 299, 'lipstick.jpg', 'Lips'),
            ('Foundation - Matte', 599, 'foundation.jpg', 'Face'),
            ('Mascara', 399, 'mascara.jpg', 'Eyes'),
            ('Kajal', 149, 'kajal.jpg', 'Eyes'),
            ('Nail Polish - Pink', 99, 'nailpolish.jpg', 'Nails'),
        ]
        c.executemany("INSERT INTO products (name, price, image, category) VALUES (?,?,?,?)", products)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    pid = str(data['product_id'])
    cart = session.get('cart', {})
    cart[pid] = cart.get(pid, 0) + 1
    session['cart'] = cart
    return jsonify({'status': 'ok', 'count': sum(cart.values())})

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    items = []
    total = 0
    if cart:
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        for pid, qty in cart.items():
            c.execute("SELECT * FROM products WHERE id=?", (pid,))
            p = c.fetchone()
            if p:
                items.append({'id': p[0], 'name': p[1], 'price': p[2], 'qty': qty, 'subtotal': p[2]*qty})
                total += p[2]*qty
        conn.close()
    return render_template('cart.html', items=items, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        session.pop('cart', None)
        return render_template('thankyou.html')
    return render_template('checkout.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '_main_':
    app.run(debug=True, port=5000)