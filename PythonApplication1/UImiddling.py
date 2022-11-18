import PySimpleGUI as sg
import MatchFiles
import CalculateMidPoint
import ExtractExif
import visualInterface

def StartMIdUi():
    sg.theme('Dark Grey 13')

    To_middle_column = [
            [        
                sg.Text('Offset'),
                sg.In(),
                sg.OK(key="-OFFSET-")
            ],
            [
              sg.Text('Filename'),
              sg.In(), sg.FileBrowse(),
              sg.OK(key="-ENTERFILE-"), sg.Cancel()
            ],
             [        
                sg.Text('Result File Name'),
                sg.In(), sg.FolderBrowse(),
                sg.OK(key="-RESULT-")
            ],
            [        
                sg.Text('Result File Name For Calculated Points'),
                sg.In(), sg.FolderBrowse(),
                sg.OK(key="-RESULTCALC-")
            ],
            [
                sg.Button('Run the program',key = "-RUN-")
            ]
    ]


    layout = [To_middle_column]

    window = sg.Window('Get filename example', layout)

    offset =.0
    path = ""
    resultPath = ""
    resultPathCalc = ""
    name = ""
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-OFFSET-":
            offset = int(values[0])/100
            print(offset)
        if event == "-ENTERFILE-":
            path = values[1]
            arr = path.split('/')
            name = arr[len(arr)-1]
            print(name)
            print(path)
        if event == "-RESULT-":
            resultPath = values[2]
            resultPath+= "/Done-" + name
            print(resultPath)
        if event == "-RESULTCALC-":
            resultPath = values[2]
            resultPath+= "/DoneCALC-" + name
            print(resultPathCalc)
        if event == "-RUN-":
            print("running the scripts")
            CalculateMidPoint.calculateMidPointFunc(path,resultPath,resultPathCalc,offset)
        
    
    window.close()
