import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq

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
            daq.StopButton(id='connect-button', buttonText='Connect'),
            html.Div(id='connect-results'),
            
            html.H3('Lane Order'),
            html.Button('Reverse Lanes', id='lane-reverse-button'),
            # Track lanes  'on' reads, 'on4' sets
            dcc.RadioItems(
                id='lane-number',
                options=[
                    {'label': '4 Lanes', 'value': 'on4'},
                    {'label': '6 Lanes', 'value': 'on6'},
                ],
                value='on4', 
                labelStyle={'display': 'inline-block'}
                ) ,

             # Lane Character 'ol' reads, 'ol1' sets to '1'
            dcc.RadioItems(
                id='lane-character',
                options=[
                    {'label': 'Set to Digit', 'value': 'ol1'},
                    {'label': 'Set to Letter', 'value': 'ol2'},
                ],
                #value='ol1', 
                labelStyle={'display': 'inline-block'}
                ) ,
                        
            # Lane Place character 'op' reads, 'op2' sets to '1'
            dcc.RadioItems(
                id='place-character',
                options=[
                    {'label': '4 Lanes', 'value': 'op2'},
                    {'label': '6 Lanes', 'value': '6'},
                ],
                value='op2', labelStyle={'display': 'inline-block'}
                ) ,
           

            # om - lane mask, 'om0' resets to all lanes


            # od - decimal places 3,4,5 options
            dcc.RadioItems(
                id='decimal-places',
                options=[
                    {'label': '3 digits', 'value': 'od3'},
                    {'label': '4 digits', 'value': 'od4'},
                    {'label': '5 digits', 'value': 'od5'},
                ],
                value='od4', labelStyle={'display': 'inline-block'}
                ) ,

            # or reset delay - 0, 10, 30
            dcc.RadioItems(
                id='reset-delay',
                options=[
                    {'label': '3 digits', 'value': 'or0'},
                    {'label': '4 digits', 'value': 'or10'},
                    {'label': '5 digits', 'value': 'or30'},
                ],
                value='or', labelStyle={'display': 'inline-block'}
                ) ,
            # ov - reverse lane numbering
            dcc.RadioItems(
                id='reset-delay',
                options=[
                    {'label': '1,2,3,4', 'value': 'ov0'},
                    {'label': '4,3,2,1', 'value': 'ov1'},
                ],
                value='ov1', labelStyle={'display': 'inline-block'}
                ) ,          
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

  #
  # reverse lane order = 'ov1'+'\r\n'