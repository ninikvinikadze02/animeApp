from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ghibli.sqlite'
app.config['SQLALCHEMY_BINDS'] = {'anime': 'sqlite:///animegeorgian.sqlite', 'top10': 'sqlite:///top.sqlite'}
db = SQLAlchemy(app)


class Ghibli(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    director = db.Column('director', db.String(40))
    release_date = db.Column(db.Integer)
    description = db.Column('description', db.String(1000))


class animegeorgian(db.Model):
    __bind_key__ = 'anime'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    release_date = db.Column(db.Integer)
    rating = db.Column(db.Float)


class Top10anime(db.Model):
    __bind_key__ = 'top10'
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    release_date = db.Column(db.Integer)


@app.route('/')
def home():
    all_anime = Ghibli.query.all()
    return render_template('home.html', all_anime=all_anime)


@app.route('/anime')
def anime():
    all_anime_georgian = animegeorgian.query.all()
    return render_template('anime.html', all_anime_georgian=all_anime_georgian)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/addAnime', methods=['GET', 'POST'])
def addAnime():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        release_date = request.form['release_date']
        description = request.form['description']
        if title == '' or director == '' or release_date == '' or description == '':
            flash('შეიტანეთ ყველა ველი','error')
        elif not release_date.isnumeric():
            flash('გადაღების წელი უნდა იყოს რიცხვი','error')
        else:
            anime1 = Ghibli(title=title, director=director, release_date=release_date, description=description)
            db.session.add(anime1)
            db.session.commit()
            flash('მონაცემები დამატებულია', 'info')
    return render_template('addAnime.html')


@app.route('/top25Anime')
def top25Anime():
    top10 = Top10anime.query.all()
    print(top10)
    return render_template('top10anime.html', top10=top10)


if __name__ == "__main__":
    app.run(debug=True)
