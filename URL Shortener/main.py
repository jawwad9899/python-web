from flask import Flask,Response, redirect, render_template, request
from flask_pymongo import PyMongo
from db import connect_to_db
from random import randint

app = Flask(__name__)
collection = connect_to_db(app)

class App():
    @staticmethod
    def index():
        data = request.form.to_dict().get("url",None)
        url = "" if data is None else data
        duplicate = collection.find_one({ "url":url }) 

        if(url != "" and duplicate is None):
            id = randint(2_222_222,9_999_999)
            shortened = f"http://127.0.0.1:5000/url/{id}"
            collection.insert_one({
                "url":url,
                "shortened_url":shortened,
                "shortened_id":id
            })
            url = shortened
        if(duplicate):
            url = duplicate.get("shortened")

        return render_template("index.html",url=url if url is not None else "")

    @staticmethod
    def shortened_url(id):
        doc = collection.find_one({"shortened_id":id})
        if(doc is None):
            return Response("404 Not Found",status=404)
        return redirect(doc.get("url",None))

# Routes
app.add_url_rule("/","index",App.index,methods=['GET','POST'])
app.add_url_rule("/url/<int:id>","shortened url",App.shortened_url,methods=['GET'])

# Main
if __name__ == "__main__":
    app.run(debug=True)

