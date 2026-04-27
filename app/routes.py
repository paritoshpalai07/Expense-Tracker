from app import app, db
from app.forms import LoginForm, RegisterForm, ExpenseForm, IncomeForm
from app.models import User, Expense, Income
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from wtforms import ValidationError
import sqlalchemy as sa
from urllib.parse import urlsplit 
from collections import defaultdict
from datetime import date

svg_list = {
    'Food & Drinks': 'images/fork-and-knife_gray.svg',
    'Travel': 'images/airplane_gray.svg',
    'Shopping': 'images/shopping-bag_gray.svg',
    'Transportation': 'images/car_gray.svg',
    'Entertainment': 'images/star_gray.svg',
    'Services': 'images/shop_gray.svg',
    'Health': 'images/heart-rate_gray.svg',
    'Home': 'images/home_gray.svg',
    'Rent': 'images/rent_gray.svg'
}



@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    stmt = sa.select(Expense).where(Expense.user_id == current_user.id).order_by(Expense.date.desc())
    pagination = db.paginate(stmt, page=page, per_page=7)
    expenses = pagination.items

    all_expenses = db.session.scalars(stmt).all()
    total_expense = float(Expense.get_total_expense(all_expenses))

    # expenses = db.session.scalars(sa.select(Expense).where(Expense.user_id==current_user.id).order_by(Expense.date.desc())).all()
    grouped_expenses = defaultdict(list)
    for expense in expenses:
        grouped_expenses[expense.date].append(expense)
    # total_expense = float(Expense.get_total_expense(expenses))

    total_food_and_drinks_amount = Expense.get_category_total(all_expenses, "Food & Drinks")
    total_travel_amount = Expense.get_category_total(all_expenses, "Travel")
    total_shopping_amount = Expense.get_category_total(all_expenses, "Shopping")
    total_transportation_amount = Expense.get_category_total(all_expenses, "Transportation")
    total_entertainment_amount = Expense.get_category_total(all_expenses, "Entertainment")
    total_services_amount = Expense.get_category_total(all_expenses, "Services")
    total_health_amount = Expense.get_category_total(all_expenses, "Health")
    total_home_amount = Expense.get_category_total(all_expenses, "Home")
    total_rent_amount = Expense.get_category_total(all_expenses, "Rent")
    total_extra_amount = Expense.get_category_total(all_expenses, 'Extra')

    print(total_rent_amount)
    income = db.session.scalars(
        sa.select(Income).where(
            Income.user_id == current_user.id and Income.date == date.today()
            )).all()
    print("income: ",income)
    total_income = Income.get_total_income(income)
    print(total_income)

    dates = [(expense.date.strftime("%B %d %Y"), expense.date.strftime("%A")) for expense in expenses]
    form = ExpenseForm()
    income_form = IncomeForm()
    if form.validate_on_submit():
        expense = Expense(
            amount=form.amount.data,
            category=form.category.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('index'))
    
    if income_form.validate_on_submit():
        income = Income(amount=income_form.income_amount.data, user_id=current_user.id)
        db.session.add(income)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template("index.html", 
                           form=form, 
                           income_form=income_form,
                           total_income=total_income,
                           grouped_expenses=grouped_expenses, 
                           dates=dates, 
                           total_expense=total_expense, 
                           total_food_and_drinks_amount=total_food_and_drinks_amount,
                           total_travel_amount=total_travel_amount,
                           total_shopping_amount=total_shopping_amount,
                           total_transportation_amount=total_transportation_amount,
                           total_entertainment_amount=total_entertainment_amount,
                           total_services_amount=total_services_amount,
                           total_health_amount=total_health_amount,
                           total_home_amount=total_home_amount,
                           total_rent_amount=total_rent_amount,
                           total_extra_amount=total_extra_amount,
                           pagination=pagination,
                           svg_list=svg_list 
                           )

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username==form.username.data)
        )

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    
    return render_template("login.html", form=form)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = db.session.scalar(sa.select(User).where(User.username==form.username.data))
        email = db.session.scalar(sa.select(User).where(User.email==form.email.data))
        if username:
            flash("The username is already taken. try another one.")
            return redirect(url_for('register'))
        if email:
            flash("We already have account with this email, try new one.")
            return redirect(url_for('register'))
        user = User(
            firstname=form.firstname.data.capitalize(),
            lastname=form.lastname.data.capitalize(),
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now registered user!")
        return redirect(url_for('index'))
    
    return render_template("register.html", form=form)

# @app.route('/add-expense/', methods=['GET', 'POST'])
# def add_expense():
#     form = ExpenseForm()
#     if form.validate_on_submit():
#         expense = Expense(
#             amount=form.amount.data,
#             category=form.category.data,
#             description=form.description.data,
#             date=form.date.data,
#             user_id=current_user.id
#         )
#         db.session.add(expense)
#         db.session.commit()
#     return redirect(url_for('index'))
