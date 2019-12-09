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

            html.Div(id='lane1', children=[
                html.H4('Lane 0'),
                html.Div(id='lane1-name'),
                html.H5('Master'),
                daq.LEDDisplay(
                    id='lane1-leddisplay',
                    value=2.140,
                    label='Time',
                    labelPosition='bottom',
                    size='20',
                    color="#FF5E5E",
                    backgroundColor="#000000"
                    ), 
            ], 
            className="three columns",
            style={'background-color':'#ffd700','border': 'solid', 'border-color':'#ffd700','text-align': 'center'},
            ),

            html.Div(id='lane2', children=[
                html.H4('Lane 2'),
                html.Div(id='lane2-name'),
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
            ], 
            className="three columns",
            style={'background-color':'#cd7f32','border': 'solid', 'text-align': 'center'}),

            html.Div(id='lane3', className="three columns"),

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
            ], 
            className="two columns",
            style={'border': 'solid', 'text-align': 'center'}),
            html.Div(id='race-controls', children=[
                html.Button('Get Results', id='button-results'),
                html.Button('Force Race End', id='button-end'),
                html.Button('Next Race', id='button-next'),
            ], 
            style={'margin': '80px' , 'text-align': 'center'},
            className="ten columns"), 


            ]),


        ], className="nine columns"),
        
        html.Div(id='leader-board', children=[
            html.H3('Fastest Average Time'),
            #html.Table([html.Tr(['Name ','Den ', 'Time '])]),
            generate_table(results_df),


        ],
        className="three columns",        
        style={'border': 'solid'}),

        ], style={'display': 'inline'}
        )
