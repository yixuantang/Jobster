from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, BooleanField, SubmitField
from wtforms import validators as v, ValidationError

'''
You can change the form fields here. You will also have to go into the jinja template to display them, but that's pretty straight forward.
Here's some documentation:
	http://wtforms.readthedocs.io/en/latest/crash_course.html
	https://www.tutorialspoint.com/flask/flask_wtf.htm

, v.Length(min=4, max=25)
'''


class LoginForm(FlaskForm):
    act_type = RadioField('', choices=[('student', 'student'), ('company', 'company')], default='student')
    username = StringField("Username", [v.DataRequired('Please enter your username')])
    password = PasswordField("Password", [v.DataRequired('Please enter your password')])
    remember = BooleanField('Remember me.')
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    act_type = RadioField('User tyle', choices=[('student', 'student'), ('company', 'company')], default='student')
    name = StringField("Name")
    username = StringField("Username", [v.DataRequired('Please specify a username')])
    password = PasswordField("Password", [v.DataRequired('Please specify a password')])
    submit = SubmitField("Register")


class ApplicationForm(FlaskForm):
<<<<<<< HEAD
	email_phone = StringField("Email/Phone")
	submit = SubmitField("Apply")

class UpdateForm(FlaskForm):
	phone = StringField("your phone")
	email = StringField("your email")
	university = StringField("your university")
	GPA = StringField("your GPA")
	major = StringField("your major")
	interests = StringField("your interest")
	qualifications = StringField("your qualifications")
	privacy_setting = StringField("your qualifications")
	#privacy_setting = RadioField("your privacy setting", [('public', 'Public'), ('friendly public', 'Friends')])
	# resume = StringField("your university")
=======
    email_phone = SelectField("Contact via", choices=[('email', 'Email'), ('phone', 'Phone')])
    submit = SubmitField("Apply")


class UpdateForm(FlaskForm):
    phone = StringField("your phone")
    email = StringField("your email")
    university = StringField("your university")
    major = StringField("your major")
    GPA = StringField("your GPA")
    interest = StringField("your interest")
    qualifications = StringField("your qualifications")
    resume = StringField("your resume")
    privacysetting = SelectField("your privacy setting", choices=[('public', 'Public'), ('friendly public', 'Friends')])
    submit = SubmitField("Update")

class UpdateForm_com(FlaskForm):
	location = StringField("company location")
	industry = StringField("company industry")
>>>>>>> 61a13e913cdc05d5e0d2365cce56fadd6c2dea7a
	submit = SubmitField("Update")

class UpdateForm_com(FlaskForm):
	location = StringField("company location")
	industry = StringField("company industry")
	submit = SubmitField("Update")

class PostJob(FlaskForm):
<<<<<<< HEAD
	aid = StringField("aid")
	joblocation = StringField("job location")
	title = StringField("job title")
	salary = StringField("salary")
	bk = StringField("back ground requirment")
	description = StringField("detailed description")
	submit = SubmitField("Post")
=======
    joblocation = StringField("Job location")
    title = StringField("job title")
    salary = StringField("salary")
    bk = StringField("Background requirement")
    description = StringField("Details")
    submit = SubmitField("Post")
>>>>>>> 61a13e913cdc05d5e0d2365cce56fadd6c2dea7a

class SearchForm(FlaskForm):
	query = StringField("Search")
	submit = SubmitField("Search")
