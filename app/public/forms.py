from flask_wtf import FlaskForm
from wtforms import StringField, TelField, TextAreaField, EmailField, IntegerField, SubmitField
from wtforms.validators import Length, Email, DataRequired


class ShippingDetailsForm(FlaskForm):
    amount = IntegerField('Amount')
    phone = TelField('Phone Number', validators=(DataRequired(), Length(min=10, max=40)))
    email = EmailField('Email', validators=(DataRequired(), Length(min=10, max=40), Email()))
    address = StringField('Address', validators=(DataRequired(), Length(min=10, max=40)))
    firstname = StringField('First Name', validators=(DataRequired(), Length(min=2)))
    lastname = StringField('Last Name', validators=(DataRequired(), Length(min=2)))
    city = StringField('City', validators=(DataRequired(), Length(min=2, max=40)))
    state = StringField('State', validators=(DataRequired(), Length(min=3, max=40)))
    description = TextAreaField('Description', validators=(DataRequired(), Length(max=200)))
    submit = SubmitField('Pay', id="submit")