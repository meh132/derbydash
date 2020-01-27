import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# Genarte table
def gen_tab2():
    return html.Div([
        html.Div(daq.LEDDisplay(
        id='my-daq-leddisplay2',
        value='3.102',
        label="Lane 2",
        color="#FF5E5E",
        backgroundColor="#A9A9A9"
        ), style={'width': '24%', 'display': 'inline-block'}),
        html.H3(['Race '],style={'width': '80%', 'display': 'inline-block'}),
        html.H3(['Leader Board'],style={'width': '20%', 'display': 'inline-block'}),
            # Set up current race Drop down?
            # Show Current Race


            # Get race Results
        ], style={'width': '100%', 'display': 'inline-block'})
