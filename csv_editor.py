# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:12:13 2023

@author: omkar
"""

import pandas as pd
import PySimpleGUI as psg

class Product:
    product_code = 0
    product_name = ""
    product_description = ""
    product_supplier = ""
    product_price = ""
    
    def __init__(self,code,name,desc,supplier,price):
        self.product_code = code
        self.product_name = name
        self.product_description = desc
        self.product_supplier = supplier
        self.product_price = price
    
    def info(self):
        print(''' 
                Product Code : {0}
                Product Name : {1}
                Product Description : {2} 
                Product Supplier : {3}
                Product Price : {4}
              '''.format(self.product_code,self.product_name,self.product_description,self.product_supplier,self.product_price))
    
    def product(self):
        return {
                "Product Code" : self.product_code,
                "Product Name" : self.product_name,
                "Product Description" : self.product_description ,
                "Product Supplier" : self.product_supplier,
                "Product Price" : self.product_price
        }
    
class ProductDemo:
    productlist = []
    supplist = set([''])
    def addproduct(self,product):
        self.productlist.append(product.product())
        self.supplist.add(product.product()['Product Supplier'])
    
    def displayproducts(self):
        p = []
        for product in self.productlist:
            p.append(product.values())
        return [list(pval) for pval in p]
    
    def display_product_for_supplier(self,supplier):
        plistsupp = []
        for product in self.productlist:
            if product['Product Supplier']==supplier:
                plistsupp.append(product.values())
        return [list(pval) for pval in plistsupp]
            
        

# prod1 = Product(1,"ABC","CDE","FGH",20.3)
# prod2 = Product(2,"ABdfgC","CDE","FGH",20.3)
# prod3 = Product(3,"asd","CDE","www",20.3)
# prod4 = Product(4,"ABC","CDE","ee",20.3)

productmanager = ProductDemo()
# productmanager.addproduct(prod1)
# productmanager.addproduct(prod2)
# productmanager.addproduct(prod3)
# productmanager.addproduct(prod4)

# print(productmanager.displayproducts())

productmanager.display_product_for_supplier("FGH")

psg.set_options(font=("Helvetica", 14))

toprow = "Product Code,Product Name,Product Description,Product Supplier,Product Price".split(",")
#rows = productmanager.displayproducts()

r = pd.read_csv('ProductData.csv',index_col=0)
r
rows =r.values.tolist()

supplist = list(set([x[3] for x in rows]))
supplist


tbl1 = psg.Table(values=rows, headings=toprow,
                auto_size_columns=True,
                display_row_numbers=False,
                justification='center', key='-TABLE-',
                selected_row_colors='yellow on blue',
                enable_events=True,
                expand_x=True,
                expand_y=True,
                enable_click_events=True)


supplist += productmanager.supplist

supplist = list(set(supplist))

layout = [
    [psg.Text('Product Code : '),psg.Input(key='pcode')],
    [psg.Text('Product Name : '),psg.Input(key='pname')],
    [psg.Text('Product Description : '),psg.Input(key='pdesc')],
    [psg.Text('Product Supplier : '),psg.Input(key='psupp')],
    [psg.Text('Product Price : '),psg.Input(key='pprice')],
    [psg.Button('Add')],
    [psg.Button('Filter'),psg.Combo(list(supplist),key='-supp-',size=(6,1))],
    [tbl1]
]
window = psg.Window("Test",layout)
while True:
    event,values = window.read()
    if event in  (None, 'Exit'):
        break
    
    if event=='Add':
        if values['pcode']!='' and values['pname']!='' and values['pdesc']!='' and values['psupp']!='' and values['pprice']!='':
            prod = Product(values['pcode'], values['pname'], values['pdesc'], values['psupp'], values['pprice'])
            productmanager.addproduct(prod)
            supplist += list(productmanager.supplist)
            supplist = list(set(supplist))
            rows += productmanager.displayproducts()
            window['-TABLE-'].update(rows)
            window['-supp-'].update(values=supplist)
        
    if event=='Filter':
        if values['-supp-']=='':
            rows += productmanager.displayproducts()
            window['-TABLE-'].update(rows)
        else:
            rows += productmanager.display_product_for_supplier(values['-supp-'])
            window['-TABLE-'].update(rows)
    
    if '+CLICKED+' in event:
        x=event[2][0]
        window['pcode'].Update(rows[x][0])
        window['pname'].Update(rows[x][1])
        window['pdesc'].Update(rows[x][2])
        window['psupp'].Update(rows[x][3])
        window['pprice'].Update(rows[x][4])


window.close()

s_t_file = pd.DataFrame(rows)
s_t_file.columns=['Product Code','Product Name','Product Description','Product Supplier','Product Price']
s_t_file.to_csv('ProductData.csv')
