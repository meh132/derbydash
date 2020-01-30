# -*- coding: utf-8 -*-

import base64
import datetime
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
from functions import *
import plotly.graph_objs as go
import serial

# Input and upload libary
from dash.dependencies import Input, Output, State
import pandas as pd

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = None)
#resultsdf = pd.read_csv('resultsFile.csv')
resultsdf = pd.DataFrame(columns=['race', 'lane', 'car', 'name', 'time', 'place', 'den', 'category'])

# Read from CSV to load Races
races = pd.read_csv('Races.csv')
races = races.set_index('Race Number')


# Read list of racers and cars from CSV

racers = pd.read_csv('Racers.csv')
racers = racers.set_index('Number')


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.config.suppress_callback_exceptions = True
app.config['suppress_callback_exceptions'] = True

# Set up Tabs

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-2', children=[
        dcc.Tab(label='Setup', value='tab-1'),
        dcc.Tab(label='Race',  value='tab-2'),
        dcc.Tab(label='Results', value='tab-3'),
    ]),
    html.Div(id='tabs-content')
])


tab1markdown_text = '''
            ### Setup

            Need to set the lane time to have 4 places, 
            place value to have Number instead of letter
            and 

            '''

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return  html.Div([
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
            # connect usb
            html.Div(id='output-data-upload'),
            html.H2('Track Setup'),
            html.H3('Connect to Track'), 
            daq.StopButton(id='connect-button', buttonText='Connect'),
            html.Div(id='connect-results'),
            # default settings
            dcc.Markdown(children=tab1markdown_text),
            html.Button(id='setup-button'),
            html.H3(id='laneset-results'), 
            html.H3(id='placeset-results'),
            html.H3(id='decimal-results'),
            html.H3(id='timeout-results'),
             ])


    elif tab == 'tab-2':
        return html.Div(children=[
            dcc.Interval(
                id='interval-component',
                interval=10*1000, # in milliseconds
                n_intervals=0
            ),
           html.Div(id='main_cols',children=[
            html.Div(id='race', children=[
                daq.NumericInput(
                    id='my-daq-numericinput',
                    max=60,
                    value=1,
                    label='Race Number',
                    labelPosition='top',
                    min=1),
                daq.ToggleSwitch(
                    id='edit',
                    label='Editable',
                    value=False),
                html.Div(id='lanes', children=[
                    html.H3('Lanes'),   

                    html.Div(id='lane1', children=[
                        html.H3('Lane 1'),
                        html.Div([
                            daq.LEDDisplay(
                            id='time1',
                            value=0,
                            label='Time',
                            labelPosition='bottom',
                            size='40',
                            color="#FF5E5E",
                             backgroundColor="#000000"
                         )
                        ]),
                        html.Div([
                            html.H5(id='car1'),
                            html.H6(id='name1'),
                        ])                        
                    ], className = "three columns"),
                    html.Div(id='lane2', children=[
                        html.H3('Lane 2'),
                        html.Div([
                            daq.LEDDisplay(
                            id='time2',
                            value=0,
                            label='Time',
                            labelPosition='bottom',
                            size='40',
                            color="#FF5E5E",
                             backgroundColor="#000000"
                         ),
                        html.Div([
                            html.H5(id='car2'),
                            html.H6(id='name2'),
                        ]),
                        ])
                    ], className = "two columns"),
                    html.Div(id='lane3', children=[
                        html.H3('Lane 3'),
                        html.Div([
                            daq.LEDDisplay(
                            id='time3',
                            value=0,
                            label='Time',
                            labelPosition='bottom',
                            size='40',
                            color="#FF5E5E",
                             backgroundColor="#000000"
                         )
                        ]),
                        html.Div([
                            html.H5(id='car3'),
                            html.H6(id='name3'),
                        ]),                        
                    ], className = "two columns"),
                    html.Div(id='lane4', children=[
                        html.H3('Lane 4'),
                        html.Div([
                            daq.LEDDisplay(
                            id='time4',
                            value=0,
                            label='Time',
                            labelPosition='bottom',
                            size='40',
                            color="#FF5E5E",
                             backgroundColor="#000000"
                         ),
                        html.Div([
                            html.H5(id='car4'),
                            html.H6(id='name4'),
                        ]),                        
                        ])
                    ], className = "two columns"),
                ],className = "twelve columns"),     
                html.Hr(id='line'),
                html.H4('Upcoming Races', className="eight column"),         
                html.Div(id='next-race')], 
                    style={'font-size': '200%', 'margin': '80px' , 'text-align': 'center'},
                    className="eight columns")]), 
            # second column           
            html.Div(children=[
                
                daq.StopButton(id='button-results', buttonText='Get Results'),
                html.Div(id='results-button-output'),
                daq.StopButton(id='button-save', buttonText='Save Results'),
                html.Div(id='save-button-output'),
                #daq.StopButton(buttonText='Refresh leaderboard', id='Refresh'),
                html.H4('Fastest Single Race'),
                #generate_table(results_df, max_rows=15)
                #dash_table.DataTable(
                #    id='leadtable',
                #    columns=[{"name": i, "id": i} for i in resultsdf.columns],
                    #data=resultsdf.to_dict('records')
                #    ),  
                    ])
           
        ])
        
    elif tab == 'tab-3':
        #global results_df
        rf = resultsdf.groupby(['den','car', 'name'], as_index=False).agg({"time": "mean"}).sort_values(['den','time'], ascending=True)
        #rf['time'] = rf['time'].map('{:,.3f}'.format)
        return dash_table.DataTable(
            id='final-board',
            columns=[{"name": i, "id": i} for i in rf.columns],
        #columns=[['name','car','time']],
            data=rf.to_dict('records'),
            style_data_conditional=[
                {'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
                },
                {'if': {'column_id': 'time'},
                'backgroundColor': '#3D9970',
                'color': 'white',
                }
            ],
            style_as_list_view=True,
            )
        

