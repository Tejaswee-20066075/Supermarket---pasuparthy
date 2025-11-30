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
}
  
