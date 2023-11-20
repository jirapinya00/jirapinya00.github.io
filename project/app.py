from flask import Flask, render_template, request, redirect, url_for
import qrcode
import os

app = Flask(__name__, template_folder='templates')

# สร้างตัวแปรสำหรับเก็บรายการอาหาร
menu_items = [
    {'id': 1, 'name': 'Burger'},
    {'id': 2, 'name': 'Pizza'},
    {'id': 3, 'name': 'Salad'},
    # เพิ่มรายการอาหารต่อไปนี้
]

# สร้างรายการคำสั่งจากลูกค้า
customer_orders = []

# สร้างรายการคำสั่งจากแอดมิน
admin_orders = []

@app.route('/')
def index():
    return render_template('index.html', menu_items=menu_items)

@app.route('/order', methods=['POST'])
def order():
    food_item_id = int(request.form.get('food_item'))
    food_item = next((item for item in menu_items if item['id'] == food_item_id), None)

    if food_item:
        # สร้าง QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"Order: {food_item['name']}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # ตรวจสอบว่าไดเรกทอรี 'static' มีอยู่หรือไม่
        if not os.path.exists('static'):
            os.makedirs('static')

        # บันทึก QR code ไว้ในไดเรกทอรี static
        img.save('static/customer_order_qr.png')

        # เพิ่มรายการคำสั่งลูกค้าใน customer_orders
        customer_orders.append({'name': food_item['name']})

        return render_template('customer_order.html', food_item=food_item)

@app.route('/admin')
def admin():
    return render_template('admin.html', orders=admin_orders)

@app.route('/admin/generate_qr', methods=['POST'])
def generate_qr():
    # สร้าง QR code สำหรับแอดมิน
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("Admin Page")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # บันทึก QR code ไว้ในไดเรกทอรี static
    img.save('static/admin_qr.png')

    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
