from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_table

from ea_dash_elements.utilities.loader_setting import LoadersSettings
from ea_dash_elements.utilities.styles import card_style, tile_title_style
from ea_dash_elements.utilities.visual_settings import VisualSettings


class GenericTile:
    def __init__(self, prefix, title: str):
        """Initialize the GenericTile with a prefix, title, and index."""
        self.prefix = prefix
        self.title = title

    def make_header(self):
        """Create a card header with the title."""
        return dbc.CardHeader(
            html.H4(self.title), className="card-title",
            style=tile_title_style()
        )

    def make_upload_button(self, name: str):
        return dcc.Upload(
            id=f"{self.prefix}{name}-upload",
            children=html.Div("Upload Excel"),
            disabled=True,
            style={
                'width': 'auto',
                'height': 'auto',
                'lineHeight': '1.5',
                'borderWidth': '0',
                'borderRadius': '0.25rem',
                'textAlign': 'center',
                'padding': '0.375rem 0.75rem',
                'backgroundColor': '#217346',
                'color': 'white',
                'cursor': 'pointer',
                'display': 'inline-block',
                'fontWeight': '400',
                'fontSize': '1rem'
            },
            multiple=False
        )

    def make_upload_error_modal(self, name: str):
        return dbc.Modal(
            [
                dbc.ModalHeader(f"Error Uploading Excel File"),
                dbc.ModalBody(id=f"{self.prefix}{name}-upload-error-text"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id=f"{self.prefix}{name}-upload-error-close",
                        className="ml-auto"
                    )
                ),
            ],
            id=f"{self.prefix}{name}-upload-error-modal",
            is_open=False,
            centered=True,
            size='lg'
        )

    def make_graph(self, name: str, height='400px'):
        formatted_title = name.replace("-graph", "").replace("-", " ").title()

        return html.Div([
            html.Div([
                dcc.Graph(
                    id=f"{self.prefix}{name}",
                    style={'height': height}
                ),

                html.Div(
                    dbc.Button(
                        "Enlarge",
                        id=f"{self.prefix}{name}-expand-btn",
                        color="secondary",
                        size="sm",
                        outline=True,
                    ),
                    style={
                        "position": "absolute",
                        "top": "10px",
                        "right": "10px",
                        "z-index": "100"
                    }
                )
            ], style={"position": "relative"}),

            dbc.Modal([
                html.Div([
                    html.H3(
                        formatted_title,
                        className="text-center mb-0",
                        style=tile_title_style()
                    ),
                    dbc.Button(
                        "×",
                        id=f"{self.prefix}{name}-modal-close",
                        color="light",
                        className="rounded-circle position-absolute",
                        style={
                            "top": "15px",
                            "right": "20px",
                            "z-index": "1060",
                            "font-size": "2rem",
                            "width": "50px",
                            "height": "50px",
                            "display": "flex",
                            "align-items": "center",
                            "justify-content": "center"
                        }
                    ),
                ], style={
                    "padding": "15px 20px",
                    "background-color": VisualSettings.BACKGROUND_COLOR,
                    "border-bottom": f"1px solid {VisualSettings.TABLE_HEADER_COLOR}",
                    "position": "relative",
                    "margin-top": "70px"
                }),

                html.Div(
                    dcc.Graph(
                        id=f"{self.prefix}{name}-modal-graph",
                        config={'displayModeBar': True},
                        style={"height": "80vh", "padding-left": "40px"}
                    ),
                    style={
                        "padding": "20px",
                        "background-color": VisualSettings.BACKGROUND_COLOR,
                        "margin-left": "20px"
                    }
                )
            ],
                id=f"{self.prefix}{name}-modal",
                size="xl",
                is_open=False,
                centered=True,
                fullscreen=True,
                contentClassName="p-0")
        ])

    def make_data_store(self, name:str):
        """Create a data store component."""
        return dcc.Store(id=f"{self.prefix}{name}", data=False)

    def make_table(self, name: str):
        """Create a table component."""
        div = html.Div(
            children=[
                dash_table.DataTable(
                    id=f"{self.prefix}{name}",
                    editable=True,
                    style_table={'overflowX': 'auto', 'width': '100%', 'max-width': '100%', 'height': '600px'},
                    fixed_rows={'headers': True},
                    fixed_columns={'headers': True, 'data': 1},
                    style_cell={
                        'height': 'auto',
                        'minWidth': '90px', 'width': '90px', 'maxWidth': '100px',
                        'whiteSpace': 'normal',
                    },
                    style_header = {
                        'height':'55px'
                    },

                )
            ]
        )

        div = dcc.Loading(
            children=div,
            color=LoadersSettings.COLOR,
            type=LoadersSettings.ELEMENT_LOADER
        )

        return div

    def make_run_chain_button(self, name: str, title: str):
        return dbc.Button(
            title,
            id=f"{self.prefix}{name}-run-chain-btn",
            color="primary",
            disabled=True
        )

    def make_total_table(self, name: str, editable: bool = True):
        return dash_table.DataTable(
            id=f"{self.prefix}{name}-total",
            editable=editable,
            style_table={
                'overflowX': 'hidden',
                'width': '120px',
                'maxWidth': '120px',
                'height': '600px',
                'overflow-x': 'hidden'
            },
            fixed_rows={'headers': True},
            style_cell={
                'height': 'auto',
                'minWidth': '60px',
                'width': '100px',
                'maxWidth': '120px',
                'whiteSpace': 'normal',
                'fontWeight': 'bold',
                'textOverflow': 'ellipsis',
                'backgroundColor': '#f0f0f0'
            },
            style_header={
                'height': '55px',
                'minHeight': '55px',
                'maxHeight': '55px',
                'whiteSpace': 'normal',
                'backgroundColor': 'white',
            }
        )

    def make_side_by_side_tables(self, name, total_editable=True):
        main_table = self.make_table(name=name)
        total_table = self.make_total_table(name=name, editable=total_editable)

        layout = html.Div(
            children=[
                html.Div(main_table, style={"flex": "1", "overflow-x": "auto"}),
                html.Div(total_table, style={
                    "flex": "0 0 auto",
                    "overflow-x": "hidden",
                    "width": "120px"
                })
            ],
            style={
                "display": "flex",
                "width": "100%",
                "overflow": "hidden"
            }
        )

        return dcc.Loading(
            children=layout,
            color=LoadersSettings.COLOR,
            type=LoadersSettings.ELEMENT_LOADER
        )

    def make_tile(self):
        raise NotImplementedError


