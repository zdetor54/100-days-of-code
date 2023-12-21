from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
API_KEY = '2e611871b539226c8cd3dc205af6708d'
API_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyZTYxMTg3MWI1MzkyMjZjOGNkM2RjMjA1YWY2NzA4ZCIsInN1YiI6IjY1MzY5NTgyMmIyMTA4MDEzZjViNzQ4YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dN1E6hiN4rYK6x-JhZ26jwdboeYN36DCrzSRZu9pO6o'
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyZTYxMTg3MWI1MzkyMjZjOGNkM2RjMjA1YWY2NzA4ZCIsInN1YiI6IjY1MzY5NTgyMmIyMTA4MDEzZjViNzQ4YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dN1E6hiN4rYK6x-JhZ26jwdboeYN36DCrzSRZu9pO6o"
}

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie.db"
db.init_app(app)

class updateRating(FlaskForm):
    rating = FloatField(label='Your rating out of 10: e.g. 7.3')
    review = StringField(label='Your Review')
    submit = SubmitField(label='Done')

class addMovie(FlaskForm):
    title = StringField(label='Movie Title')
    submit = SubmitField(label='Add Movie')

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
    db.create_all()

# with app.app_context():
#     second_movie = Movie(
#         title="Avatar The Way of Water",
#         year=2022,
#         description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#         rating=7.3,
#         ranking=9,
#         review="I liked the water.",
#         img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg" /kEiMX42a35S4blAw4KrQe3U5zNc.jpg
#     )
#     db.session.add(second_movie)
#     db.session.commit()

@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars()
    movie_list = list(movies)

    total_rank = len(movie_list)
    current_rank = total_rank

    for movie in movie_list:
        print(current_rank)
        movie.ranking = current_rank
        db.session.commit()
        current_rank -= 1


    movies = db.session.execute(db.select(Movie).order_by(Movie.ranking.desc())).scalars()
    return render_template("index.html", movies = movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():

    form = updateRating()

    movie_id = request.args.get('id')
    movie = Movie.query.get_or_404(movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', movie = movie, form = form)


@app.route('/delete')
def delete():

    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get_or_404(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods = ['POST', 'GET'])
def add():

    form = addMovie()
    if form.validate_on_submit():
        movie_title = form.title.data
        url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&include_adult=false&language=en-US&page=1"
        response = requests.get(url=url, headers=headers)
        data = response.json()

        print(data)

        return render_template('select.html', movies  = data['results'])
    return render_template('add.html', form = form)

@app.route('/get_movie_details')
def get_movie_details():
    movie_id = request.args.get('id')
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    response = requests.get(url=url, headers=headers)
    data = response.json()
    current_movie = Movie(
                title=data["original_title"],
                year=data["release_date"][:4],
                description= data["overview"],
                img_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
            )
    db.session.add(current_movie)
    db.session.commit()

    # inserted_movie = Movie.query.filter_by(title=data["original_title"]).first()
    return redirect(url_for('edit', id = current_movie.id))

if __name__ == '__main__':
    app.run(debug=True)
