var API_URL = "https://glowing-meme-jj7wq64jp4qjc4jg-5000.app.github.dev";  
let editID = null;                                                                 //when you want to edit a product by ID
function loadProducts() {                                                          //function to grt all products
    fetch(API_URL + "/api/products")                                               //calls backend product api
     .then(res => res.json())                                                      //where backend sends data in json format
        .then(data => {                                                            //data in array form
            let rows = "";
            data.forEach(p => {                                                     //for each product will create a row
                rows += `
                    <tr>                                                            //table row
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
        });
}

loadProducts();                                                                            //Loads the products.

function addProduct(){                                                                      //function for adding products
    let name = document.getElementById("pname").value;
    let price = document.getElementById("pprice").value;
    let qty = document.getElementById("pqty").value;

    fetch(API_URL + "/api/products", {                                                        //connects backend product API
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, price, quantity: qty })                               //gives data as json format
    })
    .then(res => res.json())                                                                  // response in json
        .then(() => {
            alert("Product added");
            loadProducts();                                                                    //loads added products
    });
}
function deleteProduct(id) {                                                                   //function for delete product by Id
     fetch(API_URL + "/api/products/" + id, {                                                  //fetches backend API for products by id uses method delete
        method: "DELETE"
    })
    .then(res => res.json())                                                                   //converts the response body into json format.                                         
    .then(() => {
        alert("Product deleted");
        loadProducts();
    });    
}

function openEdit(id, name, price, qty) {                                         //function for editID
    editID = id;                                                                   //stores id in variable editID
    document.getElementById("editName").value = name;                                  //Puts the product’s name,price,quantity into the input field with id
    document.getElementById("editPrice").value = price;
    document.getElementById("editQty").value = qty;
    document.getElementById("editProduct").style.display = "block";                    //This makes the editProduct visible on the screen.  
}
function updateProduct() {                                                             //function for updating products
    let name = document.getElementById("editName").value;                              //gets update values for name, price and quantity from edit form.
    let price = document.getElementById("editPrice").value;
    let qty = document.getElementById("editQty").value;

    fetch(API_URL + "/api/products/" + editID, {                                        //fetches API products using editId
        method: "PUT",                                                                   //method PUT used to update exsisting data
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, price, quantity: qty })                          //gives data in json format
    })
    .then(res => res.json())                                                          //reads the server’s response and parses it into JavaScript.
    .then(() => {
        alert("Product updated");
        closeModal();                                                                //hides the edit popup
        loadProducts();                                                              //loads the product list
    });
}
function closeModal() {                                                              //function for closeModal
    document.getElementById("editProduct").style.display = "none";                   //search for html element with the ID editProduct, changes the element css so it becomes hidden.
}


  
