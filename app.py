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

# Input and upload libary
from dash.dependencies import Input, Output, State
import pandas as pd

#from callbacks import *
#from track import *
from Tab1 import *
#from Tab2 import *
from Tab3 import *
from load import *


## Colors for winners
colors = ["#F0FFF0","#ffd700","#c0c0c0","#cd7f32","#F0FFF0"]


#resultsdf = pd.DataFrame(columns=['race', 'lane', 'car', 'name', 'time', 'place', 'den', 'category'])
#resultsdf = pd.read_csv('./resultsFile.csv')
#resultsdf.to_csv('resultsFile4016.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

# for dyanmic
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


## Callbacks
# Render Tabs

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            gen_tab1()

        ])
    elif tab == 'tab-2':
        return html.Div(children=[
            dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        ),
            gen_tab2()  # each tab reloads the csv file
        ])
        
    elif tab == 'tab-3':
        return html.Div(children=[
            gen_tab3() # each tab reloads the csv file
            
        ])



## Generate Tab 2
# Generate table
def gen_tab2():
    #resultsdf = pd.read_csv('./resultsFile.csv')
    #resultsdf = pd.DataFrame(columns=['race', 'lane', 'car', 'name', 'time', 'place', 'den', 'category'])
    return html.Div(id='main_cols',children=[
        html.Div(id='race', children=[
            daq.NumericInput(
                id='my-daq-numericinput',
                max=60,
                value=1,
                label='Race Number',
                labelPosition='top',
                min=1), 
            html.Div(id='lanes', children=[
            html.H3('Lanes'),
            #html.H3(results_df.loc['race']),
                html.Div(id='lane1', children=[
                    html.H3('Lane 1'),
                    html.Div(id='name1'),
                    html.Div(id='time1')
                 ], className="two columns"),
                html.Div(id='lane2', children=[
                    html.H3('Lane 2'),
                    html.Div(id='name2'),
                    html.Div(id='time2')
                 ], className="two columns"),
                html.Div(id='lane3', children=[
                    html.H3('Lane 3'),
                    html.Div(id='name3'),
                    html.Div(id='time3')
                 ], className="two columns"),
                html.Div(id='lane4', children=[
                    html.H3('Lane 4'),
                    html.Div(id='name4'),
                    html.Div(id='time4')
                 ], className="two columns"),
            ], 
            className="twelve columns",
            style={'border': 'solid', 'text-align': 'center'}),
            daq.StopButton(id='button-results', buttonText='Get Results'),
            html.Div(id='results-button-output'),
            daq.StopButton(id='button-save', buttonText='Save Results'),
            html.Div(id='save-button-output'),
            daq.StopButton(buttonText='Refresh leaderboard', id='Refresh'),
        #html.Div(id='race-controls', children=[
        #    daq.StopButton(id='button-results', buttonText='Get Results'),
        #    html.Div(id='results-button-output'),
            #html.Button('Force Race End', id='button-end'),
            #html.Button('Next Race', id='button-next'),
        #    ], 
        #    style={'margin': '80px' , 'text-align': 'center'},
        #    className="eight columns"), 
        html.H4('Upcoming Races', className="eight column"),         
        html.Div(id='next-race')], 
            style={'font-size': '200%', 'margin': '80px' , 'text-align': 'center'},
            className="eight columns"), 
        html.H4('Fastest Single Race'),
        html.Div(id='leader-board',
            className="three columns",        
            style={'font-size': '150%','border': 'solid'}),
            ],    
        )


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




# Connect Call back should read and set statuses of radio buttons


# callback for race change
# update cars for a lane, lanes will pick up their value
### how do we update more values than children, can we call out specific values
## can we update style to show winner??
  

