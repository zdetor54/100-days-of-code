from flask_bootstrap import Bootstrap4, Bootstrap5
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
import os

SECRET_KEY = os.urandom(32)

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
bootstrap = Bootstrap5(app)

app.config['SECRET_KEY'] = SECRET_KEY


class myForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=120)])
    submit = SubmitField(label='Log In')


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = myForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form.email.data)
            return render_template('success.html')
        else:
            return render_template('denied.html')
    else:
        return render_template('login.html', form=form)


# else:
#     return "<h1>To be continued</h1>"


if __name__ == '__main__':
    app.run(debug=True)

import os

# Set an environment variable
os.environ['MY_VARIABLE'] = 'Hello, World!'

# Access the environment variable
my_variable = os.environ['MY_VARIABLE']
print(my_variable)
