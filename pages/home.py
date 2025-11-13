from dash import register_page, html
import dash_bootstrap_components as dbc
from pages.utilities.pages_utilities import PagesOrder, PagesNames

register_page(
    __name__,
    path='/',
    title=PagesNames.HOME,
    name=PagesNames.HOME,
    order=PagesOrder.HOME
)

# the page needs to contain either a function called layout returning the layout or a layout object
layout = dbc.Container(html.Div(children=[
    html.H1(children='This is our Home page'),
    html.Div(children='''
        This is our Home page content.
    '''),

])
)
