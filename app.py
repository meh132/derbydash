# -*- coding: utf-8 -*-

import base64
import datetime
import io

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go

import pandas as pd
#from track import *
from Tab1 import *
from Tab2 import *
from Tab3 import *

# Input and upload libary
from dash.dependencies import Input, Output, State

# for testing load results
resultsdf = pd.read_csv('./resultsFile.csv')

# Read from CSV to load Races
races = pd.read_csv('Races.csv')
races = races.set_index('Race Number')


# Read list of racers and cars from CSV

racers = pd.read_csv('Racers.csv')
racers = racers.set_index('Number')

## Colors for winners
colors = ["#F0FFF0","#FF5E5E","#c0c0c0","#cd7f32","#F0FFF0"]


#leader_df = resultsdf
#leader_df = resultsdf.groupby(['den','car','name']).agg({'car':'size', 'time':'mean'}).rename(columns={'car':'Races Completed'}).sort_values('time', ascending=True)
#leader_df  = resultsdf.groupby('car').apply(lambda x: x.drop([x['time'].idxmax()])).rename_axis(['time','time']).groupby('car').agg({'car':'size', 'time':'mean'}).rename(columns={'car':'Races Completed','time':'Average Time'}).sort_values('Average Time', ascending=True)
#leader_df = resultsdf.groupby(['den','car','name']).agg({'car':'size', 'time':'mean'}).rename(columns={'car':'Races Completed'}).sort_values(['den','time'], ascending=False)
leader_df = resultsdf.groupby(['car', 'name'], as_index=False).agg({"time": "mean"}).sort_values('time', ascending=True)
#leader_df2 = leader_df.map('{:,.2f}'.format)
leader_df['time'] = leader_df['time'].map('{:,.3f}'.format)
leader1_df = resultsdf.groupby('car') \
    .apply(lambda x: x.drop([x['time'].idxmax()]))\
    .rename_axis(['time','time'])\
    .groupby('car' )\
    .agg({'car':'size', 'time':'mean'}) \
    .rename(columns={'car':'Races Completed','time':'Average Time'}) \
    .sort_values('Average Time', ascending=True)



# Pasrs CSV upload - upload races and racers
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'Racers' in filename:
            # Assume that the user uploaded a CSV file
            racers = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            df = racers
        elif 'Races' in filename:
            # Assume that the user uploaded an excel file
            races = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            df = races
        elif 'csv' in filename:
            # Assume that the user uploaded an excel file
            results = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))            
            df = results  
            results.to_csv('resultsFile.csv')  
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            editable=True,
            filter_action="native",
            sort_action="native",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 20,
        ),
        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app.config.suppress_callback_exceptions = True

# for dyanmic
app.config['suppress_callback_exceptions'] = True


# Set up Tabs

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-2', children=[
        dcc.Tab(label='Setup', value='tab-1'),
        dcc.Tab(label='Race', value='tab-2'),
        dcc.Tab(label='Results', value='tab-3'),
    ]),
    html.Div(id='tabs-content')
])

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
            gen_tab2(leader_df)
        ])
        
    elif tab == 'tab-3':
        return html.Div(children=[
            gen_tab3(resultsdf)
            
        ])

# Callback after upload
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# Connect Call back should read and set statuses of radio buttons


# callback for race change
# update cars for a lane, lanes will pick up their value
### how do we update more values than children, can we call out specific values
## can we update style to show winner??
@app.callback(
    Output('lane1-name', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_output(value):
    carNum = races.loc[value,'Lane 1']
    return carNum

@app.callback(
    Output('lane2-name', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_output(value):
    carNum = races.loc[value,'Lane 2']
    return carNum

@app.callback(
    Output('lane3', 'children'),
    [Input('my-daq-numericinput', 'value')])
def update_output(value):
    carNum = races.loc[value,'Lane 3']
    name = racers.loc[carNum,'Name']

    ### Results if available
    time = resultsdf[(resultsdf['race']==value) & (resultsdf['lane']==3)]['time']
    place = int(resultsdf[(resultsdf['race']==value) & (resultsdf['lane']==3)]['place'])
    color = colors[1]
    return html.Div([
                html.H4('Lane 3'),
                html.H5(carNum ),
                html.H5(place),
                #html.H5(color),
                html.H4(name),
                daq.LEDDisplay(
                    id='lane3-leddisplay',
                    value=time,
                    label='Time',
                    labelPosition='bottom',
                    size='20',
                    color="#FF5E5E",
                    backgroundColor="#000000"
                    ), 
            ], 
            style={'border-radius': '25px', 'background-color': color,'border': 'solid', 'text-align': 'center'})



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