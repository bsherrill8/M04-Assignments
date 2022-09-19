#application.py
#Brian Sherrill
#9/18/2022
#Purpose: design and use a basic API

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy as SA
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SA(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String)

    def __repr__(self):
        return f"{self.title} - {self.author}"


@app.route('/')
def index():
    return 'Hello'

@app.route('/books')
def get_drinks():
    books = Book.query.all()
    output = []
    
    for book in books:
        book_data = {'title': book.title, 'author':book.author, 'publisher': book.publisher}
        output.append(book_data)
    
    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return ({'title': book.title, 'author':book.author, 'publisher': book.publisher})

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(title=request.json['title'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()

    return{'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return {"message" : "Deleted"}
    