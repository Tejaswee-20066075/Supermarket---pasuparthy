from flask import Flask, request, jsonify      
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import hashlib
import os 

app= Flask (__name__, static_folder='../frontend', static_url_path='')                                                       #creates flask app
CORS(app) #CORS means Cross origin request which joins frontend javascript to backend APIs
                                                                
 

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

@app.route("/")                                                               # Route to serve login page as home
def home():
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_file(os.path.join(frontend_path, 'login.html'))



# check the routes of API
@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})    


#registering a user

@app.route("/api/register", methods=["POST","OPTIONS"])
def register():
    if request.method =="OPTIONS":
        return '',200
     try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
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
except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed. Please try again."}), 500


@app.route("/api/login", methods=["POST","OPTIONS"])                                      # creating route for user login
def login():
    if request.method =="OPTIONS":
        return '',200
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error" : "Email and password required"}), 400              #user login error message


    user = User.query.filter_by(email=email).first()                                   #user login success message
    if user and user.password_hash == hashlib.sha256(password.encode()).hexdigest():
        return jsonify({"message": "User Login successful", "user": user.name})
    else:
        return jsonify({"error": "Invalid credentials"}), 401                       #error if credentials are wrong
    except Exception as e:
        return jsonify({"error": "Login failed. Please try again."}), 500  

@app.route("/api/products", methods=["POST","OPTIONS"])                                       #crearing route for products items
def create_product():
    if request.method =="OPTIONS":
        return '',200                                                              
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")
    if not name or price is None or quantity is None:                                    #error message for product requirement fields
        return jsonify({"error": "Name, price, and quantity are required"}), 400
      try:
            price = float(price)
            quantity = int(quantity)
        except (ValueError, TypeError):
            return jsonify({"error": "Price must be a number and quantity must be an integer"}), 400
          if price < 0:
            return jsonify({"error": "Price cannot be negative"}), 400
        
        if quantity < 0:
            return jsonify({"error": "Quantity cannot be negative"}), 400

    new_product = Product(name=name, price=price, quantity=quantity)                     #adding product to db
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added successfully"}), 201                      #return message for function product once product added succesfully
except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to add product. Please try again."}), 500


@app.route("/api/products", methods=["GET","OPTIONS"])                                           #route for seeing all the products
def get_products():
    if request.method =="OPTIONS":
        return '',200                                                                   #function to get all products
    products = Product.query.all()                                                     # it represents sqlalchemy table for products
    result = []
    for p in products:                                                                #converting sqlalchemy objects to json
        result.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "quantity": p.quantity
        })
    return jsonify(result),200
except Exception as e:
        return jsonify({"error": "Failed to retrieve products"}), 500


@app.route("/api/products/<int:id>", methods=["PUT","OPTIONS"])                                 #route for updating the products by id
def update_product(id):   
        if request.method =="OPTIONS":
            return '',200                                                            #function product update
        try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        data = request.get_json()
        if not product:                                               #it looks for product id in databaseif not product:
            return jsonify({"error": "Product not found"}), 404                           #if product id doesnt found returns 404
          if "name" in data:
            name = data.get("name", "").strip()
            if name:
                product.name = name
        
        if "price" in data:
            try:
                price = float(data.get("price"))
                if price < 0:
                    return jsonify({"error": "Price cannot be negative"}), 400
                product.price = price
            except (ValueError, TypeError):
                return jsonify({"error": "Price must be a valid number"}), 400
        
        if "quantity" in data:
            try:
                quantity = int(data.get("quantity"))
                if quantity < 0:
                    return jsonify({"error": "Quantity cannot be negative"}), 400
                product.quantity = quantity
            except (ValueError, TypeError):
                return jsonify({"error": "Quantity must be a valid integer"}), 400

        db.session.commit()                                                              #take input from html and save changes to database
        return jsonify({"message": "Product updated successfully"}),200                       #once the product is updated return successful message
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update product. Please try again."}), 500

@app.route("/api/products/<int:id>", methods=["DELETE","OPTIONS"])                              #route to delete product by id
def delete_product(id):
    if request.method =="OPTIONS":
        return '',200
    try:
      product = Product.query.get(id)                                                   #function for delete product
      if not product:
          return jsonify({"error": "Product not found"}), 404                           #if product id doesnt found return error
      db.session.delete(product)                                                        #delete from database
      db.session.commit()
      return jsonify({"message": "Product deleted successfully"}),200                      #if it is deleted then return message success
  except Exception as e:
      db.session.rollback()
      return jsonify({"error": "Failed to delete product. Please try again."}), 500

@app.route("/<path:filename>")                                                               # Route to serve static files (HTML, CSS, JS) - must be after API routes
def serve_static(filename):
    if filename.startswith('api/'):                                                          # Don't serve API routes as static files
        return jsonify({"error": "Not found"}), 404
    
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    
    if filename.endswith(('.html', '.css', '.js')):                                            # Security: Only serve specific file types
        try:
            return send_from_directory(frontend_path, filename)
        except Exception:
            return jsonify({"error": "File not found"}), 404  
    return jsonify({"error": "File type not allowed"}), 403


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables if not already created
    app.run(host="0.0.0.0", port=5000, debug=True)








