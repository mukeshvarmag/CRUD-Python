from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
from flasgger.utils import swag_from
from sqlalchemy import Sequence

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://C##ORCUSR01:tempo@localhost:1521/orcl'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
swagger = Swagger(app)

# Define Books model
class Books(db.Model):
    __tablename__ = 'BOOKS'  # Define the table name explicitly if needed
    bookid = db.Column(db.Integer, Sequence('book_id_seq'),primary_key=True)
    bookname = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Books(bookid={self.bookid}, bookname='{self.bookname}', author='{self.author}', price={self.price})>"

# Routes for CRUD operations
@app.route('/api/book', methods=['GET'])
@swag_from('swagger/get_all_books.yml')
def get_all_books():
    books = Books.query.all()
    result = [{'bookid': book.bookid, 'bookname': book.bookname, 'author': book.author, 'price': book.price} for book in books]
    return jsonify(result)

@app.route('/api/book/<int:bookid>', methods=['GET'])
@swag_from('swagger/get_book.yml')
def get_book(bookid):
    book = Books.query.get(bookid)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify({'bookid': book.bookid, 'bookname': book.bookname, 'author': book.author, 'price': book.price})

@app.route('/api/book', methods=['POST'])
@swag_from('swagger/add_book.yml')
def add_book():
    data = request.json
    new_book = Books(bookname=data['bookname'], author=data['author'], price=data['price'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'bookid': new_book.bookid}), 201

@app.route('/api/book', methods=['PUT'])
@swag_from('swagger/update_book.yml')
def update_book():

    data = request.json
    bookid = data['bookid']
    book = Books.query.get(bookid)
    book.bookname = data['bookname']
    book.author = data['author']
    book.price = data['price']
    db.session.commit()
    return jsonify({'bookid': book.bookid, 'bookname': book.bookname, 'author': book.author, 'price': book.price})

@app.route('/api/book/<int:bookid>', methods=['DELETE'])
@swag_from('swagger/delete_book.yml')
def delete_book(bookid):
    book = Books.query.get(bookid)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    db.session.delete(book)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
