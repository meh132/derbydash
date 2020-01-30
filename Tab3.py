import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from functions import *
import pandas as pd

# Genarte table
def gen_tab3():
    results_df = pd.read_csv('resultsFile4016.csv')
    #rf = df[['name','time']]
    rf = results_df.groupby(['den','car', 'name'], as_index=False).agg({"time": "mean"}).sort_values(['den','time'], ascending=True)
    rf['time'] = rf['time'].map('{:,.3f}'.format)
    return dash_table.DataTable(
        id='final-board',
        columns=[{"name": i, "id": i} for i in rf.columns],
        #columns=[['name','car','time']],
        data=rf.to_dict('records'),
        style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Date', 'Region']
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        },
        {
        'if': {'column_id': 'time'},
        'backgroundColor': '#3D9970',
        'color': 'white',
    }
    ],
    style_as_list_view=True,
        #data=leader_df.to_dict('records')
        )      
    