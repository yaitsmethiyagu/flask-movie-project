from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from themoviedb import TheMovieDB
import ast

themoviedb = TheMovieDB()


class RatingEdit(FlaskForm):
    rating = StringField("Rating out of 10, eg: 7.8", validators=[DataRequired()])
    review = StringField("Review", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AddMovie(FlaskForm):
    tittle = StringField("Movie Title ", validators=[DataRequired()])
    submit = SubmitField("Submit")


db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///topmovies.db"
db.init_app(app=app)
Bootstrap(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)


def sort_movie():
    data = db.session.query(Movie).order_by(Movie.rating).all()[::-1]
    for item in data:
        item.ranking = data.index(item) + 1
        db.session.commit()


@app.route("/")
def home():

    if request.args:
        movie = db.session.query(Movie).filter(Movie.id == request.args.get("id")).first()
        db.session.delete(movie)
        db.session.commit()
        sort_movie()

        return redirect(url_for("home"))

    data = db.session.query(Movie).order_by(Movie.rating).all()
    return render_template("index.html", movies=data)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = RatingEdit()

    movie = db.session.query(Movie).filter(Movie.id == request.args.get("id")).first()

    if request.method == "POST":
        rating = request.form["rating"]
        review = request.form["review"]
        movie.rating = rating
        movie.review = review
        db.session.commit()

        sort_movie()

        return redirect(url_for("home"))

    return render_template("edit.html", movie=movie, form=form)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddMovie()
    if form.validate_on_submit():
        search_movie = request.form["tittle"]
        search_result = themoviedb.get_movie_list(search_movie)
        return render_template("select.html", search_result=search_result)

    return render_template("add.html", form=form)


@app.route("/select", methods=["GET", "POST"])
def select():
    if request.args:
        movie = (request.args.get("movie"))

        movie = ast.literal_eval(movie)

        new_movie = Movie(
            title=movie["original_title"],
            year=movie["release_date"].split("-")[0],
            description=movie["overview"],
            rating=movie["vote_average"],
            ranking=0,
            review="Nice",
            img_url=f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
        )
        db.session.add(new_movie)
        db.session.commit()

        added_movie = db.session.query(Movie).filter(Movie.title == movie["original_title"]).first()

        return redirect(url_for('edit', id=added_movie.id))


# with app.app_context():
#     # db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
