from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from app import db, login

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin,db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64))
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    incomes: so.WriteOnlyMapped['Income'] = so.relationship(back_populates='user')
    expenses: so.WriteOnlyMapped['Expense'] = so.relationship(back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    

class Income(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[float] = so.mapped_column(nullable=False)
    # category: so.Mapped[str] = so.mapped_column(sa.String(128))
    date: so.Mapped[datetime] = so.mapped_column(default=lambda: date.today())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    user: so.Mapped[User] = so.relationship(back_populates='incomes')

    @staticmethod
    def get_total_income(incomes):
        income_list = [income.amount for income in incomes]
        return sum(income_list)
    
    def __repr__(self):
        return '<Income {}>'.format(self.amount)
    
class Expense(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    amount: so.Mapped[int] = so.mapped_column(nullable=False)
    category: so.Mapped[str] = so.mapped_column(sa.String(128))
    description: so.Mapped[str] = so.mapped_column(sa.Text)
    date: so.Mapped[datetime] = so.mapped_column(default= lambda: date.today())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    user: so.Mapped[User] = so.relationship(back_populates='expenses')

    @staticmethod
    def get_total_expense(expenses):
        expense_list = [expense.amount for expense in expenses]
        return sum(expense_list)
    
    @staticmethod
    def get_category_total(expenses, category):
        match(category):
            case "Food & Drinks":
                expense_list = [expense.amount for expense in expenses if expense.category == category]
                return float(sum(expense_list))
            case "Travel":
                expense_list = [expense.amount for expense in expenses if expense.category == category]
                return float(sum(expense_list))
            case "Shopping":
                expense_list = [expense.amount for expense in expenses if expense.category == category]
                return float(sum(expense_list))
            case "Transportation":
                expense_list = [expense.amount for expense in expenses if expense.category == category]
                return float(sum(expense_list))
            case "Entertainment":
                expense_list = [expense.amount for expense in expenses if expense.category == category]
                return float(sum(expense_list))
            case "Services":
                expense_list = [expense.amount for expense in expenses if expense.category == category]
                return float(sum(expense_list))
            case "Health":
                expense_list = [expense.amount for expense in expenses if expense.category == category]
                return float(sum(expense_list))
            case "Home":
                expense_list = [expense.amount for expense in expenses if expense.category == category]
                return float(sum(expense_list))

    def __repr__(self):
        return '<Expense {}>'.format(self.amount)