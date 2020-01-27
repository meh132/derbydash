# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import dash_daq as daq
import plotly.graph_objs as go





results = pd.read_csv('./resultsFile.csv')
results['carstring'] = results['car'].astype('str')
#df.sort_values(by=['col1', 'col2'])
allresults = results.sort_values(by=['time'], ascending=False)

#results = allresults.loc[['name','car','time']]

#avg = allresults.groupby(['car','name','lane']).agg({'car':'size', 'time':'mean'}).rename(columns={'car':'Races Completed'})        .reset_index()

#avgtimes = avg.to_dict(orient='records')

# Read from CSV to load Races
races = pd.read_csv('Races.csv')
races = races.set_index('Race Number')
n_clicks = 1

# Read list of racers and cars from CSV

racers = pd.read_csv('Racers.csv')
racers = racers.set_index('Number')

current_contestants = races.loc[n_clicks]
speed = lambda x:  x

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    dcc.Graph(
    figure=go.Figure(
        data=[
            go.Bar(
                
                y=allresults['name'],
                x=allresults['time'].apply(speed),
                text=allresults['name'],
                name='Lane 1',
                orientation='h',
                marker=go.bar.Marker(
                    color='red'
                ),

            )
        ],
        transforms=go.transforms(
            type='aggregate',
            groups = allresults['lane'],
            aggregations = go.aggregations(
                [target ='x', func = 'avg',
                [target ='y', func = 'sum']                
            )
            ),
        layout=go.Layout(
            title='Race Results',

            showlegend=True,
            barmode='stack',
            legend=go.layout.Legend(
                x=1.0,
                y=0.0
            ),
            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
        )
    ),
    style={'height': 800, 'width':800},
    id='my-graph'
    ),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'y': [1, 2, 3], 'x': [4, 1, 2], 'type': 'bar', 'name': 'SF','orientation':'h'},
                {'y': [2, 1, 3], 'x': [4, 2, 5], 'type': 'bar', 'name': u'Montréal','orientation':'h'},
                
            ],
            'layout': {
                'title': 'Dash Data Visualization', 'barmode':'stack'
            }
        }
    ),
    dash_table.DataTable(id='table',
        columns=[{"name": i, "id": i} for i in allresults.columns],
        data=allresults.to_dict("rows"),
    ),
    html.Div(children=[
        html.Div([
            daq.Indicator(
                id='my-daq-indicator',
                value=True,
                label="Lane 1",
                color="#00cc96"),
            daq.LEDDisplay(
            id='my-daq-leddisplay1',
            value='3.102',
            color="#FF5E5E",
            backgroundColor="#000000"
            )],
            style={'width': '24%', 'display': 'inline-block', 'textAlign': 'center'
            }),
        html.Div(daq.LEDDisplay(
        id='my-daq-leddisplay2',
        value='3.102',
        label="Lane 2",
        color="#FF5E5E",
        backgroundColor="#A9A9A9"
        ), style={'width': '24%', 'display': 'inline-block'}),
        html.Div(daq.LEDDisplay(
        id='my-daq-leddisplay3',
        value='3.102',
        label="Lane 3",
        color="#FF5E5E",
        backgroundColor="#A9A9A9"
        ), style={'width': '24%', 'display': 'inline-block'}),
        html.Div(daq.LEDDisplay(
        id='my-daq-leddisplay4',
        value='3.502',
        label="Lane 4",
        color="#FF5E5E",
        backgroundColor="#A9A9A9"
        ), style={'width': '10%', 'display': 'inline-block'})]),
    dcc.Slider(
        min=-5,
        max=10,
        step=0.5,
        value=-3,
    ),
    html.Div(dcc.Input(id='input-box', type='text')),
    html.Button('Submit', id='button'),
    html.Div(id='output-container-button', children='Enter a value and press submit')


])

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True,port=8050)
