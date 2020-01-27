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
allresults = results.sort_values(by=['time'], ascending=True)

#results = allresults[['name','car','time']].
topresults = allresults.loc[1:5,['name','car','time']]

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
    html.H1(children='Hello Dash', style={'width': '100%', 'textAlign': 'center'
            }),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    html.Div(children=[
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                    y=allresults[allresults.lane==1]['name'],
                    x=allresults[allresults.lane==1]['time'].apply(speed),
                    text=allresults[allresults.lane==1]['name'],
                    name='Lane 1',
                    orientation='h',
                    marker=go.bar.Marker(
                    color='red'
                )
                ),
            go.Bar(
                
                y=allresults[allresults.lane==2]['name'],
                x=allresults[allresults.lane==2]['time'].apply(speed),
                name='Lane 2',
                orientation='h',
                marker=go.bar.Marker(
                    color='blue'
                )
            ),
            go.Bar(
                
                y=allresults[allresults.lane==3]['name'],
                x=allresults[allresults.lane==3]['time'].apply(speed),
                name='Lane 3',
                orientation='h',
                marker=go.bar.Marker(
                    color='green'
                )
            ),
            go.Bar(
                
                y=allresults[allresults.lane==4]['name'],
                x=allresults[allresults.lane==4]['time'].apply(speed),
                name='Lane 4',
                orientation='h',
                marker=go.bar.Marker(
                    color='yellow'
                )
            )
            ],
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
            style={'width': '20%', 'display': 'inline-block'},
            id='my-graph'
        ),
        html.Div(children=[
        html.Div(daq.LEDDisplay(
        id='my-daq-leddisplay1',
        value='3.102',
        label="Lane 1",
        color="#FF5E5E",
        backgroundColor="#A9A9A9"
        ),style={'width': '20%','display': 'inline-block'}),
        html.Div(daq.LEDDisplay(
        id='my-daq-leddisplay2',
        value='3.102',
        label="Lane 2",
        color="#FF5E5E",
        backgroundColor="#A9A9A9"
        ),style={'width': '20%','display': 'inline-block'}),
        html.Div(daq.LEDDisplay(
        id='my-daq-leddisplay3',
        value='3.102',
        label="Lane 3",
        color="#FF5E5E",
        backgroundColor="#A9A9A9"
        ),style={'width': '20%','display': 'inline-block'}),
        html.Div(daq.LEDDisplay(
        id='my-daq-leddisplay4',
        value='3.502',
        label="Lane 4",
        color="#FF5E5E",
        backgroundColor="#A9A9A9"
        ),style={'width': '20%','display': 'inline-block'})], style={'width': '100%','display': 'inline-block'}
        )
        ], 
        style={'width': '100%', 'display': 'inline-block', 'align': 'top'}),
    dash_table.DataTable(id='table',
        columns=[{"name": i, "id": i} for i in topresults.columns],
        data=allresults.to_dict("rows"),
    ),
])



if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True,port=8050)




fig = go.Figure(data=go.Scatter(x=test_df['race'],
                                            y=test_df['time'],
                                            mode='markers',
                                            marker_color=test_df['lane']
                                            text=test_df['name']))
            fig.show()                                
        ])


                    
            