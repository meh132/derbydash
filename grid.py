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
#from Tab1 import *
#from Tab2 import *
#from Tab3 import *


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','./derby.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# for dyanmic
#app.config['suppress_callback_exceptions'] = True


# Set up Tabs

app.layout = html.Div(className="grid-container", children = [
    html.Div(id='Header', className='Header', children = [html.H2('Header')] ),
    html.Div(id='Race-Number', className='Race-Number', children = [html.H2('Race Number')] ),
    html.Div(id='Lane-1', className='Lane-1', children = [html.H2('Lane 1')] ),
    html.Div(id='Lane-2', className='Lane-2', children = [html.H2('Lane 2')] ),
    html.Div(id='Lane-3', className='Lane-3', children = [html.H2('Lane 3')] ),
    html.Div(id='Lane-4', className='Lane-4', children = [html.H2('Lane 4')] ),
    html.H2('Leaders', className="Leaders"),
    html.H2('Race Controls', className="Race-Controls"),
    ])


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)