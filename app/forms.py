from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, EmailField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In') 

class RegisterForm(FlaskForm):
    firstname = StringField("First Name:", validators=[DataRequired()])
    lastname = StringField("Last Name:", validators=[DataRequired()])
    username = StringField("Username:", validators=[DataRequired()])
    email = EmailField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ExpenseForm(FlaskForm):
    amount = IntegerField('Amount:', validators=[DataRequired()])
    category = SelectField('Category:', choices=[
        'Food & Drinks',
        'Travel',
        'Shopping',
        'Transportation',
        'Entertainment',
        'Services',
        'Health',
        'Home',
        'Rent'        
    ] ,validators=[DataRequired()])
    description = StringField("Description:", validators=[DataRequired()])
    submit = SubmitField('Add Expense')

class IncomeForm(FlaskForm):
    income_amount = IntegerField("Income Amount:", validators=[DataRequired()])
    submit = SubmitField('Add Income')

    # date = DateTimeField('Date', validators=[DataRequired()])