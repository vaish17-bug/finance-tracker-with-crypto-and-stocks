from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import yfinance as yf
import requests
import os

app = Flask(__name__)

import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",       # or your MySQL server
    user="root",            # your MySQL username
    password="root",# your MySQL password
    database="f_track"   # your database name
)

cursor = db.cursor(dictionary=True)  # dictionary=True gives column names in results


            

@app.route('/')
def index():
    cursor = db.cursor()

    # Total Income
    cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE type = 'Income'")
    total_income = cursor.fetchone()[0]

    # Total Expenses
    cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE type = 'Expense'")
    total_expenses = cursor.fetchone()[0]

    # Net Savings
    net_savings = total_income - total_expenses

    # Total Investment Value
    cursor.execute("SELECT IFNULL(SUM(current_value), 0) FROM investments")
    total_investment_value = cursor.fetchone()[0]

    # Profit/Loss
    cursor.execute("SELECT IFNULL(SUM(current_value - amount), 0) FROM investments")
    investment_profit_loss = cursor.fetchone()[0]

    return render_template(
        'index.html',
        total_income=total_income,
        total_expenses=total_expenses,
        net_savings=net_savings,
        total_investment_value=total_investment_value,
        investment_profit_loss=investment_profit_loss
    )



@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    cursor = db.cursor(dictionary=True)

    # Fetch all goals (to show in dropdown)
    cursor.execute("SELECT id, goal_name FROM goals")
    goals = cursor.fetchall()

    if request.method == 'POST':
        type_ = request.form['type']
        category = request.form['category']
        amount = float(request.form['amount'])
        date = request.form['date']
        notes = request.form['notes']
        goal_id = request.form.get('goal_id')  # optional

        if goal_id == "" or goal_id is None:  
            goal_id = None  # no goal selected

        sql = """
            INSERT INTO transactions (type, category, amount, date, notes, goal_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (type_, category, amount, date, notes, goal_id)
        cursor.execute(sql, values)
        db.commit()

        return redirect(url_for('index'))

    return render_template('add_transaction.html', goals=goals)



@app.route('/view_transactions')
def view_transactions():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT t.id, t.type, t.category, t.amount, t.date, t.notes, g.goal_name FROM transactions t LEFT JOIN goals g ON t.goal_id = g.id ORDER BY t.date DESC")
    transactions = cursor.fetchall()
    return render_template('view_transactions.html', transactions=transactions)

  
@app.route('/add_investment', methods=['GET', 'POST'])
def add_investment():
    if request.method == 'POST':
        asset = request.form['asset']
        category = request.form['category']
        amount = float(request.form['amount'])
        current_value = float(request.form['current_value'])
        purchase_date = request.form['purchase_date']
        notes = request.form['notes']

        cursor = db.cursor()
        sql = """
            INSERT INTO investments (asset, category, amount, current_value, purchase_date, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (asset, category, amount, current_value, purchase_date, notes)
        cursor.execute(sql, values)
        db.commit()

        return redirect(url_for('index'))
    return render_template('add_investment.html')


@app.route('/view_investments')
def view_investments():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM investments ORDER BY purchase_date DESC")
    investments = cursor.fetchall()
    return render_template('view_investments.html', investments=investments)

  
@app.route('/goal_tracker', methods=['GET', 'POST'])
def goal_tracker():
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        goal_name = request.form['goal_name']
        target_amount = float(request.form['target_amount'])
        current_amount = float(request.form['current_amount'])
        deadline = request.form['deadline']
        notes = request.form['notes']
        progress = round((current_amount / target_amount) * 100, 2) if target_amount else 0

        sql = """
            INSERT INTO goals (goal_name, target_amount, current_amount, deadline, notes, progress)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (goal_name, target_amount, current_amount, deadline, notes, progress)
        cursor.execute(sql, values)
        db.commit()

        return redirect(url_for('goal_tracker'))

    # GET → Fetch all saved goals
    cursor.execute("SELECT * FROM goals ORDER BY deadline ASC")
    goals = cursor.fetchall()

    return render_template('goal_tracker.html', goals=goals)



@app.route('/stock_market')
def stock_market():
    stock_symbols = ['AAPL', 'GOOG', 'AMZN']
    stock_data = {}

    for symbol in stock_symbols:
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")
        if not stock_info.empty:
            stock_data[symbol] = round(stock_info['Close'].iloc[-1], 2)  # rounded for cleaner display

    return render_template('stock_market.html', stock_data=stock_data)


@app.route('/cryptocurrency')
def cryptocurrency():
    crypto_symbols = ['bitcoin', 'ethereum', 'dogecoin']
    crypto_data = {}
    for symbol in crypto_symbols:
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=inr'
        response = requests.get(url)
        data = response.json()
        crypto_data[symbol] = data[symbol]['inr']
    return render_template('cryptocurrency.html', crypto_data=crypto_data)

if __name__ == '__main__':
    app.run(debug=True)
