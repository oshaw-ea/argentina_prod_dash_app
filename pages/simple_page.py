from dash import html, register_page, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from pages.utilities.pages_utilities import PagesOrder, PagesNames
from ea_dash_elements.components.chart_card import make_chart_card
from ea_dash_elements.utilities.visual_settings import VisualSettings

# This is needed to add the page to navigation
# You can remove order if you don't care about page ordering in navbar
register_page(
    __name__,
    path='/simple_page',
    title=PagesNames.SIMPLE_PAGE,
    name=PagesNames.SIMPLE_PAGE,
    order=PagesOrder.SIMPLE_PAGE
)


def get_prefix():
    return 'simple-'


prefix = get_prefix()

# the page needs to contain either a function called layout returning the layout or a layout object
layout = dbc.Container(children=[
    dbc.Row(dbc.Col([
        make_chart_card(
            source='Energy Aspects',
            title='Simple page chart',
            id_name='example-1',
            prefix=get_prefix()
        )
    ], width=10), justify="center"),
], id=f'{prefix}master'

)


@callback(
    Output(f'{prefix}example-1-graph', 'figure'),
    Input(f'{prefix}master', 'children'),
)
def make_chart(trigger):
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })
    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    # this sets all the background elements of the chart in line with EA like white background without lines
    fig.update_layout(VisualSettings().make_base_layout_dict())
    return fig
