from tkinter import *
import tkinter.ttk as ttk
import csv

root = Tk()
root.title("Python - Import CSV File To Tkinter Table")
width = 500
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

TableMargin = Frame(root, width=250)
TableMargin.pack(side=TOP)

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("Employye ID", "Name", "Date",'Registration Time'), height=300, selectmode="extended",
                    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('Employye ID', text="Employye ID", anchor=W)
tree.heading('Name', text="Name", anchor=W)
tree.heading('Date', text="Date", anchor=W)
tree.heading('Registration Time', text="Time", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=120)
tree.column('#2', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.pack()
with open('./RegisteredEmployees/RegisteredEmployees.csv') as f:
  reader = csv.DictReader(f, delimiter=',')
  for row in reader:
    emp_id = row['Employye ID']
    name = row['Name']
    dt = row['Date']
    ti = row['Registration Time']
    tree.insert("", 0, values=(emp_id, name, dt,ti),tags = ('oddrow',))
    tree.tag_configure('oddrow', background='black',foreground = 'white',font=('times', 14, ' bold '))
root.mainloop()