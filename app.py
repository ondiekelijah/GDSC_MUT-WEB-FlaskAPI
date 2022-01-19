from flask import Flask,request,json,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

import traceback
import sys

from werkzeug.routing import BuildError
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


# Begin models

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique = True, nullable=False)
    content = db.Column(db.Text,nullable=False)

# End models


class PostSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "title", "content")


post_schema = PostSchema()
posts_schema = PostSchema(many=True)

# Begin routes

# Home route
@app.route("/")
def hello_world():
    return {"message": "Introduction to APIs in Flask"}


# Fetching all posts

@app.route("/posts")
def posts():

    try:
        posts = Post.query.all()

        all_posts = posts_schema.dump(posts)

        return {"data": all_posts}

    except Exception as e:
        return {"ERROR" : f"{e}"}, 500


# Fetch a single post by ID
# http://localhost:5000/posts/7000000

@app.route("/posts/<int:article_id>", methods=['GET'])
def post(article_id):
    try:
        post = Post.query.filter_by(id=article_id).first()

        if post is None:
            return f"Post with an id {article_id} not available", 404

        single_post = post_schema.dump(post)

        return {"data": single_post}

    except Exception as e:
        return {"ERROR" : f"{e}"}, 500


# Create a new post

@app.route("/createpost", methods=['POST'])
def new_post():
    try:
        title = request.json['title']
        content = request.json['content']

        # TypeError: Object of type Post is not JSON serializable
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()

        saved_post = post_schema.dump(new_post)

        return {"data": saved_post}, 201

    except Exception as e:
        return {"ERROR" : f"{e}"}, 500


# localhost:5000/posts/update/8
@app.route("/posts/update/<int:article_id>", methods=['PATCH'])
def update_post(article_id):
    try:
        post = Post.query.filter_by(id=article_id).first()

        if post is None:
            return f"Post with an id {article_id} not available", 404

        updated_title = request.json['title']
        updated_content = request.json['content']

        post.title = updated_title
        post.content = updated_content

        db.session.commit()


        update_post = Post.query.filter_by(id=article_id).first()

        update_post = post_schema.dump(update_post)

        return {"data": update_post}
    
    except Exception as e:
        return {"ERROR" : f"{e}"}, 500


# Delete a post
# http://127.0.0.1:5000/posts/delete/4

@app.route("/posts/delete/<int:article_id>", methods=['DELETE'])
def delete_post(article_id):
    try:
        post = Post.query.filter_by(id=article_id).first()

        if post is None:
            return f"Post with an id {article_id} not available", 404

        db.session.delete(post)
        db.session.commit()

        return {"message":"post has been deleted"}, 204

    except Exception as e:
        return {"ERROR" : f"{e}"}, 500



# End routes

# Before Python runs a Python file, it sets a few special variable for that file, __name__ is one of them.
# When Python runs a python file directly it sets the __name__ == __main__

# When we import a file, Python sets the __name__ variable to the name of the file

if __name__ == "__main__":
    app.run(debug=True)
