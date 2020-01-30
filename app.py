#imports
import json
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.ttk import *

#Global Variables
products = []

### Main program ###
#Main module
def main():
    #Load product data
    productData = loadProductData()["products"]
    for product in productData:
        products.append(product)
    #Initialise Tkinter
    window = Tk()
    window.geometry("800x300")
    window.title("Stock Management Application")
    app = mainWindow(products, master=window)
    app.mainloop()

def loadProductData():
    f = open("productData.json", "r")
    data = json.loads(f.read())
    f.close()
    return data

def addNewProduct(name, price, numberInStock, productType, manufacturer):
    products.append({
        "name": name,
        "price": price,
        "numberInStock": numberInStock,
        "type": productType,
        "manufacturer": manufacturer
        })
    saveData()
    return products

def saveData():
    print("saving data")
    f = open("productData.json", "w")
    f.write(json.dumps({"products": products}, indent=4))
    f.close()

### Classes ###
class mainWindow(Frame):

    def __init__(self, products, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets(products)

    def createWidgets(self, products):
        ##Menubar
        #New product
        self.btnNewProduct = Button(self, text="New Product", command=self.createProduct).grid(row=0, column=0)
        #Remove product
        self.btnRemoveProduct = Button(self, text="Remove Product", command=self.removeProduct).grid(row=0, column=1)
        #Save data
        self.btnSave = Button(self, text="Save", command=saveData).grid(row=0, column=2)
        ##Table
        self.table = Treeview(self)
        #Create Columns
        self.table["columns"]=("price","number","type", "manufacturer")
        self.table.column("#0", width=100)
        self.table.column("price", width=100)
        self.table.column("number", width=100)
        self.table.column("type", width=100)
        self.table.column("manufacturer", width=100)
        #Create headings for the columns
        self.table.heading("#0", text="Name")
        self.table.heading("price", text="Price")
        self.table.heading("number", text="Number in stock")
        self.table.heading("type", text="Type")
        self.table.heading("manufacturer", text="Manufacturer")
        self.table.grid(column=1)
        self.loadData(products)

    def loadData(self, products):
        self.table.delete(*self.table.get_children()) #Clear table
        for product in products:
            self.table.insert("", "end", text=product["name"], values=(product["price"], product["numberInStock"], product["type"], product["manufacturer"]))
        self.table.grid(column=1)

    def createProduct(self):
        productName = simpledialog.askstring("Create New Product", "Enter the product name", parent=self)
        if productName =="":
            messagebox.showinfo("Invalid Input","Please enter a value.")
            return
        price = simpledialog.askstring("Create New Product", "Enter the product price", parent=self)
        if price =="":
            messagebox.showinfo("Invalid Input","Please enter a value.")
            return
        numberInStock = 0
        productType = simpledialog.askstring("Create New Product", "Enter the type or product(phone, food, etc)", parent=self)
        if productType =="":
            messagebox.showinfo("Invalid Input","Please enter a value.")
            return
        manufacturer = simpledialog.askstring("Create New Product", "Enter the manufacturer", parent=self)
        if manufacturer =="":
            messagebox.showinfo("Invalid Input","Please enter a value.")
            return
        newProducts = addNewProduct(productName, price, numberInStock, productType, manufacturer)
        self.loadData(newProducts)
    
    def removeProduct(self):
        displayRemoveProductWindow()

class product:
    
    def __init__(self: object, name: str, price: float, numberInStock: int):
        self.name = name
        self.price = price
        self.numberInStock = numberInStock



#Call main subroutine when script is run
if __name__ == "__main__":
    main()