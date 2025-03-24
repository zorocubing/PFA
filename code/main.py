from flask import Flask, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('finance.db')
conn.execute('''CREATE TABLE IF NOT EXISTS transactions
                (amount REAL, category TEXT, date TEXT, type TEXT, description TEXT)''')
conn.commit()
conn.close()

@app.route('/')
def message():
    return '''
        <html>
            <head>
                <title>Welcome to PFA</title>
            </head>
            <body style="background-color: #f0f4f8; font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
                <h1 style="color: #2c3e50;">Welcome to Personal Finance App (PFA)</h1>
                <p style="font-size: 18px; color: #34495e;">To get started, go to <a href="/add_transactions_page" style="color: #2980b9; text-decoration: none;">Add Transactions</a>.</p>
            </body>
        </html>
    '''

@app.route('/add_transactions_page')
def form():
    return '''
        <html>
            <head>
                <title>Add Transaction</title>
            </head>
            <body style="background-color: #f0f4f8; font-family: Arial, sans-serif; text-align: center; padding: 20px;">
                <h2 style="color: #2c3e50;">Add a New Transaction</h2>
                <form action="/add_transaction" method="POST" style="background-color: white; padding: 20px; border-radius: 10px; display: inline-block;">
                    <input name="amount" type="number" step="1" placeholder="Amount" style="margin: 5px; padding: 5px;"><br>
                    <input name="category" type="text" placeholder="Category" style="margin: 5px; padding: 5px;"><br>
                    <input name="date" type="date" placeholder="Date" style="margin: 5px; padding: 5px;"><br>
                    <input name="type" type="text" placeholder="Type" style="margin: 5px; padding: 5px;"><br>
                    <input name="description" type="text" placeholder="Description" style="margin: 5px; padding: 5px;"><br>
                    <button type="submit" style="background-color: #2c3e50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Add Transaction</button>
                </form>
            </body>
        </html>
    '''

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.form
    conn = sqlite3.connect('finance.db')
    conn.execute("INSERT INTO transactions (amount, category, date, type, description) VALUES (?, ?, ?, ?, ?)",
                 (data['amount'], data['category'], data['date'], data['type'], data['description']))
    conn.commit()
    conn.close()
    return '''
        <html>
            <head>
                <title>Transaction Added!</title>
            </head>
            <body style="background-color: #f0f4f8; font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
                <h1 style="color: #2c3e50;">You've commited! One step closer towards financial freedom!</h1>
                <p style="font-size: 18px; color: #34495e;">To add more transactions, go to <a href="/add_transactions_page" style="color: #2980b9; text-decoration: none;">Add Transactions</a>.</p>
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
