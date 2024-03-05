from wtforms import Form, StringField, DecimalField, IntegerField, TextAreaField, PasswordField, validators

class RegisterForm(Form):
    """
    Form class used for user registration.

    Attributes:
    - name: StringField for user's full name (1-50 characters)
    - username: StringField for user's username (4-25 characters)
    - email: StringField for user's email (6-50 characters)
    - password: PasswordField for user's password (required) and confirmation (must match)
    - confirm: PasswordField for confirming user's password
    """

    name = StringField('Full Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

class SendMoneyForm(Form):
    """
    Form class used for sending money.

    Attributes:
    - username: StringField for recipient's username (4-25 characters)
    - amount: StringField for amount of money to send (1-5 characters)
    """

    username = StringField('Username', [validators.Length(min=4, max=25)])
    amount = StringField('Amount', [validators.Length(min=1, max=5)])

class BuyForm(Form):
    """
    Form class used for buying.

    Attributes:
    - amount: StringField for amount to buy (1-3 characters)
    """

    amount = StringField('Amount', [validators.Length(min=1, max=3)])
