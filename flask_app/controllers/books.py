from flask import render_template, redirect, request
from flask_app import app

# from ..models.author import Author
from flask_app.models.book import Book
from flask_app.models.author import Author


@app.route("/")
def index():
    return redirect("/books")


@app.route('/books')
def books():
    return render_template('create_book.html', books=Book.get_all())


@app.route("/create/book", methods=["POST"])
def create_book():
    Book.save(request.form)
    return redirect("/books")


@app.route('/books/<int:id>')
def show_book(id):
    data = {
        "id": int(id)
    }
    authors = Author.get_all()
    return render_template('favorite_books.html', book=Book.get_book_by_id(data), authors=authors)

@app.route('/books/connect', methods=['POST'])
def connect_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_to_favorite(data)
    return redirect(f"/books/{request.form['book_id']}")
