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

#current-race = 1


# Genarte table
def gen_tab2(results_df):
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

            html.Div(id='lane1', className="three columns"),
            html.Div(id='lane2', className="three columns"),
            html.Div(id='lane3', className="three columns"),
            html.Div(id='lane4', className="two columns"),
            ], 
            className="twelve columns",
            style={'border': 'solid', 'text-align': 'center'}),
        html.Div(id='race-controls', children=[
            html.Button('Get Results', id='button-results'),
            html.Button('Force Race End', id='button-end'),
            html.Button('Next Race', id='button-next'),
            ], 
            style={'margin': '80px' , 'text-align': 'center'},
            className="ten columns"), 
            ], className="nine columns"),
        html.Div(id='leader-board', children=[
            html.H3('Fastest Average Time'),
            #html.Table([html.Tr(['Name ','Den ', 'Time '])]),
            generate_table(results_df),
            ],
            className="two columns",        
            style={'border': 'solid'}),
            ],
        )
