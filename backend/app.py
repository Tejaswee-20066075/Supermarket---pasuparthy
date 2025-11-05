from flask import Flask, request, jsonify      
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib

app= Falsk (__name__)                                                       //creates flask app
CORS(app)                                                                  //CORS means Cross origin request which joins frontend javascript to backend APIs

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'           //here we are creating db which is sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False            
db = SQLAlchemy(app)

class User(db.Model):                                                   // so here we are creating user model in database we have created id,name,email,password also we are hashing passwords
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

class Product(db.Model):                                              // we are adding stock items as product model in database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


# check the routes of API
@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})    


#registering a user

@app.route("/api/register", methods=[POST])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")




