import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_table
from functions import *


# generate leader board
#def gen_leaderboard():
 #   den_results = resultsdf.groupby(['den','car','name'])
  #  .agg({'car':'size', 'time':'mean'})
   # .rename(columns={'car':'Races Completed'})
    #.sort_values('time', ascending=True)




# Genarte table
def gen_tab2(results_df):
    return html.Div(id='main_cols',children=[
        html.Div(id='race', children=[
            daq.NumericInput(
            id='my-daq-numericinput',
            max=40,
            value=5,
            label='Race Number',
            labelPosition='top',
            min=1), 
            html.Div(id='lanes', children=[
            html.H3('Lanes'),

            html.Div(id='lane1', children=[
                html.H4('Lane 1'),
                html.H5('Joey Chestnut'),
                daq.LEDDisplay(
                    id='lane1-leddisplay',
                    value='3.141',
                    label='Time',
                    labelPosition='bottom',
                    size='20',
                    color="#FF5E5E",
                    backgroundColor="#000000"
                    ), 
            ], style={'border': 'solid','width': '20%', 'display': 'inline-block', 'text-align': 'center'}),

                        html.Div(id='lane2', children=[
                html.H4('Lane 2'),
                html.H5('Joey Chestnut'),
                daq.LEDDisplay(
                    id='lane1-leddisplay',
                    value='3.141',
                    label='Time',
                    labelPosition='bottom',
                    size='20',
                    color="#FF5E5E",
                    backgroundColor="#000000"
                    ), 
            ], style={'border': 'solid','width': '20%', 'display': 'inline-block', 'text-align': 'center'}),

            html.Div(id='lane3', children=[
                html.H4('Lane 3'),
                html.H5('Joey Chestnut'),
                daq.LEDDisplay(
                    id='lane1-leddisplay',
                    value='3.141',
                    label='Time',
                    labelPosition='bottom',
                    size='20',
                    color="#FF5E5E",
                    backgroundColor="#000000"
                    ), 
            ], style={'border': 'solid','width': '20%', 'display': 'inline-block', 'text-align': 'center'}),

            html.Div(id='lane4', children=[
                html.H4('Lane 4'),
                html.H5('Joey Chestnut'),
                daq.LEDDisplay(
                    id='lane1-leddisplay',
                    value='3.141',
                    label='Time',
                    labelPosition='bottom',
                    size='20',
                    color="#FF5E5E",
                    backgroundColor="#000000"
                    ), 
            ], style={'border': 'solid','width': '20%', 'display': 'inline-block', 'text-align': 'center'}),


            ]), 

        ], style={'width': '70%', 'display': 'inline-block'}),
        
        html.Div(id='leader-board', children=[
            html.H3('Fastest Average Time'),
            #html.Table([html.Tr(['Name ','Den ', 'Time '])]),
            generate_table(results_df),


        ],style={'border': 'solid', 'width': '20%', 'display': 'inline-block'}),

        ], style={'width': '100%', 'display': 'inline-block'})
