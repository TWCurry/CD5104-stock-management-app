var apiUrl = "https://mnwg43encg.execute-api.eu-west-2.amazonaws.com/Prod"

window.onload = function(){ //Function to trigger once DOM has loaded
    console.log("Page loaded");
    //Fetch data
    loadTable()
 }

function addItem(){
    console.log("Adding new product");
}

function loadTable(){
    $("#tableCanvas").html("<img src=\"img/spinner.gif\">");//Display loading spinner
    var request = new XMLHttpRequest();
    request.open("POST", apiUrl+"/updatedb?action=getdata&data=placeholder", true)
    request.send();
    request.onreadystatechange = function() { //On data recieved...
        if (request.readyState == 4) {
            if (request.status != 200){
                $("#tableCanvas").html("Error: Could not load data: " + request.status);
            }else{
                dynamicTable(request.response);
            }
        }
    }
    request.onerror=function(){
        console.log(request.responseText);
        $("#tableCanvas").html("Error: Could not load data.");
    }
}

function dynamicTable(data){
    var tableHtml="<table id=\"productTable\"><tr><th>Product Name</th><th>Price</th><th>Number in stock</th><th>Product Type</th><th>Manufacturer</th></tr>";
    for (product of JSON.parse(data)) {
        tableHtml += "<tr>";
        for (field in product){
            tableHtml += "<td>"+product[field]+"</td>";
        }
        //Add buttons
        tableHtml += "<td><button class=\"closeButton\" onclick=\"deleteItem(\'"+product["name"]+"\')\">X</button> <button onclick=\"changeStock(\'"+product["name"]+"\', "+String(Number(product["number"])+1)+")\">▲</button> <button onclick=\"changeStock(\'"+product["name"]+"\', "+String(Number(product["number"])-1)+")\">▼</button></td></tr>";
    }
    //New product input fields
    tableHtml += "<tr><td><input type=\"text\" id=\"tbName\"</td><td><input type=\"text\" id=\"tbPrice\"</td><td><input type=\"text\" id=\"tbNumber\"</td><td><input type=\"text\" id=\"tbType\"</td><td><input type=\"text\" id=\"tbManufacturer\"</td>";
    tableHtml += "<td><button id=\"createButton\" onclick=\"createProduct()\">Create product</button></td></tr></table>";
    $("#tableCanvas").html(tableHtml);
}

function deleteItem(productName){
    var postData = JSON.stringify({"name": productName});
    var request = new XMLHttpRequest();
    request.open("POST", encodeURI(apiUrl+"/updatedb?action=remove&data="+postData), true)
    request.send();
    request.onreadystatechange = function() { //On data recieved...
        if (request.readyState == 4) {
            if (request.status != 200){
                alert("Error: Could not remove item - " + request.responseText);
            }else{
                alert("Successfully deleted item.");
            }
        }
    }
    request.onerror=function(){
        console.log(request.responseText);
        alert("Error: Could not remove item - " + request.responseText)
    }
    loadTable();
}

function createProduct(){
    var name = document.getElementById('tbName').value
    var price = document.getElementById('tbPrice').value
    var number = document.getElementById('tbNumber').value
    var type = document.getElementById('tbType').value
    var manufacturer = document.getElementById('tbManufacturer').value
    var data = JSON.stringify({
        "name": name,
        "price": price,
        "numberinstock": number,
        "producttype": type,
        "manufacturer": manufacturer
    });
    var request = new XMLHttpRequest();
    request.open("POST", encodeURI(apiUrl+"/updatedb?action=add&data="+data), true)
    request.send();
    request.onreadystatechange = function() { //On data recieved...
        if (request.readyState == 4) {
            if (request.status != 200){
                alert("Error: Could not add item - " + request.responseText);
            }else{
                alert("Successfully added item.");
            }
        }
    }
    request.onerror=function(){
        console.log(request.responseText);
        alert("Error: Could not add item - " + request.responseText)
    }
    loadTable();
}

function changeStock(productName, newStockLevel){
    data = JSON.stringify({
        "name": productName,
        "number": newStockLevel
    });
    var request = new XMLHttpRequest();
    request.open("POST", encodeURI(apiUrl+"/updatedb?action=setstocklevel&data="+data), true)
    request.send();
    request.onreadystatechange = function() { //On data recieved...
        if (request.readyState == 4) {
            if (request.status != 200){
                alert("Error: Could not update stock level - " + request.responseText);
            }
        }
    }
    request.onerror=function(){
        console.log(request.responseText);
        alert("Error: Could not update stock level - " + request.responseText)
    }
    loadTable();
}