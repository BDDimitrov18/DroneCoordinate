import PySimpleGUI as sg
import os
import calcTimeForPoints

def runUi():
# Define the layout for the GUI
    layout = [
        [sg.Text('Input Path'), sg.Input(key='input_path'), sg.FileBrowse()],
        [sg.Text('Output Path'), sg.Input(key='output_path'), sg.FolderBrowse()],
        [sg.Text('Result Filename'), sg.Input(key='result_filename')],
        [sg.Text('Start Hour (HH:MM:SS)'), sg.Input(key='start_hour')],
        [sg.Text('Start Date (DD.MM.YYYY)'), sg.Input(key='start_date')],
        [sg.Button('Run Program')]
    ]

    # Create the window
    window = sg.Window('GNSS Data Processor', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Run Program':
            input_path = values['input_path']
            output_path = os.path.join(values['output_path'], values['result_filename'])
            start_hour = values['start_hour']
            start_date = values['start_date']
        
            # Call the calcTimeForPoints function with the provided inputs
            calcTimeForPoints(input_path, output_path, start_date, start_hour)
            sg.popup('Program completed successfully!')

    # Close the window
    window.close()
