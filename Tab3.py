import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

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



# Genarte table
def gen_tab3(results_df):
    return html.Div([
           html.H1(children='Race Results'),
            html.H4(children='Pack Pinewood Derby'),
            html.Div(children=[
                generate_table(results_df),
                 
                html.Div(children='''
                    Dash: A web application framework for Python.
                    '''),
                ]),

            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {
                            'x': results_df['race'],
                            'y': results_df['time'],
                            'text': results_df['name'],
                            'mode': 'markers',
                            'marker': {'color': results_df['lane']}
                        }
                    ],

                }
            )
        ])

        
