import PySimpleGUI as sg
import MatchFiles
import CalculateMidPoint
import ExtractExif
import visualInterface
import MatchFiles

def matchUi():
    sg.theme('Dark Grey 13')

    To_middle_column = [
            [
              sg.Text('Done File Name'),
              sg.In(), sg.FileBrowse(),
              sg.OK(key="-ENTERFILEDONE-"), sg.Cancel()
            ],
            [
              sg.Text('To match File Name'),
              sg.In(), sg.FileBrowse(),
              sg.OK(key="-ENTERFILEMATCH-"), sg.Cancel()
            ],
            [        
                sg.Text('Result File Name'),
                sg.In(), sg.FolderBrowse(),
                sg.OK(key="-RESULT-")
            ],
            [
                sg.Button('Run the program',key = "-RUN-")
            ]
    ]


    layout = [To_middle_column]

    window = sg.Window('Get filename example', layout)

    donePath = ""
    matchPath =""
    resultPath = ""
    name = ""
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-ENTERFILEDONE-":
            donePath = values[0]
            arr = donePath.split('/')
            name = arr[len(arr)-1]
            print(donePath)
        if event == "-ENTERFILEMATCH-":
            matchPath = values[1] 
            print(matchPath)
        if event == "-RESULT-":
            resultPath = values[2]
            resultPath+= "/matched-" + name
            print(resultPath)
        if event == "-RUN-":
            print("running the scripts")
            MatchFiles.match(donePath,matchPath,resultPath)

        
    
    window.close()
