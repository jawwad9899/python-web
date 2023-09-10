from flask_pymongo import PyMongo

def connect_to_db(app):
    # your mongo URI
    mongoURI = ""
    app.config["MONGO_URI"] = f"{mongoURI}/URLs"
    mongo = PyMongo(app)
    if(mongo.cx.get_database("URLs") is not None):
        return mongo.db.get_collection("all_urls")
    
    collection = mongo.db.create_collection("all_urls")
    return collection   
