import PySimpleGUI as psg
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns




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

def monthdata(month,Headers,Rows):
    rows = [[x[0],x[1],x[2],float(x[3])] for x in Rows if int(x[0].split('-')[1])==month]
    new_df = pd.DataFrame(rows,columns=Headers)    
    return new_df.groupby('Category',as_index =False).sum(numeric_only=True),new_df.groupby('Date',as_index =False).sum(numeric_only=True)

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


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def popup_show_graphs(fig):
    layout = [
        [psg.Canvas(key='figcanvas')]
    ]
    window = psg.Window("Expense Tracker",layout,resizable=True,finalize=True)
    draw_figure(window['figcanvas'].TKCanvas, fig)
    block_focus(window)
    event, values = window.read()
    window.close()


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
          [psg.Button("Add Expense ➕ ",key="Add"),psg.Button("Show Graph for Month",size=(90,1),key="show"),psg.Button("Save File 💾",key="Save")]
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
    
    if event=="show":
        if values['Month']!="All":
            
            mindex = months.index(values["Month"])


            categoryexpense,daywise = monthdata(mindex,Headers,Rows)
            
            if len(categoryexpense)>0:
                a4_dims = (30.7, 10.27)
                fig, axs = plt.subplots(ncols=3,figsize=a4_dims)
                
                catex = sns.barplot(categoryexpense,x='Category',y='Amount',ax=axs[0])
                catex.axes.set_title("Category wise Amount",fontsize=40)
                catex.set_xlabel("Category",fontsize=30)
                catex.set_ylabel("Amount",fontsize=20)
                catex.bar_label(catex.containers[0])
                catex.tick_params(labelsize=30)

                dayexp = sns.barplot(daywise,x='Date',y='Amount',ax=axs[1])
                dayexp.axes.set_title("Date Wise Amount",fontsize=40)
                dayexp.set_xlabel("Date",fontsize=12)
                dayexp.set_ylabel("Amount",fontsize=20)
                dayexp.set_xticklabels(labels=daywise['Date'].to_list(),rotation=90)
                dayexp.bar_label(dayexp.containers[0],fontsize=12)
                dayexp.tick_params(labelsize=10)
                
                piplt = axs[2].pie(categoryexpense['Amount'],labels=categoryexpense['Category'],explode=(0, 0, 0,0, 0.1),textprops={'fontsize': 28})  
                axs[2].set_title("Category Pie Chart",fontsize=40)
                
                popup_show_graphs(fig)

            else:
                psg.popup("No Records Found")
        else:
            psg.popup("Select a month")
        



window.close()

