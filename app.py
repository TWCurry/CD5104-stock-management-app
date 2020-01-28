#imports
import json
from tkinter import *
from tkinter.ttk import *

#Global Variables
products = []

### Main program ###
#Main module
def main():
    #Load product data
    products = loadProductData()["products"]
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

def displayCreateProductWindow():
    print("creating new product")

def displayRemoveProductWindow():
    print("destroying product")

def saveData():
    print("saving data")

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
        for product in products:
            self.table.insert("", "end", text=product["name"], values=(product["price"], product["numberInStock"], product["type"], product["manufacturer"]))
        self.table.grid(column=1)

    def createProduct(self):
        displayCreateProductWindow()
        self.loadData()
    
    def removeProduct(self):
        displayRemoveProductWindow()
        self.loadData()

class product:
    
    def __init__(self: object, name: str, price: float, numberInStock: int):
        self.name = name
        self.price = price
        self.numberInStock = numberInStock



#Call main subroutine when script is run
if __name__ == "__main__":
    main()