var API_URL = window.location.origin;  
let editID = null;                                                                 //when you want to edit a product by ID
function loadProducts() {                                                          //function to grt all products
    fetch(API_URL + "/api/products")                                               //calls backend product api
     .then(res => {
        if (!res.ok) {
            throw new Error('Failed to load products');
        }
         return res.json();
     })
                                                      //where backend sends data in json format
    .then(data => {                                                            //data in array form
        let rows = "";
        if (data.length ===0){
            rows ="<tr><td colspan='5' style='text-align: center;'>No products found</td></tr>";
        }else{
            data.forEach(p => {
                rows +=`
                    <tr>
                        <td>${p.id}</td>
                        <td>${p.name}</td>
                        <td>${p.price}</td>
                        <td>${p.quantity}</td>
                        <td>                                                         //table cell
                            <button class="edit" onclick="openEdit(${p.id}, '${p.name}', ${p.price}, ${p.quantity})">Edit</button>      //calls openEdit() with product details.
                            <button class="delete" onclick="deleteProduct(${p.id})">Delete</button>                                     //calls backend to delete that product.
                        </td>
                    </tr>
                `;
            });
            document.querySelector("#productTable tbody").innerHTML = rows;                                                        //Finds the table row of your table and inserts all the newly created rows
        })
        .catch(error => {
            console.error("Error loading products:", error);
            alert("Error while loading products.");
        });
}

loadProducts();                                                                            //Loads the products.

function addProduct(){                                                                      //function for adding products
    let name = document.getElementById("pname").value;
    let price = document.getElementById("pprice").value;
    let qty = document.getElementById("pqty").value;

    if(!name){
        alert("Product name is required");
        return;
    }
    if (!price || isNaN(price) || parseFloat(price) < 0) {
        alert("Please enter a valid price (must be a number >= 0)");
        return;
    }
    if (!qty || isNaN(qty) || parseInt(qty) < 0 || !Number.isInteger(parseFloat(qty))) {
        alert("Please enter a valid quantity (must be a whole number >= 0)");
        return;
    }
    fetch(API_URL + "/api/products", {                                                        //connects backend product API
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name:name, price:parseFloat(price), quantity: parseInt(qty) })                               //gives data as json format
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(data => {
                throw new Error(data.error || "Failed to add product");
            });
        }
        return res.json();
    })                                                                                                          // response in json
    .then(() => {
        alert("Product added");
        loadProducts();                                                                    //loads added products
    })
    .catch.catch(error => {
        console.error("Error adding product:", error);
        alert(error.message || "Error adding product. Please try again.");
    });
}
function deleteProduct(id) {
    if (!confirm("DELETE")) {
        return;
    }                                                                                           //function for delete product by Id
     fetch(API_URL + "/api/products/" + id, {                                                  //fetches backend API for products by id uses method delete
        method: "DELETE"
    })
    .then(res => {
        if (!res.ok) {
            return res.json().then(data => {
                throw new Error(data.error || "Failed to delete product");
            });
        }
        return res.json();                                                                        /converts the response body into json format.
    })
    .then(() => {
        alert("Product deleted");
        loadProducts();
    })
    .catch(error => {
        console.error("Error deleting product:", error);
        alert(error.message || "Error deleting product. Please try again.");
    });
}

function openEdit(id, name, price, qty) {                                         //function for editID
    editID = id;                                                                   //stores id in variable editID
    document.getElementById("editName").value = name;                                  //Puts the product’s name,price,quantity into the input field with id
    document.getElementById("editPrice").value = price;
    document.getElementById("editQty").value = qty;
    document.getElementById("editProduct").style.display = "block";                    //This makes the editProduct visible on the screen.  
}
function updateProduct() {                                                              //function for updating products
    if (!editID) {
        alert("No product selected for editing");
        return;
    }                                                                                 
    let name = document.getElementById("editName").value;                              //gets update values for name, price and quantity from edit form.
    let price = document.getElementById("editPrice").value;
    let qty = document.getElementById("editQty").value;
    if (!name) {
        alert("Product name is required");
        return;
    }
    if (!price || isNaN(price) || parseFloat(price) < 0) {
        alert("Please enter a valid price (must be a number >= 0)");
        return;
    }
    if (!qty || isNaN(qty) || parseInt(qty) < 0 || !Number.isInteger(parseFloat(qty))) {
        alert("Please enter a valid quantity (must be a whole number >= 0)");
        return;
    }
    fetch(API_URL + "/api/products/" + editID, {                                        //fetches API products using editId
        method: "PUT",                                                                   //method PUT used to update exsisting data
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name:name, parseFloat(price), quantity: parseInt(qty) })                          //gives data in json format
    })
    .then(res => {                                       
        if (!res.ok) {
            return res.json().then(data => {                                                            //reads the server’s response and parses it into JavaScript
                throw new Error(data.error || "Failed to update product");
            });
        }
        return res.json();
    })
                                                          
    .then(() => {
        alert("Product updated");
        closeModal();                                                                //hides the edit popup
        loadProducts();                                                              //loads the product list
    })
    .catch(error => {
        console.error("Error updating product:", error);
        alert(error.message || "Error updating product. Please try again.");
    });
}
function closeModal() {                                                              //function for closeModal
    document.getElementById("editProduct").style.display = "none";                   //search for html element with the ID editProduct, changes the element css so it becomes hidden.
    editID = Null;
    document.getElementById("editName").value = "";
    document.getElementById("editPrice").value = "";
    document.getElementById("editQuantity").value = "";
}


  
