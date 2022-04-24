from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.book import Book


class Author:
    def __init__(self, author_data):
        self.id = author_data['id']
        self.name = author_data['name']
        self.created_at = author_data['created_at']
        self.updated_at = author_data['updated_at']

        self.favorite_books = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO authors ( name ) VALUES (%(name)s);"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"

        author_author_results = connectToMySQL('books_schema').query_db(
            query
        )
        authors = []
        for author in author_author_results:
            authors.append(cls(author))
        return authors

    @classmethod
    def get_author_by_id(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorite_books ON authors.id = favorite_books.author_id LEFT JOIN books ON books.id = favorite_books.book_id WHERE authors.id = %(id)s;"
        author_results = connectToMySQL('books_schema').query_db(query, data)
        author = cls(author_results[0])
        print('author_results - ', author_results)
        for row in author_results:
            print('row - ', row)
            book_data = {
                "id": row['books.id'],
                "title": row['title'],
                "num_of_pages": row['num_of_pages'],
                "created_at": row['books.created_at'],
                "updated_at": row['books.updated_at']
            }
            author.favorite_books.append(Book(book_data))
        print('author - ', author.favorite_books)
        return author

    @classmethod
    def add_to_favorite(cls, data):
        query = "INSERT INTO favorite_books (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        insert_result = connectToMySQL('books_schema').query_db(query, data)
        print('insert_result - ', insert_result)
        return insert_result
