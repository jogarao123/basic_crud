import re
import os
from flask import Flask,render_template,request,flash,redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy

project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir,"bookdatabase.db"))

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=database_file

db=SQLAlchemy(app)
class Book(db.Model):
    title=db.Column(db.String(80),unique=True,nullable=False,primary_key=True)
    def __repr__(self):
        return "<title>: {}".format(self.title)
@app.route('/',methods=['POST','GET'])
def home():
    if request.form:
        book=Book(title=request.form.get('title'))
        # print(book)
        db.session.add(book)
        db.session.commit()
        # flash(f'book added',category='success')
    books=Book.query.all()
    return render_template('home.html',books=books)

@app.route('/update',methods=["GET","POST"])
def update():
    try:
        oldtitle=request.form.get('oldtitle')
        newtitle=request.form.get('newtitle')
        book=Book.query.filter_by(title=oldtitle).first()
        book.title=newtitle
        db.session.commit()
    except Exception as e:
        print(f"coudnt update booktitle {e}")
    return redirect(url_for('home'))

@app.route('/delete',methods=['POST','GET'])
def delete():
    title=request.form.get('title')
    print(request.form)
    book=Book.query.filter_by(title=title).first();
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('home'))

if(__name__=='__main__'):
    app.run(host='0.0.0.0',debug=True)