#notepad

import PySimpleGUI as psg

layout = [[psg.Text("Choose a file: "),psg.Input("Select a file please",key='fpath',size=(180,1)), psg.Button("Browse")],
          [psg.Multiline('open a file to view here', key='-filecontent-',size=(200,50))],
          [psg.Button("Save"),psg.Button("Cancel")]
          ]
window = psg.Window('Simple Notepad', layout,icon="./icon.ico")

psg.theme("LightBrown3")

while True:
    event, values = window.read()
    if event in (None,"Exit"):
        break
    elif event == "Browse":
        filepath = psg.popup_get_file('', multiple_files=True, no_window=True)
        window['fpath'].update(filepath)
        with open(filepath[0]) as fp:
            window['-filecontent-'].update(fp.read())
        window.set_title(filepath[0])
    elif event== "Save":
        if values['fpath'] in ("","Select a file"):
            psg.popup("Select a file please")
        else:
            f = open(filepath[0],"w+")
            x=values['-filecontent-']
            f.writelines(x)
            psg.popup("Saved content to "+filepath[0])
            f.close()
    elif event== "Cancel":
        window['-filecontent-'].update("open a file to view here")
        window['fpath'].update("Select a file please")
            
