from flask import Flask, request, jsonify      
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib

app= Falsk (__name__) //creates flask app
CORS(app)             //CORS means Cross origin request which joins frontend javascript to backend APIs

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' //here we are creating db which is sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False            
db = SQLAlchemy(app)

