from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bqrkxmehljpxxa:72d0732aa4c776a6fdb62ffcda5cbdb895d39217663285532a1935e1ba77be1d@ec2-54-159-175-38.compute-1.amazonaws.com:5432/da6mos1t2k0h1b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

class BlogPost(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String,nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(20),nullable=False,default='N/A')
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts',methods=['GET','POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == "POST":
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post)




@app.route('/posts/flask_new',methods=['GET','POST'])
def posts_new():

    if request.method == 'POST':
        post_title = request.form['title']
        post_author = request.form['author']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title,author=post_author,content=post_content)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_posts.html')




if __name__ == "__main__":
    app.run(debug=True)