## CAllbacks for Race

## update racer info
## Lane 2
@app.callback(
    [Output('car1', 'children'),
    Output('name1', 'children'),
    Output('car2', 'children'),
    Output('name2', 'children'),
    Output('car3', 'children'),
    Output('name3', 'children'),
    Output('car4', 'children'),
    Output('name4', 'children'),
    Output('edit','value') ],
    [Input('my-daq-numericinput', 'value')])
def update_racers(value):
    car1 = races.loc[value,'Lane 1']
    name1 = racers.loc[car1,'Name']
    car2 = races.loc[value,'Lane 2']
    name2 = racers.loc[car2,'Name']
    car3 = races.loc[value,'Lane 3']
    name3 = racers.loc[car3,'Name']
    car4 = races.loc[value,'Lane 4']
    name4 = racers.loc[car4,'Name']
    return car1,name1,car2,name2,car3,name3,car4,name4,False


### update times
@app.callback(
    [Output('time1', 'value'),
    Output('time2', 'value'),
    Output('time3', 'value'),
    Output('time4', 'value')],
    [Input('button-results', 'n_clicks'),
    Input('my-daq-numericinput', 'value')],
    [State('edit', 'value')])
def update_times(clicks,value,edit):
    if edit:
        #laneresults = ['1=1.1212a','2=1.2323b','3=1.1234c','4=1.4321d']
        
        laneresults = serialwrite('rg')
        #time1=1
        time1=laneresults[0][2:8]
        time2=laneresults[1][2:8]
        time3=laneresults[2][2:8]
        time4=laneresults[3][2:8]
   
    else:
        #time1=0
        time1=resultsdf[(resultsdf['race']==value) & (resultsdf['lane']==1)]['time']
        time2=resultsdf[(resultsdf['race']==value) & (resultsdf['lane']==2)]['time']
        time3=resultsdf[(resultsdf['race']==value) & (resultsdf['lane']==3)]['time']
        time4=resultsdf[(resultsdf['race']==value) & (resultsdf['lane']==4)]['time']
    return time1,time2,time3,time4

## Save Results
@app.callback(
    #[
    Output('save-button-output', 'children'),
    #Output('leadtable', 'data')],
    [Input(component_id='button-save', component_property='n_clicks'),
    ],
    [State('my-daq-numericinput', 'value'),
    State('time1', 'value'),
    State('time2', 'value'),
    State('time3', 'value'),
    State('time4', 'value'),
    State('edit', 'value')
    ])
def save_output(clicks,current_race,time1,time2,time3,time4,edit):
    #resultsdf = pd.DataFrame(columns=['race', 'lane', 'car', 'name', 'time', 'place', 'den', 'category'])
    global resultsdf
    times = [time1,time2,time3,time4]
    race = {}
    for lane in [1,2,3,4]:
        car = races.iloc[current_race-1,lane-1]
        name = racers.loc[car,'Name']
        den = racers.loc[car,'Den']
        category = racers.loc[car,'Category']
        time = times[lane-1]
        place = 1

        # Create results json
        details = {'race' : current_race , 'lane' : int(lane), 'car': str(car), 'name': name, 'time': time, 'place': place, 'den': den, 'category': category} 
        trackName = 'lane' + str(lane)
        race[trackName] = details
        
        # append to dg
        resultsdf = resultsdf.append(details, ignore_index=True)
    if edit:
        # write results 
        resultsdf.to_csv('newResults.csv')
        message = 'Race '+ str(current_race) +' Saved...'        # write results 
        #leader_df = results_df.groupby(['car', 'name'], as_index=False).agg({"time": "mean"}).sort_values('time', ascending=True)
        #leader_df['time'] = leader_df['time'].map('{:,.3f}'.format) 
        #data = leader_df.to_dict('records')
        
    else:
        message = 'cannot save'

    #resultsdf.to_csv('resultsFile.csv',mode='a', header=False)
    return  message#,data


## Next race details
@app.callback(
    Output('next-race', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_nextrace(value):
    df = races.loc[value+1:value+3]
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
        )  




## Callbacks for Track Setup tab

# Callback after upload 
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_uploads(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        # for testing load results
        #Plotlyresultsdf = pd.read_csv('./resultsFile.csv')
        # Read from CSV to load Races
        #races = pd.read_csv('Races.csv')
        #races = races.set_index('Race Number')
        # Read list of racers and cars from CSV
        #racers = pd.read_csv('Racers.csv')
        #racers = racers.set_index('Number')
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# callback for track connect
@app.callback(
    Output('connect-results', 'children'),
    [Input('connect-button', 'n_clicks')])
def connect__usb(value):
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = None)

    return ser.name


## CAll back for track set
@app.callback(
    [Output('laneset-results', 'children'),
    Output('placeset-results', 'children'),
    Output('decimal-results', 'children'),
    Output('timeout-results', 'children')],
    [Input('setup-button', 'n_clicks')])
def setup_output(value):
    laneset = serialwrite('on4')
    placeset = serialwrite('ol1')
    decimalset = serialwrite('on4')
    timeoutset = serialwrite('or')
    return laneset,placeset,decimalset,timeoutset


def serialwrite(code):
    command = code +'\r\n'
    newcommand = command.encode('ascii')
    ser.write(newcommand)
    results = ser.readline()
    #laneresults = results.decode().split()
    #print(laneresults)
    return results.decode().split()



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)