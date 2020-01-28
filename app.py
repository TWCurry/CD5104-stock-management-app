from tkinter import *
from ui import *

def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()

if __name__ == "__main__":
    main()