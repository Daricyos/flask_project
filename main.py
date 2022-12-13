from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate


app = Flask(__name__)


#create datebase
app.config['SQLALCHEMY_DATABASE_URI'] = 
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String)
    # anime = db.relationship('Anime', backref='person',                
    #                             lazy='dynamic')

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, name="Name anime")
    description = db.Column(db.Text, name= "Description")
    rating = db.Column(db.Float, nullable= False, name='Rating')
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def repr(self):
        return f'<Id {self.id} name {self.name} description {self.description } rating {self.rating}>'


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('base.html', items=Anime.query.all())


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    return 'Logout'


@app.route('/anime', methods=['GET'])
def anime():
    return render_template('form.html')


@app.route('/add_anime', methods=['POST'])
def add_anime():
    if request.method == "POST":
        new = Anime(
            name=request.form["name"],
            description=request.form["description"],
            rating=request.form["rating"],
        )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for("hello_world"))
    return render_template("form.html")


@app.route('/anime/delete/<int:id>')
def delete_anime(id):
    anime_to_delete = Anime.query.get_or_404(id)

    try:
        db.session.delete(anime_to_delete)
        db.session.commit()

        return redirect(url_for("hello_world"))

    except:
        return redirect(url_for("hello_world"))

if __name__ == '__main__':
    app.run(debug=True)
