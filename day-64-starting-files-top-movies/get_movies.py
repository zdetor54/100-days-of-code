from flask import Flask, render_template, redirect, url_for, request

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie.db"
db.init_app(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.String)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String)
    img_url = db.Column(db.String)

with app.app_context():
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars()
    movie_list = list(movies)
    print(movie_list)

    total_rank = len(movie_list)
    current_rank = total_rank

    for movie in movie_list:
        print(current_rank)
        movie.ranking = current_rank
        db.session.commit()
        current_rank -= 1