import PySimpleGUI as sg
sg.set_options(font=("Helvetica", 14))
sg.theme('DarkBlue2')

def factorial(num):
    f=1
    for i in range(int(num),1,-1):
        f*=i
    return f

layout = [
    [sg.Text(size=(13,2),background_color='white',key='-dis-',text_color='black'),sg.Button('C',button_color='red',size=(4,1))],
    [sg.Button('!',size=(3,1)),sg.Button('(',size=(1,1)),sg.Button(')',size=(1,1)),sg.Button('<-',size=(3,1),button_color='red'),sg.Button('/',size=(4,1))],
    [sg.Button('7',size=(3,1)),sg.Button('8',size=(3,1)),sg.Button('9',size=(3,1)),sg.Button('X',size=(4,1))],
    [sg.Button('4',size=(3,1)),sg.Button('5',size=(3,1)),sg.Button('6',size=(3,1)),sg.Button('-',size=(4,1))],
    [sg.Button('1',size=(3,1)),sg.Button('2',size=(3,1)),sg.Button('3',size=(3,1)),sg.Button('+',size=(4,1))],
    [sg.Button('^',size=(3,1)),sg.Button('0',size=(3,1)),sg.Button('.',size=(3,1)),sg.Button('=',size=(4,1),button_color='grey')],
]
window = sg.Window("Calculator",layout)

while(True):
    event, values = window.read()

    if event in  (None, 'Exit'):
        break

    if event == '<-':
        text = window['-dis-']
        e = text.get()
        text.update(e[0:len(e)-1])


    if event == '!':
        text = window['-dis-']
        text.update(text.get()+' !')
    if event == '+':
        text = window['-dis-']
        text.update(text.get()+' + ')
    if event == '-':
        text = window['-dis-']
        text.update(text.get()+' - ')
    if event == 'X':
        text = window['-dis-']
        text.update(text.get()+' * ')
    if event == '(':
        text = window['-dis-']
        text.update(text.get()+' ( ')
    if event == ')':
        text = window['-dis-']
        text.update(text.get()+' ) ')
    if event == '/':
        text = window['-dis-']
        text.update(text.get()+' / ')
    if event == '.':
        text = window['-dis-']
        text.update(text.get()+'.')
    if event == '9':
        text = window['-dis-']
        text.update(text.get()+'9')
    if event == '8':
        text = window['-dis-']
        text.update(text.get()+'8')
    if event == '7':
        text = window['-dis-']
        text.update(text.get()+'7')
    if event == '6':
        text = window['-dis-']
        text.update(text.get()+'6')
    if event == '5':
        text = window['-dis-']
        text.update(text.get()+'5')
    if event == '4':
        text = window['-dis-']
        text.update(text.get()+'4')
    if event == '3':
        text = window['-dis-']
        text.update(text.get()+'3')
    if event == '2':
        text = window['-dis-']
        text.update(text.get()+'2')
    if event == '1':
        text = window['-dis-']
        text.update(text.get()+'1')
    if event == '0':
        text = window['-dis-']
        text.update(text.get()+'0')
    if event == '^':
        text = window['-dis-']
        text.update(text.get()+'**')
    if event == '=':
        text = window['-dis-']
        if "!" in text.get():
            n = float(text.get().split()[0])
            if n.is_integer() and len(text.get().split())==2 and len(str(n))<=3:
                text.update(factorial(int(n)))
            else:
                sg.Popup('something went wrong', keep_on_top=True)
                text.update('')
        else:
            try:
                text.update(eval(text.get()))
            except (SyntaxError, NameError, TypeError, ZeroDivisionError):
                sg.Popup("something went wrong",keep_on_top=True)
                pass
    if event == 'C':
        text = window['-dis-']
        text.update('')
window.close()
