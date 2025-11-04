**Pasuparthy's SuperMarket**

**Description**

It is a web based product management system, Where user able to Register themselves, login, add, update, view and delete the products. 

**Technolgies Used**

**Frontend**

1.HTML

2.CSS

3.JavaScript

**Backend**

1.Python

2.SQLIte

3.Flask

**FEATURES**

1. User can register or login to system.

2. User can add, view, update and delete the product.

3. Rest API : Frontend communicates with backend using simple API endpoints.

4. SQLite database : Data is stored in a light weight relational database.

**Prerequisites**

Make sure you have Python installed on your system. You can check by running:

python --version

**Steps to Run the Project**

**Clone the repository:**

git clone https://github.com/your-repo-link.git

cd supermarket-inventory

**Set up a virtual environment (recommended):**

python -m venv venv

venv\Scripts\activate

**Install dependencies:**

pip install -r requirements.txt

**Run the Flask server:**

**python app.py**

This will start the API at http://127.0.0.1:5000

**API Endpoints**

## API Endpoints

| **Method** | **Endpoint**              | **Description**              |
|-------------|---------------------------|------------------------------|
| **POST**    | `/api/register`           | Register a new user          |
| **POST**    | `/api/login`              | User login                   |
| **GET**     | `/api/products`           | Get all products in stock    |
| **POST**    | `/api/products`           | Add a new product            |
| **PUT**     | `/api/products/<id>`      | Update a product by ID       |
| **DELETE**  | `/api/products/<id>`      | Delete a product by ID       |



