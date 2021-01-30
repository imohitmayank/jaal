"""
Author: Mohit Mayank

Layout of the application
"""
# import 
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# list of common styles of row alignment
def fetch_row_style(style=""):
    return {'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center'}

def create_row(children, style=""):
    return dbc.Row(children, 
                   style=fetch_row_style(style),
                   className="column flex-display")