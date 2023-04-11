import PySimpleGUI as psg
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if not os.path.isfile('./data.csv'):
    f = open('./data.csv',encoding="utf-8-sig",mode='w+')
    f.write("Date,Reason,Category,Amount")
    
data = []
with open("./data.csv",encoding="utf-8-sig") as f:
    data = f.read().split('\n')
f.close()
Headers = data[0].split(",")
Rows = [row.split(',') for row in data[1::] if len(row)>0]

total = sum([float(r[3]) for r in Rows])

def sort_help(dt):
    date = dt[0].split("-")
    return int(date[1]),int(date[0])

Rows.sort(key=sort_help)

def block_focus(window):
    for key in window.key_dict:    # Remove dash box of all Buttons
        element = window[key]
        if isinstance(element, psg.Button):
            element.block_focus()

def popup_add_expense():
    layout = [
        [psg.Text('Date: ',size=(10,1)), psg.InputText(key='Date',disabled=True,size=(31,1)),psg.CalendarButton("Select Date",close_when_date_chosen=True, target="Date", format='%d-%m-%Y',size=(10,1),font="arial 15")],
        [psg.Text('Reason: ',size=(10,1)), psg.InputText(key='Reason',size=(40,1))],
        [psg.Text('Category: ',size=(10,1)), psg.Combo(["drink","flat","food","other","travel"],key='Category',size=(39,1),default_value="Click to Choose",readonly=True)],
        [psg.Text('Amount: ',size=(10,1)), psg.InputText(key='Amount',size=(40,1))],
        [psg.Button("Add Expense to data",key="Add",size=(50,1))]
    ]
    window = psg.Window("Add new expense", layout, use_default_focus=False, finalize=True, modal=True)
    block_focus(window)
    event, values = window.read()
    window.close()
    return [values['Date'],values['Reason'],values['Category'],values['Amount']] if event == 'Add' else None

psg.set_options(font=('Consolas', 16))

psg.theme("DarkTeal2")

read_table = psg.Table(values=Rows,headings=Headers,
                        auto_size_columns=True,
                        display_row_numbers=False,
                        justification='center', key='-TABLE-',
                        selected_row_colors='yellow on blue',
                        enable_events=True,
                        expand_x=True,
                        expand_y=True,
                        enable_click_events=True
                     )

months = ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
categories = ["All","food","flat","drink","other","travel"]

layout = [ 
          [psg.Text("Expense Tracker",font=" Arial 30 bold",justification='center',size=(1500,1))],
          [psg.Combo(months,key="Month",default_value="All",size=(30,1),readonly=True),psg.Button("Filter Month",key="filmonth",size=(30,1),),psg.Combo(categories,key="Category",default_value="All",size=(30,1),readonly=True),psg.Button("Filter Category",key="filcat",size=(30,1))],
          [psg.Button("Filter by Month and Category",key="filmthcat",size=(150,1))],
          [read_table],
          [psg.Text("Total Amount : ",font="roboto 20"),psg.InputText(str(round(total,2)),key='total',disabled=True,font="Roboto 20",size=(100,1))],
          [psg.Button("Add Expense ➕ ",key="Add"),psg.Text(" ",size=(90,1)),psg.Button("Save File 💾",key="Save")]
         ]



window = psg.Window("Expense Tracker",layout,size=(1500,800),resizable=True,icon=resource_path("rupee-indian.ico"))

while True:
    event, values = window.read(timeout=1000)
    
    if event in  (None, 'Exit'):
        ch = psg.popup_yes_no("Want to save ?",title="save before exit")
        if ch=="Yes":
            s = []
            s.append(",".join(Headers))
            for x in Rows:
                s.append(",".join(x))

            f = open("./data.csv",mode="w+",encoding="utf-8-sig")
            f.write("\n".join(s))
            f.close()
            psg.popup("Saved Succesfully")
        break
    
    if event=="filmonth":
        filrows = []
        if values['Month']=="All":
            filrows=Rows
            filtotal = total
            window["-TABLE-"].update(filrows)
            window['total'].update(round(filtotal,2))
            
        if values['Month']!="All":
            mindex = months.index(values["Month"])
            filrows = [x for x in Rows if int(x[0].split('-')[1])==mindex]
            if len(filrows)==0:
                psg.popup("No Records Found for month {mth}".format(mth=values["Month"]))
            filtotal = sum([float(r[3]) for r in filrows])
            window["-TABLE-"].update(filrows)
            window["total"].update(round(filtotal,2))

    if event=="filcat":
        filrows = []
        
        print(values['Category'])
        
        if values['Category']=="All":
            filrows=Rows
            filtotal = total
            window["-TABLE-"].update(filrows)
            window['total'].update(round(filtotal,2))
            
        if values['Category']!="All":
            fcat = values["Category"]
            filrows = [x for x in Rows if x[2]==fcat]
            
            filtotal = sum([float(r[3]) for r in filrows])
            window["-TABLE-"].update(filrows)
            window["total"].update(round(filtotal,2))
        
    if event=="filmthcat":
        if values['Category']!="All" and values['Month']!="All":
            mindex = months.index(values["Month"])
            fcat = values["Category"]
            filrows = [x for x in Rows if x[2]==fcat and int(x[0].split('-')[1])==mindex]
            filtotal = sum([float(r[3]) for r in filrows])
            window["-TABLE-"].update(filrows)
            window["total"].update(round(filtotal,2))
        
        if values['Category']=="All" and values['Month']=="All":
            filrows = Rows
            filtotal = sum([float(r[3]) for r in filrows])
            window["-TABLE-"].update(filrows)
            window["total"].update(round(filtotal,2))
            
    
    if event=="Add":
        new_row = popup_add_expense()
        if new_row==None:
            print("Canceled Entry")
        elif "" not in new_row and new_row[3].isdigit():
            Rows+=[new_row]
            Rows.sort(key=sort_help)
            total += float(new_row[3]) 
            window['-TABLE-'].update(Rows)
            window['total'].update(round(total,2))
            psg.popup("Added Succesfuly")
        else:
            psg.popup("Something Went Wrong")
    
    if event=="Save":
        s = []
        s.append(",".join(Headers))
        for x in Rows:
            s.append(",".join(x))

        f = open("./data.csv",mode="w+",encoding="utf-8-sig")
        f.write("\n".join(s))
        f.close()
        psg.popup("Saved Succesfully")



window.close()

