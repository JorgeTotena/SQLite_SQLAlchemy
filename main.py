from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_bootstrap import Bootstrap
from sqlalchemy import Integer, String, Float



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
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
bootstrap = Bootstrap(app)
# initialize the app with the extension
class Base(DeclarativeBase):
  pass
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Books(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(unique=True, nullable=False)
    rating: Mapped[float] = mapped_column()

#CREATE
# with app.app_context():
#     # db.create_all()
#     # book = Books(
#     #     title="Los Juegos del Hambre",
#     #     author="Suzanne Collins",
#     #     rating=9,
#     # )
#     # db.session.add(book)
#     # db.session.commit()

# READ ALL RECORDS

# with app.app_context():
#     result = db.session.execute(db.select(Books).order_by(Books.title))
#     all_books = result.scalars()

# Read A Particular Record By Query
# with app.app_context():
#     book = db.session.execute(db.select(BookS).where(Books.title == "Harry Potter")).scalar()

# Update A Particular Record By Query
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Books).where(Books.title == "Harry Potter and the Chamber of Secrets")).scalar()
#     book_to_update.title = "Harry Potter and the Goblet of Fire"
#     db.session.commit()

#
# Update A Record By PRIMARY KEY
# book_id = 2
# with app.app_context():
#     book_to_update = db.session.execute(db.select(Books).where(Books.id == book_id)).scalar()
#     # or book_to_update = db.get_or_404(Book, book_id)
#     book_to_update.title = "Los Juegos del Hambre En Llamas "
#     db.session.commit()

# Delete A Particular Record By PRIMARY KEY
# book_id = 1
# with app.app_context():
#     book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
#     # or book_to_delete = db.get_or_404(Book, book_id)
#     db.session.delete(book_to_delete)
#     db.session.commit()
# You can also delete by querying for a particular value e.g. by title or one of the other properties. Again, the get_or_404() method is quite handy.




class BookForm(FlaskForm):
    book_name = StringField(label="book name", validators=[DataRequired()])
    book_author = StringField(label="book author", validators=[DataRequired()])
    rating = StringField(label="rating", validators=[DataRequired()])
    add_book = SubmitField(label="Add Book")

class EditForm(FlaskForm):
    new_rating = StringField(label="new rating", validators=[DataRequired()])
    edit_rating = SubmitField(label="Change rating")

@app.route('/')
def home():
    books = db.session.execute(db.select(Books).order_by(Books.title))
    all_books = books.scalars().all()
    # print(all_books[0].id)
    # print(type(all_books))
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Books(title = form.book_name.data,
                    author = form.book_author.data,
                    rating = form.rating.data)
        db.session.add(new_book)
        db.session.commit()
        # new_book_list ={"title":form.book_name.data,"author": form.book_author.data,"rating": form.rating.data}
        # all_books.append(new_book_list)
        # print(all_books)
        return  redirect(url_for("home"))
    return render_template("add.html", form=form)

@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
    book = db.session.execute(db.select(Books).where(Books.id == id)).scalar()
    # all_books = books.scalars().all()
    edit_rating_form = EditForm()
    if edit_rating_form.validate_on_submit():
         book.rating = edit_rating_form.new_rating.data
         db.session.commit()
         return redirect(url_for("home"))
    return render_template("editrating.html", book=book, edit_form=edit_rating_form, id=id)

@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    book = db.session.execute(db.select(Books).where(Books.id == id)).scalar()
    # all_books = books.scalars().all()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))
    return render_template("delete.html", book=book, id=id)



if __name__ == "__main__":
    app.run(debug=True)

