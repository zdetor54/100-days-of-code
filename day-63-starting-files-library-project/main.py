import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from flask_bootstrap import Bootstrap5

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

class editRatingForm(FlaskForm):
    rating = FloatField()
    submit = SubmitField(label='Change Rating')

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    result = db.session.execute(db.select(Book))
    all_books = result.scalars()
    return render_template("index.html", books = all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        new_book = {
            "title": request.form["title"],
            "author": request.form["author"],
            "rating": request.form["rating"]
        }
        max_id = db.session.execute(db.func.max(Book.id)).scalar()
        new_book = Book(id=max_id+1, title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        # all_books.append(new_book)
        # print(all_books)
        # print(len(all_books))
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/edit", methods=["POST", "GET"])
def edit():
    id = request.args.get('id')
    book = db.session.query(Book).filter(Book.id == id).all()

    edit_form = editRatingForm()
    edit_form.rating.hide_label = True
    if edit_form.validate_on_submit():
        book_to_update = db.get_or_404(Book,id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit.html", book = book[0], form = edit_form)

@app.route('/delete')
def delete():
    id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

