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
            <body style="background-color: #f0f4f8; font-family: monospace; text-align: center; padding-top: 50px;">
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
            <body style="background-color: #f0f4f8; font-family: monospace; text-align: center; padding: 20px;">
                <h2 style="color: #2c3e50;">Add a New Transaction</h2>
                <form action="/add_transaction" method="POST" style="background-color: ; padding: 20px; border-radius: 10px; display: inline-block; font-family: monospace;">
                    <input name="amount" type="number" step="1" placeholder="Amount" style="margin: 5px; padding: 5px; font-family: monospace;"><br>
                    <input name="category" type="text" placeholder="Category" style="margin: 5px; padding: 5px; font-family: monospace;"><br>
                    <input name="date" type="date" placeholder="Date" style="margin: 5px; padding: 5px; font-family: monospace;"><br>
                    <input name="type" type="text" placeholder="Type" style="margin: 5px; padding: 5px; font-family: monospace;"><br>
                    <input name="description" type="text" placeholder="Description" style="margin: 5px; padding: 5px; font-family: monospace;"><br>
                    <button type="submit" style="background-color: #2980b9; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-family: monospace;">Add Transaction</button>
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
            <body style="background-color: #f0f4f8; font-family: monospace; text-align: center; padding-top: 50px;">
                <h1 style="color: #2c3e50;">You've commited! One step closer towards financial freedom!</h1>
                <p style="font-size: 18px; color: #34495e;">To add more transactions, go to <a href="/add_transactions_page" style="color: #2980b9; text-decoration: none;">Add Transactions</a>.</p>
                <p style="font-size: 18px; color: #34495e;">Go to <a href="/summary" style="color: #2980b9; text-decoration: none;">Summary</a> to check your summary.</p>
            </body>
        </html>
    '''


@app.route('/summary')
def summary():
    conn = sqlite3.connect('finance.db')
    income = conn.execute("SELECT SUM(amount) FROM transactions WHERE LOWER(type)='income'").fetchone()
    expense = conn.execute("SELECT SUM(amount) FROM transactions WHERE LOWER(type)='expense'").fetchone()
    income_value = income[0] or 0
    expense_value = expense[0] or 0
    balance = income_value - expense_value
    transactions = conn.execute("SELECT * FROM transactions").fetchall()
    conn.close()
    # Tip logic
    if balance > 0:
        tip = "Nice, you're in the green! Keep saving!"
    elif balance < 0:
        tip = "You're spending more than you earn! Cut back!"
    else:
        tip = "You're breaking even. Try to save a bit."

    # Start the table with headers
    table_html = '''
        <table style="border-collapse: collapse; margin: 20px auto;">
            <tr>
                <th style="border: 1px solid #34495e; padding: 8px; color: #34495e;">Amount</th>
                <th style="border: 1px solid #34495e; padding: 8px; color: #34495e;">Category</th>
                <th style="border: 1px solid #34495e; padding: 8px; color: #34495e;">Date</th>
                <th style="border: 1px solid #34495e; padding: 8px; color: #34495e;">Type</th>
                <th style="border: 1px solid #34495e; padding: 8px; color: #34495e;">Description</th>
            </tr>
    '''

    # Add a row for each transaction
    for transaction in transactions:
        table_html += f'''
            <tr>
                <td style="border: 1px solid #34495e; padding: 8px; color: #34495e;">{transaction[0]}</td>
                <td style="border: 1px solid #34495e; padding: 8px; color: #34495e;">{transaction[1]}</td>
                <td style="border: 1px solid #34495e; padding: 8px; color: #34495e;">{transaction[2]}</td>
                <td style="border: 1px solid #34495e; padding: 8px; color: #34495e;">{transaction[3]}</td>
                <td style="border: 1px solid #34495e; padding: 8px; color: #34495e;">{transaction[4]}</td>
            </tr>
        '''

    # Close the table
    table_html += '''
        </table>
    '''

    # Return with tip logic
    return f'''
        <html>
            <head>
                <title>Transaction Added!</title>
             </head>
            <body style="background-color: #f0f4f8; font-family: monospace; text-align: center; padding-top: 50px;">
                <h1 style="color: #2c3e50;">Ooooh a summary! Let's see how you did.</h1>
                <p style="font-size: 18px; color: #34495e;">Income: ${income_value}</p>
                <p style="font-size: 18px; color: #34495e;">Expenses: ${expense_value}</p>
                <p style="font-size: 18px; color: #34495e;">Balance: ${balance}</p>
                <p style="font-size: 18px; color: #34495e;">{tip}</p>
                {table_html}
                <p style="font-size: 18px; color: #34495e;">To add more transactions, go to <a href="/add_transactions_page" style="color: #2980b9; text-decoration: none;">Add Transactions</a>.</p>
            </body>
        </html>
    '''



if __name__ == '__main__':
    app.run(debug=True)
