import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table


# Genarte table1
def generate_table(dataframe, max_rows=15):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