## lane 1
@app.callback(
    Output('name1', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_lane1(value):
    carNum = races.loc[value,'Lane 1']
    name = racers.loc[carNum,'Name']
    return html.Div([
        html.H5(carNum ),
        html.H4(name),
        ], style={'background-color': 'grey','border': 'solid', 'text-align': 'center'})


@app.callback(
    Output('time1', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_time1(value):
    #time = resultsdf[(resultsdf['race']==value) & (resultsdf['lane']==1)]['time']
    return html.Div([
        daq.LEDDisplay(
            id='lane1-leddisplay',
            value=0,
            label='Time',
            labelPosition='bottom',
            size='40',
            color="#FF5E5E",
            backgroundColor="#000000"
            )
        ])


## Lane 2
@app.callback(
    Output('name2', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_lan2(value):
    carNum = races.loc[value,'Lane 2']
    name = racers.loc[carNum,'Name']
    return html.Div([
        html.H5(carNum ),
        html.H4(name),
        ], style={'background-color': 'grey','border': 'solid', 'text-align': 'center'})



@app.callback(
    Output('time2', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_time2(value):
    #time = resultsdf[(resultsdf['race']==value) & (resultsdf['lane']==2)]['time']
    return html.Div([
        daq.LEDDisplay(
            id='lane2-leddisplay',
            value=0,
            label='Time',
            labelPosition='bottom',
            size='40',
            color="#FF5E5E",
            backgroundColor="#000000"
            )
        ])

## LAne 3 

@app.callback(
    Output('name3', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_lane3(value):
    carNum = races.loc[value,'Lane 3']
    name = racers.loc[carNum,'Name']
    return html.Div([
        html.H5(carNum ),
        html.H4(name),
        ], style={'background-color': 'grey','border': 'solid', 'text-align': 'center'})



@app.callback(
    Output('time3', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_time3(value):
    #time = resultsdf[(resultsdf['race']==value) & (resultsdf['lane']==3)]['time']
    return html.Div([
        daq.LEDDisplay(
            id='lane3-leddisplay',
            value=0,
            label='Time',
            labelPosition='bottom',
            size='40',
            color="#FF5E5E",
            backgroundColor="#000000"
            )
        ])


## lane 4
@app.callback(
    Output('name4', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_lane4(value):
    carNum = races.loc[value,'Lane 4']
    name = racers.loc[carNum,'Name']
    return html.Div([
        html.H5(carNum ),
        html.H6(name),
        ], style={'background-color': 'grey','border': 'solid', 'text-align': 'center'})



@app.callback(
    Output('time4', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_time4(value):
    #time = resultsdf[(resultsdf['race']==value) & (resultsdf['lane']==4)]['time']
    return html.Div([
        daq.LEDDisplay(
            id='lane4-leddisplay',
            value=0,
            label='Time',
            labelPosition='bottom',
            size='40',
            color="#FF5E5E",
            backgroundColor="#000000"
            )
        ])

## Race Controls
# #  html.Button('Get  Results', id='button-results'),
#            html.Button('Force Race End', id='button-end'),
#            html.Button('Next Race', id='button-next'),


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


## Refresh leader board 
@app.callback(
    Output('leader-board', 'children'),
    [Input('interval-component','n_intervals'),
    Input('Refresh','n_clicks')])
def update_leaders(intervals,clicks):
    results_df = pd.read_csv('./resultsFile4016.csv')
    #rf = df[['name','time']]
    rf = results_df.groupby(['car', 'name'], as_index=False).agg({"time": "mean"}).sort_values('time', ascending=True)
    rf['time'] = rf['time'].map('{:,.3f}'.format)
    return dash_table.DataTable(
        id='leader-board',
        columns=[{"name": i, "id": i} for i in rf.columns],
        #columns=[['name','car','time']],
        data=rf.to_dict('records')
        #data=leader_df.to_dict('records')
        )    

## Get Results
@app.callback(
    [Output(component_id='results-button-output', component_property='children'),
    Output('lane1-leddisplay', 'value'),
    Output('lane2-leddisplay', 'value'),
    Output('lane3-leddisplay', 'value'),
    Output('lane4-leddisplay', 'value')],
    [Input(component_id='button-results', component_property='n_clicks'),
    #Input('my-daq-numericinput', 'value')
    ])
def update_times(clicks):
    laneresults = ['1=1.1704a', '2=5.4159b', '3=3.5462c', '4=3.7246d']
    # get race results
    command = 'rg'+'\r\n'
    newcommand = command.encode('ascii')
    #ser.write(newcommand)
    #results = ser.readline()
    #laneresults = results.decode().split()

    return  clicks,laneresults[0][2:8],laneresults[1][2:8],laneresults[2][2:8],laneresults[3][2:8]


#daq.StopButton(id='button-save', buttonText='Save Results'),
@app.callback(
    Output('save-button-output', 'children'),
    [Input(component_id='button-save', component_property='n_clicks'),
    #Input('my-daq-numericinput', 'value')
    ],
    [State('my-daq-numericinput', 'value'),
    State('lane1-leddisplay', 'value'),
    State('lane2-leddisplay', 'value'),
    State('lane3-leddisplay', 'value'),
    State('lane4-leddisplay', 'value')
    ])
def update_save(clicks,current_race,time1,time2,time3,time4):
    resultsdf = pd.DataFrame(columns=['race', 'lane', 'car', 'name', 'time', 'place', 'den', 'category'])
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
        #resultsdf = pd.DataFrame(details)

    # write results 
    resultsdf.to_csv('resultsFile4016.csv',mode='a', header=False)
    return  'Race '+ str(current_race) +' Saved...'
    


# callback for race change
@app.callback(
    Output('connect-results', 'children'),
    [Input('connect-button', 'n_clicks')])
def update_output(value):
    # connect to Track
    #ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = None)
    #ser.name = value
    return value


# callback for race change
@app.callback(
    Output('lane-character', 'value'),
    [Input('lane-number', 'value')])
def update_output(value):
    return 'ol1'

## Get Race Results
#laneresults = ['1=1.1704a', '2=5.4159b', '3=3.5462c', '4=3.7246d']
#@app.callback(
#    Output('lane-character', 'value'),
#    [Input('lane-number', 'value')])
#def update_output(value):
#    laneresults = ['1=1.1704a', '2=5.4159b', '3=3.5462c', '4=3.7246d']
#    return 'ol1'



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)