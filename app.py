from tkinter import *

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        frame1 = Frame(self, width=40, height=40)
        frame1.grid(column=0, row=0)
        frame1.grid_propagate(False)
        frame1.rowconfigure(0, weight=1)
        frame1.columnconfigure(0, weight=1)
        self.button1 = Button(frame1, text="1", command=self.one).grid(row=0)
        self.button2 = Button(self, text="2", command=self.two).grid(row=0, column=1)
        self.button3 = Button(self, text="3", command=self.three).grid(row=1)
        self.button4 = Button(self, text="4", command=self.four).grid(row=1, column=1)

    def one(self):
        print("1")
    def two(self):
        print("2")
    def three(self):
        print("3")
    def four(self):
        print("4")

def main():
    window = Tk()
    window.geometry("400x300")
    window.title("Stock Management Application")
    app = Application(master=window)
    app.mainloop()

if __name__ == "__main__":
    main()