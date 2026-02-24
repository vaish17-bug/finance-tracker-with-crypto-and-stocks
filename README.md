# finance-tracker-with-crypto-and-stocks
SmartFinance is a Flask-based personal finance tracker that allows users to securely manage income and expenses, set budgets, track savings goals, and visualize financial data through interactive dashboards.  Built using Python, Flask, SQLAlchemy, and Bootstrap with a modular architecture and RESTful design principles.

SmartFinance – Personal Finance Tracker

SmartFinance is a full-stack web application built with Flask that helps users track income and expenses, manage budgets, and visualize financial data through an interactive dashboard.

🚀 Features

User authentication (secure password hashing)

Add / edit / delete transactions

Categorize income and expenses

Dashboard with financial summaries

Monthly budget tracking

Savings goal monitoring

Export transactions (CSV / Excel)

🛠 Tech Stack

Backend: Python, Flask, SQLAlchemy

Frontend: HTML, CSS, Bootstrap

Database: SQLite / MySQL


Data Processing: Pandas

Charts: Chart.js

📂 Project Structure
smartfinance/
│── app/
│   ├── auth/
│   ├── main/
│   ├── models.py
│   └── templates/
│── migrations/
│── config.py
│── run.py
│── requirements.txt

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/vaish17-bug/smartfinance.git
cd smartfinance
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Initialize Database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
5️⃣ Run Application

python run.py

App runs at:

http://127.0.0.1:5000/

📊 Future Improvements

🔐 Security

Session-based authentication
Protect routes using Flask-Login
Multi-currency support

API integration for stock/crypto tracking

AI-based spending insights

Email reminders for budgets

📌 Learning Outcomes

This project demonstrates:

RESTful architecture

Database modeling & migrations

Authentication & authorization

CRUD operations

Data visualization
