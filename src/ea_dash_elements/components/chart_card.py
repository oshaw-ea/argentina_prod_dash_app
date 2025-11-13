from ea_dash_elements.utilities.loader_setting import LoadersSettings  #
from ea_dash_elements.utilities.visual_settings import VisualSettings
import plotly.graph_objects as go
from dash import html, dcc

import dash_bootstrap_components as dbc


def make_chart_card(prefix: str,
                    id_name: str,
                    title: str,
                    source: str = None
                    ):
    if not source:
        source = 'Energy Aspects'
    fig = go.Figure()
    fig.layout = VisualSettings().make_base_layout_dict()

    """This should be contained in a dbc layout framework"""
    content = dbc.Stack(
        [
            html.Div(title, style=tile_title_style(), id=f'{prefix}{id_name}-graph-title'),
            dcc.Loading(
                type=LoadersSettings.ELEMENT_LOADER,
                color=LoadersSettings.COLOR,
                children=[
                    dcc.Graph(
                        id=f'{prefix}{id_name}-graph',
                        figure=fig,
                        config={
                            'displayModeBar': False
                        }
                    )
                ]
            ),
            html.Div(source, style=tile_source_style())
        ],
        style=card_style()
    )
    return content


