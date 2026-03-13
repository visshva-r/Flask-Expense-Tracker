from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4)])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Password must be at least 6 characters long.'),
        ],
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.'),
        ],
    )
    submit = SubmitField('Register')

class ExpenseForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01, message='Amount must be positive.')])
    category = SelectField('Category', choices=[('Food', 'Food'), ('Travel', 'Travel'), ('Rent', 'Rent'), ('Other', 'Other')])
    submit = SubmitField('Add Expense')
