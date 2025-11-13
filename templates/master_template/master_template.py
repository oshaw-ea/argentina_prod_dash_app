from dash import dcc
from dash import html, page_container

from ea_dash import EALayout


def make_master_template():
    layout = [dcc.Location(id="url")]
    layout.append(html.Div(id="segment-tracking", style={'display': 'none'}))
    layout.append(dcc.Store(id="user-info-store"))
    layout.append((
        EALayout(
            page_container,
            logoLink="/app/",
            id="layoutEA",
            defaultLeftDrawerOpen=True,
            defaultFooterShow=True
        )
    ))

    return html.Div(layout, className="dbc")
