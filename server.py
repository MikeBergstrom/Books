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
    query = "INSERT INTO books (title, author, created_at, updated_at) VALUES (:title, :author, NOW(), NOW())"
    data = {
        "title": request.form['title'],
        "author": request.form['author'],
    }
    mysql.query_db(query,data)
    return redirect('/')

@app.route('/quote/<id>')
def change(id):
    query = "SELECT id, title FROM books WHERE id =:id"
    data = {"id": id}
    book = mysql.query_db(query, data)
    print book
    print book[0]
    return render_template('quote.html', book=book)

@app.route('/postquote', methods=['POST'])
def update():
    print request.form
    print request.form['submit']
    if request.form['submit'] == 'Go Back':
        print "we are canceling"
        return redirect('/')
    elif request.form['submit'] == 'Add Quote':
        print "lets submit this sumbit"
        query = "INSERT INTO quotes (quote, book_id, created_at, updated_at) VALUES (:quote, :id, NOW(), NOW())"
        data = {
            "quote": request.form['quote'],
            "id": request.form['id']
        }
        mysql.query_db(query,data)
    return redirect('/')
@app.route('/quotes/<id>')
def quotes(id):
    query = "SELECT quote FROM quotes WHERE book_id = :id"
    data = {"id": id}
    quote_list = mysql.query_db(query, data)
    query2 = "SELECT title FROM books WHERE id = :id"
    data2 ={"id": id}
    book = mysql.query_db(query2,data2)
    print quote_list
    print book
    print quote_list[0]['quote']
    return render_template('quotes.html', quote_list=quote_list, book=book)

    # query = "UPDATE books SET title = :title, author= :author WHERE id = :id"
    # data = {
    #     "title": request.form['title'],
    #     "author": request.form['author'],
    #     "id": request.form['id']
    # }
    # mysql.query_db(query,data)
    return redirect('/')

app.run(debug=True)