import pandas as pd

from ea_dash_elements.utilities.loader_setting import LoadersSettings  #
from ea_dash_elements.utilities.visual_settings import VisualSettings
import plotly.graph_objects as go
from dash import html, dcc
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc


def make_table_card(prefix: str,
                    id_name: str,
                    title: str,
                    source: str = None,
                    editable: bool = False
                    ):
    if not source:
        source = 'Energy Aspects'
    fig = go.Figure()
    fig.layout = VisualSettings().make_base_layout_dict()

    """This should be contained in a dbc layout framework"""
    content = dbc.Stack(
        [
            html.Div(title, style=tile_title_style(), id=f'{prefix}{id_name}-table-title'),
            dcc.Loading(
                id=f'{prefix}{id_name}-table-area',  # use this to replace the table
                type=LoadersSettings.ELEMENT_LOADER,
                color=LoadersSettings.COLOR,
                children=[
                    make_standard_table(
                        prefix=prefix,
                        id_name=id_name,
                        editable=editable
                    )
                ],
            ),
            html.Div(source, style=tile_source_style())
        ],
        style=card_style()
    )
    return content


def make_standard_table(prefix: str, id_name: str, editable: bool = False):
    df = pd.DataFrame()  # use make_random_df() to generate a random dataframe and style things

    table = DataTable(
        id=f'{prefix}{id_name}-table',
        data=df.to_dict('records'),
        columns=[{'name': str(c), 'id': str(c)} for c in df.columns],
        style_as_list_view=True,
        style_table={'overflow': 'auto', 'max-height': '75vh', 'minWidth': '100%'},
        style_cell={
            'padding': '10px',
            'textAlign': 'right',
            'minWidth': '75px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        style_header={
            'backgroundColor': f'{VisualSettings.TABLE_HEADER_COLOR}',
            'color': 'white',
        },
        fixed_columns={'headers': True, 'data': 1},
        fixed_rows={'headers': True},
        editable=editable

    )
    return table


def make_random_df():
    import pandas as pd
    import numpy as np

    # Define the list of country names
    countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Australia']

    # Define the list of years
    years = [2010, 2011, 2012, 2013, 2014, 2015]

    # Generate a matrix of random integers
    # For example, let's create random integers between 0 and 100
    random_data = np.random.randint(0, 100, size=(len(countries), len(years)))

    # Create the DataFrame
    df = pd.DataFrame(data=random_data, index=countries, columns=years)
    df.index.name = ''
    # Display the DataFrame
    return df.reset_index()


def make_last_row_highligh_conditional_formatting(df: pd.DataFrame):
    """This is to be used in the style_data_conditional to make the last row grey for total if needed"""
    style_data_conditional = [
        {
            'if': {
                'row_index': len(df) - 1,
            },
            'backgroundColor': '#E4E4E4',
            'borderTop': '1px #9A9A9A solid',
            'borderBottom': '1px #9A9A9A solid',
            'color': 'black'
        } for i in df.columns
    ]
    return style_data_conditional
