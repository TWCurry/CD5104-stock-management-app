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
    var request = new XMLHttpRequest();
    request.open("POST", apiUrl+"/updatedb?action=getdata&data=test", true)
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
        tableHtml += "</tr>";
    }
    tableHtml += "</table>";
    $("#tableCanvas").html(tableHtml);
}