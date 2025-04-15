from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


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
app.config['SECRET_KEY'] = '12345678'
class BookForm(FlaskForm):
    book_name = StringField(label="book name", validators=[DataRequired()])
    book_author = StringField(label="book author", validators=[DataRequired()])
    rating = StringField(label="rating", validators=[DataRequired()])



all_books = []


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    form = BookForm()
    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

