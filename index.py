from os import name
from tkinter import ttk
from tkinter import *

import sqlite3

class Product:
    db_name='DataBase.db'


    def __init__(self, window):
        self.wind=window
        self.wind.title('Register Product')

        #creatin a frame container
        frame=LabelFrame(self.wind, text= 'Register a new Predutc')
        frame.grid(row=0, column=0,columnspan=3,pady=10)

        #name input
        Label(frame, text='Name : ').grid(row=1, column=0)
        self.name=Entry(frame)
        self.name.focus()
        self.name.grid(row =1 ,column=1)
        
        #Price input
        Label(frame, text='Price : ').grid(row=2, column=0)
        self.price=Entry(frame)
        self.price.grid(row =2 ,column=1)
        #Add Button
        ttk.Button(frame,text='Save Product',command=self.add_Product).grid(row=3,columnspan=2,sticky=W+E)
        #Output Messages
        self.message=Label(text='',fg='red')
        self.message.grid(row=3,column=0,columnspan=2,sticky=W+E)

        #table
        self.tree=ttk.Treeview(height=10,columns=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0',text='Name',anchor=CENTER)
        self.tree.heading('#1',text='Price',anchor=CENTER)
        
        #Buttons
        ttk.Button(text='DELETE',command= self.delete_product).grid(row=5,column=0,sticky=W+E)
        ttk.Button(text='EDIT',command=self.edit_product).grid(row=5,column=1,sticky=W+E) 

        #Filling the Row
        self.get_product()
    
    def run_query(self,query,parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result=cursor.execute(query,parameters)
            conn.commit()
        return result
    
    def get_product(self):
        #Cleaning table
        records =self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query='SELECT * FROM Product ORDER BY NAME DESC'
        db_rows=self.run_query(query)
        #filling data
        for row in db_rows:
            self.tree.insert('',0,text=row[1],values=row[2])
    
    def validation(self):
        return len(self.name.get())!=0 and len(self.price.get())!=0
    
    def add_Product(self):
        if self.validation():
            query='INSERT INTO Product Values (NULL,?,?)'
            parameters=(self.name.get(),self.price.get())
            self.run_query(query,parameters)
            self.message['text']='Product {} added successfully'.format(self.name.get())
            self.name.delete(0,END)
            self.price.delete(0,END)
        else:
            self.message['text']='Name and Price are required'
        self.get_product()
    
    def delete_product(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']='Please Select a Record'
            return
        self.message['text']=''
        name=self.tree.item(self.tree.selection())['text']
        query='DELETE FROM Product WHERE Name = ?'
        self.run_query(query,(name, ))
        self.message['text']='Record {} deleted successfully'.format(name)
        self.get_product()
    def edit_product(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text']='Please Select a Record'
            return
        old_name=self.tree.item(self.tree.selection())['text']
        old_price=self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind=Toplevel()
        self.edit_wind.title='Edit Product'
        #old_name
        Label(self.edit_wind,text=('Old Name: ')).grid(row=0,column=1)
        Entry(self.edit_wind,textvariable=StringVar(self.edit_wind,value=old_name),state='readonly').grid(row=0,column=2)
        #New name
        Label(self.edit_wind,text=('New Name: ')).grid(row=1,column=1)
        new_name=Entry(self.edit_wind)
        new_name.grid(row=1,column=2)
        #old_Price
        Label(self.edit_wind,text=('Old Price: ')).grid(row=2,column=1)
        Entry(self.edit_wind,textvariable=StringVar(self.edit_wind,value=old_price),state='readonly').grid(row=2,column=2)
        #New Price
        Label(self.edit_wind,text=('New Price: ')).grid(row=3,column=1)
        new_price=Entry(self.edit_wind)
        new_price.grid(row=3,column=2)
        #Button
        Button(self.edit_wind,text='Update',command=lambda: self.edit_records(new_name.get(),new_price.get(),old_name,old_price)).grid(row=4,column=2,sticky=W+E)
    
    def edit_records(self,new_name,new_price,old_name,old_price):
        query='UPDATE Product SET Name = ?, Price = ? WHERE Name = ? AND Price = ?'
        parameters=(new_name,new_price,old_name,old_price)
        self.run_query(query,parameters)
        self.edit_wind.destroy()
        self.message['text']='Record {} updated successfully'.format(old_name)
        self.get_product()



if __name__=='__main__':
    window=Tk()
    application=Product(window)
    window.mainloop()