class DrilledWellsTile(GenericTile):
    def __init__(self, prefix, title: str, index: int):
        super().__init__(prefix=prefix, title=title)

    def make_tile(self):
        """Assemble the tile with all components."""
        return dbc.Col(
            [
                dbc.Card(
                    [
                        self.make_header(),
                        dbc.CardBody(
                            [
                                self.make_data_store(name='drilled-wells-history'),
                                self.make_data_store(name='drilled-wells-table-previous'),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            self.make_upload_button(name='drilled-wells'),
                                            width="auto",
                                        ),
                                        dbc.Col(
                                            self.make_run_chain_button(name='drilled-wells', title='Run Drilled Wells Model'),
                                            width="auto",
                                        ),
                                    ],
                                    align='start'
                                ),
                                self.make_upload_error_modal(name="drilled-wells"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                self.make_side_by_side_tables(name='drilled-wells-table'),
                                                self.make_graph(name='drilled-wells-graph'),

                                            ],

                                            width=12,
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ],
                    style=card_style()
                )
            ],
            width=12
        )

class CompletionsTile(GenericTile):
    def __init__(self, prefix, title: str, index: int):
        super().__init__(prefix=prefix, title=title)

    def make_tile(self):
        """Assemble the tile with all components."""
        return dbc.Col(
            [
                dbc.Card(
                    [
                        self.make_header(),
                        dbc.CardBody(
                            [
                                self.make_data_store(name='completions-forecast'),
                                self.make_data_store(name='completions-history'),
                                self.make_data_store(name='completions-table-previous'),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            self.make_upload_button(name='completions'),
                                            width="auto",
                                        ),
                                        dbc.Col(
                                            self.make_run_chain_button(name='completions', title="Run Completions Model"),
                                            width="auto",
                                        ),
                                    ],
                                    align='start'
                                ),
                                self.make_upload_error_modal(name="completions"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                self.make_side_by_side_tables(name='completions-table'),
                                                self.make_graph(name='completions-graph'),
                                            ],

                                            width=12,
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ],
                    style=card_style()
                )
            ],
            width=12
        )

class ProductionTile(GenericTile):
    def __init__(self, prefix, title: str, index: int):
        super().__init__(prefix=prefix, title=title)

    def make_tile(self):
        """Assemble the tile with all components."""
        return dbc.Col(
            [
                dbc.Card(
                    [
                        self.make_header(),
                        dbc.CardBody(
                            [
                                self.make_data_store(name='unconventional-continuous'),
                                self.make_data_store(name='conventional-continuous'),
                                self.make_data_store(name='production-table-previous'),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            self.make_upload_button(name='production'),
                                            width="auto",
                                        ),
                                    ],
                                    align='start'
                                ),
                                self.make_upload_error_modal(name="production"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                self.make_side_by_side_tables(name="production-table", total_editable=False),
                                                self.make_graph(name='production-graph'),
                                            ],

                                            width=12,
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ],
                    style=card_style(),
                )
            ],
            width=12
        )