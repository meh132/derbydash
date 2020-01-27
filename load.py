
import base64
import datetime
import io
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go
import pandas as pd


### todo
# if racers and races don't exist -- 


## Load Exisitng ?


# for testing load results
resultsdf = pd.read_csv('./resultsFile.csv')

# Read from CSV to load Races
races = pd.read_csv('Races.csv')
races = races.set_index('Race Number')


# Read list of racers and cars from CSV

racers = pd.read_csv('Racers.csv')
racers = racers.set_index('Number')


#Load New
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

