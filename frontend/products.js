var API_URL = "https://glowing-meme-jj7wq64jp4qjc4jg-5000.app.github.dev";  
let editID = null;                                                                 //when you want to edit a product by ID
function loadProducts() {                                                          //function to grt all products
    fetch(API_URL + "/api/products")                                               //calls backend product api
  
