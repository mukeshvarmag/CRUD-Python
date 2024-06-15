from flask import Blueprint, request, jsonify
from flasgger.utils import swag_from
from DataBase.models import Books
from DataBase import db

bp = Blueprint('books', __name__, url_prefix='/api/book')

@bp.route('/', methods=['GET'])
@swag_from('../../swagger/get_all_books.yml')
def get_all_books():
    books = Books.query.all()
    result = [{'bookid': book.bookid, 'bookname': book.bookname, 'author': book.author, 'price': book.price} for book in books]
    return jsonify(result)

@bp.route('/<int:bookid>', methods=['GET'])
@swag_from('../../swagger/get_book.yml')
def get_book(bookid):
    book = Books.query.get(bookid)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify({'bookid': book.bookid, 'bookname': book.bookname, 'author': book.author, 'price': book.price})

@bp.route('/', methods=['POST'])
@swag_from('../../swagger/add_book.yml')
def add_book():
    data = request.json
    new_book = Books(bookname=data['bookname'], author=data['author'], price=data['price'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'bookid': new_book.bookid}), 201

@bp.route('/', methods=['PUT'])
@swag_from('../../swagger/update_book.yml')
def update_book():
    data = request.json
    bookid = data['bookid']
    book = Books.query.get(bookid)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    book.bookname = data['bookname']
    book.author = data['author']
    book.price = data['price']
    db.session.commit()
    return jsonify({'bookid': book.bookid, 'bookname': book.bookname, 'author': book.author, 'price': book.price})

@bp.route('/<int:bookid>', methods=['DELETE'])
@swag_from('../../swagger/delete_book.yml')
def delete_book(bookid):
    book = Books.query.get(bookid)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    db.session.delete(book)
    db.session.commit()
    return '', 204
