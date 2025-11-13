from copy import deepcopy
from ea_dash_elements.utilities.loader_setting import LoadersSettings  #
from ea_dash_elements.utilities.visual_settings import VisualSettings
import plotly.graph_objects as go
from dash import html, dcc

import dash_bootstrap_components as dbc


def make_double_chart_cart(prefix: str,
                           left_id: str,
                           right_id: str,
                           left_title: str,
                           right_title: str,
                           left_source: str = None,
                           right_source: str = None
                           ):
    for source in [left_source, right_source]:
        if not source:
            source = 'Energy Aspects'
    fig_1 = go.Figure()
    fig_1.layout = VisualSettings().make_base_layout_dict()
    fig_2 = deepcopy(fig_1)
    content = dbc.Stack(
        dbc.Row([
            dbc.Col([
                html.Div(left_title, style=tile_title_style(), id=f'{prefix}{left_id}-graph-title'),
                dcc.Loading(
                    type=LoadersSettings.ELEMENT_LOADER,
                    color=LoadersSettings.COLOR,
                    children=[
                        dcc.Graph(
                            id=f'{prefix}{left_id}-graph',
                            figure=fig_2,
                            config={
                                'displayModeBar': False
                            }
                        )
                    ]
                ),
                html.Div(source, style=tile_source_style())
            ], width=6),

            dbc.Col([
                html.Div(right_title, style=tile_title_style(), id=f'{prefix}{right_id}-graph-title'),
                dcc.Loading(
                    type=LoadersSettings.ELEMENT_LOADER,
                    color=LoadersSettings.COLOR,
                    children=[
                        dcc.Graph(
                            id=f'{prefix}{right_id}-graph',
                            figure=fig_2,
                            config={
                                'displayModeBar': False
                            }
                        )
                    ]
                ),
                html.Div(right_source, style=tile_source_style())
            ], width=6),


        ], justify='center'), style=card_style()
    )
    return content
