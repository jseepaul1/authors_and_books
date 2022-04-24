from flask import render_template, redirect, request
from flask_app import app

from flask_app.models.author import Author
from flask_app.models.book import Book


@app.route('/authors')
def authors():
    return render_template('create_author.html', authors=Author.get_all())


@app.route("/create/author", methods=["POST"])
def create_author():
    Author.save(request.form)
    return redirect("/authors")


@app.route('/authors/<int:id>')
def show_author(id):
    data = {
        "id": id
    }
    books = Book.get_all()
    return render_template('favorite_authors.html', author=Author.get_author_by_id(data), books=books)


@app.route('/authors/connect', methods=['POST'])
def connect_author():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_to_favorite(data)
    return redirect(f"/authors/{request.form['author_id']}")
