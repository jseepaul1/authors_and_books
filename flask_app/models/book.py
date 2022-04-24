from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author


class Book:
    def __init__(self, book_data):
        self.id = book_data['id']
        self.title = book_data['title']
        self.num_of_pages = book_data['num_of_pages']
        self.created_at = book_data['created_at']
        self.updated_at = book_data['updated_at']
        self.authors_favorite = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO  books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"

        book_results = connectToMySQL('books_schema').query_db(
            query
        )
        books = []
        for book in book_results:
            books.append(cls(book))
        return books

    @classmethod
    def get_book_by_id(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorite_books ON books.id = favorite_books.book_id LEFT JOIN authors ON authors.id = favorite_books.author_id WHERE books.id = %(id)s;"

        book_results = connectToMySQL('books_schema').query_db(query, data)
        print('book_results - ', book_results)
        book = cls(book_results[0])
        for row in book_results:
            print('row - ', row)
            book_data = {
                'id': row['authors.id'],
                'name': row['name'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            book.authors_favorite.append(author.Author(book_data))
        return book
