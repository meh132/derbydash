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

# Input and upload libary
from dash.dependencies import Input, Output, State


test_df = pd.read_csv('./resultsFile.csv')

# Genarte table
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


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


# for dyanmic
app.config['suppress_callback_exceptions'] = True


# Set up Tabs

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
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
            html.H3('Race Setup'),
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
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-3':
        return html.Div(children=[
            html.H1(children='Race Results'),
            html.H4(children='Pack Pinewood Derby'),
            generate_table(test_df),
                 
            html.Div(children='''
                Dash: A web application framework for Python.
                '''),

            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {
                            'x': test_df['race'],
                            'y': test_df['time'],
                            'text': test_df['name'],
                            'mode': 'markers',
                            'marker': {'color': test_df['lane']}
                        }
                    ],

                }
            )
        ]
        )

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





if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)