import PySimpleGUI as sg
import datetime

class DataWareHouse:
    DW = {}
    def __init__(self,data):
        self.DW = data

    def check_if_exist_and_active(self,customerkey):
        for i in self.DW:
            if(self.DW[i]['CustomerKey']==customerkey):
                if(self.DW[i]['isActive']==1):
                    return i
        return False


    def insert_data(self,data):
        dt = datetime.datetime.now()
        date = "-".join(str(x) for x in [dt.year,dt.month,dt.day])
        if self.check_if_exist_and_active(data['CustomerKey'])==False:
            self.DW[len(self.DW)+1] = {
                                        "SurrogateKey":len(self.DW)+1,
                                        "CustomerKey":data['CustomerKey'],
                                        "CustomerAddress":data['CustomerAddress'],
                                        "isActive":1,
                                        "ValidFrom":date,
                                        "ValidTo":"9999-12-31",
                                    }
        else:
            i = self.check_if_exist_and_active(data['CustomerKey'])

            if self.DW[i]['CustomerAddress']!=data["CustomerAddress"]:
                
                self.DW[i]['isActive']=0
                self.DW[i]['ValidTo']=date

                self.DW[len(self.DW)+1] = {
                                            "SurrogateKey":len(self.DW)+1,
                                            "CustomerKey":data['CustomerKey'],
                                            "CustomerAddress":data['CustomerAddress'],
                                            "isActive":1,
                                            "ValidFrom":date,
                                            "ValidTo":"9999-12-31",
                                        }

    def view_records(self):
        return self.DW

    def get_record_list(self):
        records = []
        for i in self.DW:
            record = list(self.DW[i].values())
            records.append(record)
        return records

dw = DataWareHouse({
    1:{
        "SurrogateKey":1,
        "CustomerKey":1,
        "CustomerAddress":"82 Margate Drive, Sheffield, S4 8FQ",
        "isActive":1,
        "ValidFrom":"2022-01-19",
        "ValidTo":"9999-12-31",
      },
    2:{
        "SurrogateKey":2,
        "CustomerKey":2,
        "CustomerAddress":"135 High Barns, Ely, CB7 4RH",
        "isActive":1,
        "ValidFrom":"2022-01-19",
        "ValidTo":"9999-12-31",
      },
    3:{
        "SurrogateKey":3,
        "CustomerKey":3,
        "CustomerAddress":"39 Queen Annes Drive, Bedale, DL8 2EL",
        "isActive":1,
        "ValidFrom":"2022-01-19",
        "ValidTo":"9999-12-31",
      }
})


# dw.insert_data({'CustomerKey':1,'CustomerAddress':'82 Margate Drive, Sheffield, S4 8FQ'})
# dw.insert_data({'CustomerKey':2,'CustomerAddress':'135 High Barns, Ely, CB7 4RH, DL8 2EL'})
# dw.insert_data({'CustomerKey':3,'CustomerAddress':'Guyzance Cottage, Guyzance, NE65 9AF'})
# dw.insert_data({'CustomerKey':4,'CustomerAddress':'322 Fernhill, Mountain Ash, CF45 3EN'})
# dw.insert_data({'CustomerKey':5,'CustomerAddress':'381 Southborough Lane, Bromley, BR2 8BQ'})

# dw.view_records()

sg.set_options(font=("Arial Bold", 14))
toprow = "Surrogate Key, Customer Key, Customer Address, isActive, ValidFrom, ValidTo".split(",")
sg.theme('DarkBrown4')   # Add a touch of color

rows = dw.get_record_list()
tbl1 = sg.Table(values=rows, headings=toprow,
                auto_size_columns=True,
                display_row_numbers=False,
                justification='center', key='-TABLE-',
                selected_row_colors='yellow on blue',
                enable_events=True,
                expand_x=True,
                expand_y=True,
                enable_click_events=True)

layout = [  [sg.Text('Add New Record')],
            [sg.Text('Enter Customer Key : '), sg.HSeparator(pad=(10,0)),sg.Input(key='-CustKey-')],
            [sg.Text('Enter Customer Address : '), sg.HSeparator(pad=(10,0)),sg.Input(key='-CustAdd-')],
            [sg.Button('Add')],
            [tbl1],
            [sg.Button('Exit')]
        ]
window = sg.Window("Table Test",layout, resizable=True)

while True:
    event, values = window.read(timeout=1000)
    
    if event in  (None, 'Exit'):
        break

    if '+CLICKED+' in event:
        x = event[2][0]
        window['-CustKey-'].update(rows[x][1])
        window['-CustAdd-'].update(rows[x][2])
        
    
    if event == 'Add':
        dw.insert_data({'CustomerKey':int(values['-CustKey-']),'CustomerAddress':values['-CustAdd-']})
        rows = dw.get_record_list()
        window['-TABLE-'].update(rows)
  
window.close()

