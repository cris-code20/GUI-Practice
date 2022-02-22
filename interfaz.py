from cProfile import label
from cgitb import text
from inspect import Parameter
import sqlite3;
from tkinter import ttk;
from tkinter import *

from pkg_resources import run_script


class Product:
    db_name = 'guiDB'

    def __init__(self, window):
        self.wind = window
        self.wind.title('products Application')
# frame

        frame = LabelFrame(self.wind , text = 'Register a New Product');
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

# price Input
        
        Label(frame, text = 'price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

#Button Add Products
        ttk.Button(frame, text = 'save Product', command=self.add_productos).grid(row=3, columnspan=2, sticky=W + E)
        

# messages
        self.messages = Label(text='',fg='red')
        self.messages.grid(row=3, column=0, columnspan=2, sticky=W+E)

# Table
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row = 4, column = 0, columnspan=2)
        self.tree.heading('#0', text='Name', anchor=CENTER)
        self.tree.heading('#1',text='price', anchor=CENTER)

        self.get_Products()

# Buttons
        ttk.Button(text='DELETE', command=self.deleteProducts).grid(row=5, column=0, sticky=W+E)
        ttk.Button(text='EDIT', command=self.editProducts).grid(row=5, column=1, sticky=W+E)

# filling the Row
    def querys(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                result = cursor.execute(query, parameters)
                conn.commit()
        return result


    def get_Products(self):
        
        recors = self.tree.get_children()
        for element in recors:
                self.tree.delete(element)
        query = 'SELECT * FROM product ORDER BY name DESC'
        dbRow = self.querys(query)
        for row in dbRow:
                self.tree.insert('', 0, text=row[1], values=row[2])
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_productos(self):
        if self.validation():
                query = 'INSERT INTO product VALUES(NULL, ?, ?)'
                parameters = (self.name.get(),self.price.get())
                self.querys(query, parameters)
                self.messages['text'] = 'product {} added Susefully'.format(self.name.get())
                self.name.delete(0, END)
                self.price.delete(0, END)
        else:
                self.messages['text'] = 'Name and Price are required'
        self.get_Products()

    def deleteProducts(self):
        self.messages['text'] = ''
        try:
                self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
                self.messages['text'] = 'Please Select a Record'
                return
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.querys(query, (name, ))
        self.messages['text'] = 'Record {} deleted successfully'.format(name)
        self.get_Products()
    

    def editProducts(self):
        self.messages['text'] = ''
        try:
                self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
                self.messages['text'] = 'Please Select a Record'
                return
        name = self.tree.item(self.tree.selection())['text']
        oldPrice = self.tree.item(self.tree.selection())['values'][0]
        self.new_Wind = Toplevel()
        self.new_Wind.title='EDIT PRODUCT'
# values name
        Label(self.new_Wind, text = 'Old Name:').grid(row = 0, column = 1)
        Entry(self.new_Wind, textvariable = StringVar(self.new_Wind, value = name), state = 'readonly').grid(row = 0, column = 2)

        Label(self.new_Wind, text = 'New Price:').grid(row = 1, column = 1)
        new_name = Entry(self.new_Wind)
        new_name.grid(row = 1, column = 2)

#  values price
        Label(self.new_Wind, text = 'Old Price:').grid(row = 2, column = 1)
        Entry(self.new_Wind, textvariable = StringVar(self.new_Wind, value = oldPrice), state = 'readonly').grid(row = 2, column = 2)

        Label(self.new_Wind, text = 'New Name:').grid(row = 3, column = 1)
        new_price= Entry(self.new_Wind)
        new_price.grid(row = 3, column = 2)

        Button(self.new_Wind, text = 'Update', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), oldPrice)).grid(row = 4, column = 2, sticky = W)
        self.new_Wind.mainloop()

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price,name, old_price)
        self.querys(query, parameters)
        self.new_Wind.destroy()
        self.messages['text'] = 'Record {} updated successfylly'.format(name, )
        self.get_Products()

if __name__ == '__main__':
        window = Tk()
        Product(window)
        window.mainloop()

