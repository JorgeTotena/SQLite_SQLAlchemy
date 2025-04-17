from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
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
    add_book = SubmitField(label="Add Book")



all_books = []


@app.route('/')
def home():
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = BookForm()
    if form.validate_on_submit():
        new_book ={"title":form.book_name.data,
                   "author": form.book_author.data,
                   "rating": form.rating.data
        }
        all_books.append(new_book)
        print(all_books)
        return  redirect(url_for("home"))
    return render_template("add.html", form=form, all_books=all_books)


if __name__ == "__main__":
    app.run(debug=True)

