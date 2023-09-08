from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

# Read data from CSV file
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

def read_data():
    with open('products.csv', 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

# Write data to CSV file
def write_data(data):
    fieldnames = ['Product_Name', 'Price', 'Description']
    with open('products.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Render template to display data
@app.route('/read')
def read():
    data = read_data()
    return render_template('read.html', data=data)

# Render template to add new product
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        description = request.form.get('description')

        data = read_data()
        data.append({'Product_Name': product_name, 'Price': price, 'Description': description})
        write_data(data)

        return redirect('/index')
    return render_template('write.html')

# Render template to update product price
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        new_price = request.form.get('new_price')

        data = read_data()
        for item in data:
            if item['Product_Name'] == product_name:
                item['Price'] = new_price
        write_data(data)

        return redirect('/index')
    return render_template('update.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        product_name = request.form['product_name']
        with open('products.csv', 'r') as file:
            csv_reader = csv.reader(file)
            products = list(csv_reader)
        products = [product for product in products if product[0] != product_name]
        with open('products.csv', 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(products)
        return redirect('/index')
    return render_template('delete.html')

if __name__ == '__main__':
    app.run(debug=True,port=8000)
