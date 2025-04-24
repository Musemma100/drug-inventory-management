from flask import Flask, render_template, request, redirect
from models.drug import Drug
from models.inventory import Inventory
from models.user import Pharmacist
from datetime import datetime

app = Flask(__name__)
inventory = Inventory()
current_user = None

@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        if role == 'Pharmacist':
            current_user = Pharmacist(username)
        else:
            current_user = User(username)
        return redirect('/')
    return render_template('login.html')


@app.route('/')
def index():
    if not current_user:
        return redirect('/login')
    return render_template('index.html', drugs=inventory.all_drugs(), user=current_user)



@app.route('/add_drug', methods=['GET', 'POST'])
def add_drug():
    if not current_user:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        drug_type = request.form['type']
        quantity = int(request.form['quantity'])
        batch = request.form['batch']
        expiry = datetime.strptime(request.form['expiry'], "%Y-%m-%d").date()
        drug = Drug(name, drug_type, quantity, batch, expiry)
        inventory.add_drug(drug)
        return redirect('/')
        
    return render_template('add_drug.html', user=current_user)



@app.route('/stock_out', methods=['POST'])
def stock_out():
    batch = request.form['batch']
    amount = int(request.form['amount'])
    drug = inventory.get_drug(batch)
    if drug:
        try:
            drug.stock_out(amount)
        except ValueError as e:
            return str(e)
    return redirect('/')


@app.route('/low_stock')
def low_stock():
    if not current_user:
        return redirect('/login')

    low_stock_drugs = [drug for drug in inventory.all_drugs() if drug.is_low_stock()]
    return render_template('low_stock.html', low_stock_drugs=low_stock_drugs, user=current_user)


@app.route('/stock_in', methods=['GET', 'POST'])
def stock_in():
    if not current_user:
        return redirect('/login')

    if request.method == 'POST':
        batch = request.form['batch']
        amount = int(request.form['amount'])
        drug = inventory.get_drug(batch)
        if drug:
            drug.stock_in(amount)
            return redirect('/')
        else:
            return "Drug not found"
        
    return render_template('stock_in.html', user=current_user, drugs=inventory.all_drugs())



if __name__ == '__main__':
    app.run(debug=True)
