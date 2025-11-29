from flask import Flask, request, jsonify      
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib

app= Flask (__name__)                                                       #creates flask app
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers="*", supports_credentials=True)                                                                  #CORS means Cross origin request which joins frontend javascript to backend APIs

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'           #here we are creating db which is sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False            
db = SQLAlchemy(app)

class User(db.Model):                                                   #so here we are creating user model in database we have created id,name,email,password also we are hashing passwords
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

class Product(db.Model):                                              # we are adding stock items as product model in database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


# check the routes of API
@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})    


#registering a user

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400
        
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400


#hashing password using python library hashlib

    password_hash = hashlib.sha256(password.encode()).hexdigest()    
    new_user = User(name=name, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/api/login", methods=["POST"])                                      # creating route for user login
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error" : "Email and password required"}), 400              #user login error message


    user = User.query.filter_by(email=email).first()                                   #user login success message
    if user and user.password_hash == hashlib.sha256(password.emcode()).hexdigest():
        return jsonify({"message": "User Login successful", "user": user.name})
    else:
        return jsonify({"error": "Invalid credentials"}), 401                       #error if credentials are wrong

@app.route("/api/products", methods=["POST"])                                       #crearing route for products items
def create_product():                                                              
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")
    if not name or price is None or quantity is None:                                    #error message for product requirement fields
        return jsonify({"error": "Name, price, and quantity are required"}), 400

    new_product = Product(name=name, price=price, quantity=quantity)                     #adding product to db
    db.sesion.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added successfully"}), 201                      #return message for function product once product added succesfully

@app.route("/api/products", methods=["GET"])                                           #route for seeing all the products
def get_products():                                                                    #function to get all products
    products = Product.query.all()                                                     # it represents sqlalchemy table for products
    result = []
    for p in products:                                                                #converting sqlalchemy objects to json
        result.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "quantity": p.quantity
        })
    return jsonify(result)

@app.route("/api/products/<int:id>", methods=["PUT"])                                 #route for updating the products by id
def update_product(id):                                                               #function product update
        product = Product.query.get(id)
        if not Product:                                               #it looks for product id in databaseif not product:
            return jsonify({"error": "Product not found"}), 404                           #if product id doesnt found returns 404


        data = request.get_json()
        product.name = data.get("name", product.name)
        product.price = data.get("price", product.price)
        product.quantity = data.get("quantity", product.quantity)
        db.session.commit()                                                              #take input from html and save changes to database

        return jsonify({"message": "Product updated successfully"})                       #once the product is updated return successful message

@app.route("/api/products/<int:id>", methods=["DELETE"])                              #route to delete product by id
def delete_product(id):
    product = Product.query.get(id)                                                   #function for delete product
    if not product:
        return jsonify({"error": "Product not found"}), 404                           #if product id doesnt found return error

    db.session.delete(product)                                                        #delete from database
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})                       #if it is deleted then return message success

if __name__ == "__main__":                                                            #main function
    with app.app_context():
        db.create_all()                                                               # Creates tables if not already created
    app.run(host="0.0.0.0", port=5000, debug=True)







