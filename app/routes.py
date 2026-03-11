from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User, Expense
from .forms import LoginForm, RegisterForm, ExpenseForm
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import csv
import io
from flask import Response

# FIX 1: Set Matplotlib to headless 'Agg' mode to prevent Flask from crashing
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created!')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(amount=form.amount.data, category=form.category.data, owner=current_user)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('main.dashboard'))

    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    generate_chart(expenses)
    return render_template('dashboard.html', form=form, expenses=expenses)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

def generate_chart(expenses):
    categories = {}
    for exp in expenses:
        categories[exp.category] = categories.get(exp.category, 0) + exp.amount

    plt.clf()
    path = os.path.join('app', 'static', 'chart.png')
    
    # FIX 3: Auto-create the static directory so you never get a FileNotFoundError
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # FIX 2: Prevent the app from crashing if a new user has 0 expenses
    if not categories:
        plt.pie([1], labels=["No Expenses Yet"], colors=["#e0e0e0"])
    else:
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        
    plt.savefig(path)

@main.route('/export')
@login_required
def export_csv():
    # Get the user's expenses
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    # Create a virtual file in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write the top row (Headers)
    writer.writerow(['Category', 'Amount'])

    # Write the actual data
    for exp in expenses:
        writer.writerow([exp.category, exp.amount])

    # Package it up and force the browser to download it
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=my_expenses.csv'
    return response