from flask import Flask, request, redirect, render_template, session, flash, url_for
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key='sectreto'
mysql = MySQLConnector(app, 'books')

@app.route('/')
def index():
    print "in the index"
    query = "SELECT id, title, author, DATE_FORMAT(created_at, '%D %M %Y') as created FROM books"
    books = mysql.query_db(query)
    return render_template('index.html', all_books=books)

@app.route('/confirm/<id>')
def confirm(id):
    query = "SELECT title FROM books WHERE id = :id"
    data ={"id": id}
    book = mysql.query_db(query,data)
    title = book[0]['title']
    return render_template('confirm.html', title=title, id=id)

@app.route('/destroy/<id>')
def destroy(id):
    print "helllooooooooo"
    query = "DELETE FROM books WHERE id = :id"
    data = { "id" : id  }
    mysql.query_db(query,data)
    return redirect('/')

@app.route('/add')
def add():    
    print "clicked add butttononononononon"
    return render_template('add.html')

@app.route('/insert', methods=['POST'])
def insert():
    print "inserting"
    query = "INSERT INTO books (title, author, created_at, update_at) VALUES (:title, :author, NOW(), NOW())"
    data = {
        "title": request.form['title'],
        "author": request.form['author'],
    }
    mysql.query_db(query,data)
    return redirect('/')

@app.route('/change/<id>')
def change(id):
    query = "SELECT id, title, author FROM books WHERE id =:id"
    data = {"id": id}
    book = mysql.query_db(query, data)
    print book
    print book[0]
    return render_template('update.html', book=book)

@app.route('/update', methods=['POST'])
def update():
    print request.form
    query = "UPDATE books SET title = :title, author= :author WHERE id = :id"
    data = {
        "title": request.form['title'],
        "author": request.form['author'],
        "id": request.form['id']
    }
    mysql.query_db(query,data)
    return redirect('/')

app.run(debug=True)