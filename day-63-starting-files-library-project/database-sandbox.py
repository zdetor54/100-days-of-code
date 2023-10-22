from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()

# with app.app_context():
#     max_id = db.session.execute(db.func.max(Book.id)).scalar()
#     new_book = Book(id=max_id+1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
#     db.session.add(new_book)
#     db.session.commit()

with app.app_context():
    result = db.session.execute(db.select(Book).order_by(Book.id.desc()))
    all_books = result.scalars()
    result_list = list(result)
    print(len(result_list))
    for book in all_books:
        print(book.id)