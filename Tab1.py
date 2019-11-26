import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# Genarte table
def gen_tab1():
    return html.Div([
            html.H2('Race Setup'),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '80%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=True
            ),
            html.Div(id='output-data-upload'),
            html.H2('Track Setup'),
            html.H3('Connect to Track'), 
            html.Button('Connect', id='connect-button'),
            html.H3('Lane Order'),
            html.Button('Reverse Lanes', id='lane-reverse-button'),
    ]) 


def serialwrite(code):
    command = code +'\r\n'
    newcommand = command.encode('ascii')
    #ser.write(newcommand)
    #results = ser.readline()
    results = 'xxx'
    #laneresults = results.decode().split()
    #print(laneresults)
    return results