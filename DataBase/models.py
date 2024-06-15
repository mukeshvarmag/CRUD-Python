from DataBase import db
from sqlalchemy import Sequence

class Books(db.Model):
    __tablename__ = 'BOOKS'
    bookid = db.Column(db.Integer, Sequence('book_id_seq'), primary_key=True)
    bookname = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Books(bookid={self.bookid}, bookname='{self.bookname}', author='{self.author}', price={self.price})>"
