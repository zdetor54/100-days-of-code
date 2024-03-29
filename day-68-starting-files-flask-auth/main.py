from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)


# CREATE TABLE IN DB
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
 
 
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods = ['POST', 'GET'])
def register():

    if request.method == 'POST':
        new_user = User(
            email = request.form.get('email'),
            password = generate_password_hash(password = request.form.get('password'), method='pbkdf2:sha256', salt_length=8),
            name = request.form.get('name')
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            login_user(new_user)
            return redirect('secrets')
        except:
            flash('The user already exists.')
            return render_template("register.html")
    return render_template("register.html")


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(password)

        result = User.query.filter_by(email=email).first()
        # result = db.session.execute(db.select(User).where(User.email == email))

        try:
            if check_password_hash(result.password, password):
                login_user(result)
                return redirect('secrets')
            else:
                flash('Password incorrect, please try again.')
                return render_template(("login.html"))
        except:
            flash("That email does not exist, please try again.")
            return render_template(("login.html"))

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')



@app.route('/download')
@login_required
def download():
    return send_from_directory('static','files/cheat_sheet.pdf')


if __name__ == "__main__":
    app.run(debug=True, port=5002)
