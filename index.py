from tkinter import ttk
from tkinter import *

import sqlite3

class Product:

    def __init__(self, window):
        self.wind=window
        self.wind.title('Hola Mundo')

        #creatin a frame container
        frame=LabelFrame(self.wind, text= 'Register a new Predutc')
        frame.grid(row=0, column=0,columnspan=3,pady=20)

        #name input
        Label(frame, text='Name : ').grid(row=1, column=0)
        self.name=Entry(frame)
        self.name.grid(row =1 ,column=1)



    

if __name__=='__main__':
    window=Tk()
    application=Product(window)
    window.mainloop()


