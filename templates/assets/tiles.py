from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_table
from plotly import graph_objs as go
from argentina_prod.configs.enums import ModelMetadata

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


class RigCountTile(GenericTile):
    def __init__(self, prefix, title: str, index: int):
        super().__init__(prefix=prefix, title=title)



    def make_naive_extension_button(self, name: str):
        return dbc.Button(
            "Naive Extension",
            id=f"{self.prefix}{name}-naive-extension-btn",
            color="primary",
            disabled=True
        )

    def make_tile(self):
        """Assemble the tile with all components."""
        return dbc.Col(
            [
                dbc.Card(
                    [
                        self.make_header(),
                        dbc.CardBody(
                            [
                                self.make_data_store(name='rig-count-history'),
                                self.make_data_store(name='rig-count-table-previous'),

                                dbc.Row(
                                    [
                                        dbc.Col(
                                            self.make_upload_button(name='rig-count'),
                                            width="auto",
                                        ),
                                        dbc.Col(
                                            self.make_run_chain_button(name='rig-count', title='Run Rigs Model'),
                                            width="auto",
                                        ),
                                        dbc.Col(
                                            self.make_naive_extension_button(name='rig-count'),
                                            width="auto",
                                        ),
                                    ],
                                    align='start'
                                ),
                                self.make_upload_error_modal(name="rig-count"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                self.make_side_by_side_tables(name='rig-count-table'),
                                                self.make_graph(name='rig-count-graph'),
                                                self.make_graph(name='permits-graph'),
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
                                self.make_data_store(name='drilled-wells-ratios'),
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
                                                self.make_graph(name='drilled-ratio-graph'),

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
                                self.make_data_store(name='completions-ratios'),
                                self.make_data_store(name='ducs-data'),
                                self.make_data_store(name='completions-table-previous'),
                                self.make_data_store(name='frac-fleets-history'),
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
                                                self.make_graph(name='completions-ratio-graph'),
                                                self.make_graph(name='ducs-graph'),
                                                self.make_graph(name='frac-fleets-graph'),
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
                                self.make_data_store(name='unconventional-existing'),
                                self.make_data_store(name='unconventional-future'),
                                self.make_data_store(name='conventional-continuous'),
                                self.make_data_store(name='eia-production'),
                                self.make_data_store(name='production-table-previous'),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            self.make_upload_button(name='production'),
                                            width="auto",
                                        ),
                                        dbc.Col(
                                            self.make_snap_to_eia_button(),
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

    def make_snap_to_eia_button(self):
        return html.Div([
            dbc.Button(
                "Snap to EIA",
                id=f"{self.prefix}production-snap-to-eia-btn",
                color="secondary",
                disabled=True
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader("Snap to EIA Options"),
                    dbc.ModalBody(
                        [
                            html.P("How would you like to handle the forecast adjustment?"),
                            dbc.RadioItems(
                                id=f"{self.prefix}snap-to-eia-delta-option",
                                options=[
                                    {"label": "Maintain forecast delta from previous adjustment series",
                                     "value": "maintain"},
                                    {"label": "Use flat forecast (last historical value)", "value": "flat"},
                                ],
                                value="maintain",
                                inline=False,
                            ),
                        ]
                    ),
                    dbc.ModalFooter([
                        dbc.Button(
                            "Cancel",
                            id=f"{self.prefix}snap-to-eia-cancel",
                            className="ms-auto",
                            color="secondary",
                            n_clicks=0
                        ),
                        dbc.Button(
                            "Apply",
                            id=f"{self.prefix}snap-to-eia-confirm",
                            className="ms-2",
                            color="primary",
                            n_clicks=0
                        ),
                    ]),
                ],
                id=f"{self.prefix}snap-to-eia-modal",
                is_open=False,
                centered=True,
                backdrop="static",
            ),
        ])
#
# class TypeCurveTile(GenericTile):
#     EMPTY_FIGURE = go.Figure().update_layout(
#         title="No Type Curve Selected",
#         xaxis_title="Months",
#         yaxis_title="Production",
#         template="plotly_white",
#         xaxis=dict(
#             range=[0, 60],
#             rangeslider=dict(visible=True),
#             tickmode="auto",
#             showticklabels=True
#         ),
#         yaxis=dict(
#             tickmode="auto",
#             showticklabels=True,
#             fixedrange=False
#         )
#     )
#
#     def __init__(self, prefix, title: str, index: int):
#         super().__init__(prefix=prefix, title=title)
#
#     def _make_play_dropdown(self, mode):
#         dropdown = dcc.Dropdown(
#             id=f"{self.prefix}{mode}-play-dropdown",
#             placeholder="Select a play",
#             style={'width': '100%', 'marginBottom': '10px'},
#             multi=True,
#         )
#
#         return dcc.Loading(
#             id=f"{self.prefix}{mode}-play-loader",
#             children=[dropdown],
#             color=LoadersSettings.COLOR,
#             type=LoadersSettings.ELEMENT_LOADER
#         )
#
#
#     def _make_vintage_dropdown(self, mode):
#         dropdown = dcc.Dropdown(
#             id=f"{self.prefix}{mode}-vintage-dropdown",
#             placeholder="Select a vintage",
#             style={'width': '100%', 'marginBottom': '10px'},
#             multi=True,
#         )
#
#         return dcc.Loading(
#             id=f"{self.prefix}{mode}-vintage-loader",
#             children=[dropdown],
#             color=LoadersSettings.COLOR,
#             type=LoadersSettings.ELEMENT_LOADER
#         )
#
#     def _make_vintage_to_copy_dropdown(self):
#         dropdown =  dcc.Dropdown(
#             id=f"{self.prefix}create-new-vintage-to-copy-dropdown",
#             placeholder="Select vintage to copy from",
#             style={'width': '100%', 'marginBottom': '10px'},
#             multi=True,
#         )
#         return dcc.Loading(
#             id=f"{self.prefix}create-new-vintage-to-copy-loader",
#             children=[dropdown],
#             color=LoadersSettings.COLOR,
#             type=LoadersSettings.ELEMENT_LOADER
#         )
#
#     def _make_vintage_to_generate_dropdown(self):
#         dropdown = dcc.Dropdown(
#             id=f"{self.prefix}create-new-vintage-to-generate-dropdown",
#             placeholder="Select vintage to generate",
#             style={'width': '100%', 'marginBottom': '10px'},
#             multi=True,
#         )
#         return dcc.Loading(
#             id=f"{self.prefix}create-new-vintage-to-generate-loader",
#             children=[dropdown],
#             color=LoadersSettings.COLOR,
#             type=LoadersSettings.ELEMENT_LOADER
#         )
#
#
#     def _make_create_new_buttons(self):
#         return dbc.Row([
#             dbc.Col([
#                 dbc.Button("Apply", id=f"{self.prefix}create-new-apply-btn", color="primary", className="me-2"),
#                 dbc.Button("Save", id=f"{self.prefix}create-save-btn", color="success", className="me-2"),
#                 dbc.Button("Cancel", id=f"{self.prefix}create-cancel-btn", color="secondary"),
#             ], width=12, className="d-flex justify-content-end")
#         ], className="mt-3")
#
#     def _make_edit_buttons(self):
#         return dbc.Row([
#             dbc.Col([
#                 dbc.Button("Apply", id=f"{self.prefix}edit-apply-btn", color="primary", className="me-2"),
#                 dbc.Button("Save", id=f"{self.prefix}edit-save-btn", color="success", className="me-2"),
#                 dbc.Button("Cancel", id=f"{self.prefix}edit-cancel-btn", color="secondary"),
#             ], width=12, className="d-flex justify-content-end")
#         ], className="mt-3")
#
#     def _make_delete_buttons(self):
#         return dbc.Row([
#             dbc.Col([
#                 dbc.Button("Delete", id=f"{self.prefix}delete-confirm-btn", color="danger", className="me-2"),
#                 dbc.Button("Cancel", id=f"{self.prefix}delete-cancel-btn", color="secondary"),
#             ], width=12, className="d-flex justify-content-end")
#         ], className="mt-3")
#
#     def _make_generate_type_curves_button_row(self, mode):
#         button= dbc.Row([
#             dbc.Col([
#                 dbc.Button(
#                     "Display Type Curves",
#                     id=f"{self.prefix}{mode}-generate-btn",
#                     color="primary",
#                     className="w-100",
#                     disabled = True
#                 )
#             ], width=12)
#         ], className="mt-3 mb-3")
#
#         return dcc.Loading(
#             id=f"{self.prefix}{mode}-generate-btn-loader",
#             children=[button],
#             color=LoadersSettings.COLOR,
#             type=LoadersSettings.ELEMENT_LOADER
#         )
#
#     def _make_type_curve_graph(self, mode):
#         return self.make_graph(name=f"{mode}-type-curve-graph")
#
#     def _make_create_new_tab(self):
#         return dbc.Tab(
#             label="Create New",
#             tab_id="create-new",
#             children=[
#                 dbc.Row([
#                     dbc.Col([
#                         html.Label("Plays:"),
#                         self._make_play_dropdown(mode="create-new"),
#                     ], width=6),
#                     dbc.Col([
#                         html.Label("Vintages to display:"),
#                         self._make_vintage_to_copy_dropdown(),
#                     ], width=6),
#                 ], className="mt-3"),
#                 self._make_generate_type_curves_button_row(mode="create-new"),
#                 dbc.Row([
#                     dbc.Col([
#                         html.H6("Type Curve Parameters:", style={'marginTop': '20px'}),
#                         self._make_parameter_table(mode="create-new"),
#                     ], width=12),
#                 ]),
#                 dbc.Row([
#                     dbc.Col([
#                         html.Label("Vintages to Generate:"),
#                         self._make_vintage_to_generate_dropdown(),
#                     ], width=6),
#                 ], className="mt-3"),
#                 self._make_selected_type_curves_table(mode="create-new"),
#                 self._make_type_curve_graph(mode="create-new"),
#                 self._make_create_new_buttons(),
#             ],
#             id=f"{self.prefix}create-new-tab",
#             disabled=True
#         )
#
#     def _make_edit_tab(self):
#         return dbc.Tab(
#             label="Edit",
#             tab_id="edit",
#             children=[
#                 dbc.Row([
#                     dbc.Col([
#                         html.Label("Plays:"),
#                         self._make_play_dropdown(mode="edit"),
#                     ], width=6),
#                     dbc.Col([
#                         html.Label("Vintages to display:"),
#                         self._make_vintage_dropdown(mode="edit"),
#                     ], width=6),
#                 ], className="mt-3"),
#                 self._make_generate_type_curves_button_row(mode="edit"),
#                 dbc.Row([
#                     dbc.Col([
#                         html.H6("Type Curve Parameters:", style={'marginTop': '20px'}),
#                         self._make_parameter_table(mode="edit"),
#                     ], width=12),
#                 ]),
#                 self._make_selected_type_curves_table(mode="edit"),
#                 self._make_type_curve_graph(mode="edit"),
#                 self._make_edit_buttons(),
#             ],
#             id=f"{self.prefix}edit-tab",
#             disabled=True
#         )
#
#     def _make_delete_tab(self):
#         return dbc.Tab(
#             label="Delete",
#             tab_id="delete",
#             children=[
#                 dbc.Row([
#                     dbc.Col([
#                         html.Label("Plays:"),
#                         self._make_play_dropdown(mode="delete"),
#                     ], width=6),
#                     dbc.Col([
#                         html.Label("Vintages to display:"),
#                         self._make_vintage_dropdown(mode="delete"),
#                     ], width=6),
#                 ], className="mt-3"),
#                 self._make_generate_type_curves_button_row(mode="delete"),
#                 dbc.Row([
#                     dbc.Col([
#                         html.H6("Type Curve Parameters:", style={'marginTop': '20px'}),
#                         self._make_parameter_table(mode="delete"),
#                     ], width=12),
#                 ]),
#                 self._make_selected_type_curves_table(mode="delete"),
#                 self._make_type_curve_graph(mode="delete"),
#                 self._make_delete_buttons(),
#             ],
#             id=f"{self.prefix}delete-tab",
#             disabled=True
#         )
#
#     def _make_type_curve_tabs(self):
#         return dbc.Tabs(
#             [
#                 self._make_create_new_tab(),
#                 self._make_edit_tab(),
#                 self._make_delete_tab()
#             ],
#             id=f"{self.prefix}type-curve-tabs",
#             active_tab="create-new"
#         )
#
#     # @staticmethod
#     # def make_parameter_table_value_column(editable):
#     #     return [
#     #         {"name": "Play", "id": ModelMetadata.EA_PLAY, "editable": False},
#     #         {"name": "Vintage", "id": ModelMetadata.VINTAGE, "editable": False},
#     #         {"name": "Type", "id": TypeCurveMetadata.TYPE_CURVE_TYPE, "editable": False},
#     #         {
#     #             "name": "qi",
#     #             "id": TypeCurveMetadata.QI,
#     #             "type": "numeric",
#     #             "format": {"specifier": ".4f"},
#     #             "editable": editable
#     #         },
#     #         {
#     #             "name": "b",
#     #             "id": TypeCurveMetadata.B,
#     #             "type": "numeric",
#     #             "format": {"specifier": ".4f"},
#     #             "editable": editable
#     #         },
#     #         {
#     #             "name": "di",
#     #             "id": TypeCurveMetadata.DI,
#     #             "type": "numeric",
#     #             "format": {"specifier": ".4f"},
#     #             "editable": editable
#     #         },
#     #         {
#     #             "name": "Lateral Length (ft)",
#     #             "id": TypeCurveMetadata.LATERAL_LENGTH,
#     #             "type": "numeric",
#     #             "format": {"specifier": ".0f"},
#     #             "editable": False
#     #         },
#     #         {
#     #             "name": "Completion Stages",
#     #             "id": TypeCurveMetadata.FIRST_COMPLETION_STAGES,
#     #             "type": "numeric",
#     #             "format": {"specifier": ".0f"},
#     #             "editable": False
#     #         },
#     #         {
#     #             "name": "Proppant Mass (lb)",
#     #             "id": TypeCurveMetadata.FIRST_COMPLETION_PROPPANT_MASS,
#     #             "type": "numeric",
#     #             "format": {"specifier": ".0f"},
#     #             "editable": False
#     #         },
#     #         {
#     #             "name": "Fluid Volume (gal)",
#     #             "id": TypeCurveMetadata.FIRST_COMPLETION_FLUID_VOLUME,
#     #             "type": "numeric",
#     #             "format": {"specifier": ".0f"},
#     #             "editable": False
#     #         },
#     #         {
#     #             "name": "90 Days",
#     #             "id": TypeCurveMetadata.FIRST_90_DAYS_PRODUCTION,
#     #             "type": "numeric",
#     #             "format": {"specifier": ".0f"},
#     #             "editable": False
#     #         },
#     #         {
#     #             "name": "180 Days",
#     #             "id": TypeCurveMetadata.FIRST_180_DAYS_PRODUCTION,
#     #             "type": "numeric",
#     #             "format": {"specifier": ".0f"},
#     #             "editable": False
#     #         },
#     #         {
#     #             "name": "365 Days",
#     #             "id": TypeCurveMetadata.FIRST_365_DAYS_PRODUCTION,
#     #             "type": "numeric",
#     #             "format": {"specifier": ".0f"},
#     #             "editable": False
#     #         },
#     #         {
#     #             "name": "EUR",
#     #             "id": TypeCurveMetadata.EUR,
#     #             "type": "numeric",
#     #             "format": {"specifier": ".0f"},
#     #             "editable": False
#     #         }
#     #     ]
#
#     # def _make_parameter_table(self, mode):
#     #     return dash_table.DataTable(
#     #         id=f"{self.prefix}{mode}-parameter-table",
#     #         columns=self.make_parameter_table_value_column(editable=False),
#     #         data=[],
#     #         selected_rows=[],
#     #         row_selectable="multi",
#     #         style_table={
#     #             'marginBottom': '20px',
#     #             'overflowX': 'auto',
#     #         },
#     #         style_cell={
#     #             'textAlign': 'left',
#     #             'minWidth': '75px',
#     #             'maxWidth': '150px',
#     #             'whiteSpace': 'normal',
#     #             'height': 'auto',
#     #             'overflow': 'visible',
#     #             'textOverflow': 'clip',
#     #             'wordBreak': 'normal'
#     #         },
#     #         style_header={
#     #             'fontWeight': 'bold',
#     #         },
#     #         page_size=10
#     #     )
#
#     def _make_selected_type_curves_table(self, mode):
#         is_editable = mode != "delete"
#         title_for_mode = {
#             "create-new": "Type Curves to Create:",
#             "edit": "Type Curves to Edit:",
#             "delete": "Type Curves to Delete:"
#         }
#
#         style_data_conditional = [
#
#             {
#                 'if': {'row_index': 'odd'},
#                 'backgroundColor': 'rgb(248, 248, 248)'
#             },
#
#             {
#                 'if': {'column_editable': False},
#                 'backgroundColor': '#f5f5f5',
#                 'color': '#666666'
#             }
#         ]
#
#         return html.Div([
#             html.H6(title_for_mode[mode], style={'marginTop': '20px'}),
#             dash_table.DataTable(
#                 id=f"{self.prefix}{mode}-selected-parameter-table",
#                 columns=self.make_parameter_table_value_column(editable=is_editable),
#                 data=[],
#                 style_table={
#                     'marginBottom': '20px',
#                     'overflowX': 'auto',
#                 },
#                 style_cell={
#                     'textAlign': 'left',
#                     'minWidth': '75px',
#                     'maxWidth': '150px',
#                     'whiteSpace': 'normal',
#                     'height': 'auto',
#                     'overflow': 'visible',
#                     'textOverflow': 'clip',
#                     'wordBreak': 'normal'
#                 },
#                 style_header={
#                     'fontWeight': 'bold',
#                     'backgroundColor': 'rgb(230, 230, 230)',
#                 },
#                 style_data_conditional=style_data_conditional,
#                 page_size=10
#             )
#         ], id=f"{self.prefix}{mode}-selected-table-container", style={'display': 'none'})
#
#
#     def make_tile(self):
#         return dbc.Col([
#             dbc.Card([
#                 self.make_header(),
#                 dbc.CardBody([
#                     dcc.Loading(
#                         id=f'{self.prefix}type-curve-save-loader',
#                         children=[],
#                         color=LoadersSettings.COLOR,
#                         type=LoadersSettings.FULLSCREEN_LOADER,
#                         fullscreen=True,
#                         style={"zIndex": 9999},
#                     ),
#                     dcc.Loading(
#                         id=f'{self.prefix}type-curve-edit-loader',
#                         children=[],
#                         color=LoadersSettings.COLOR,
#                         type=LoadersSettings.FULLSCREEN_LOADER,
#                         fullscreen=True,
#                         style={"zIndex": 9999},
#                     ),
#                     dcc.Loading(
#                         id=f'{self.prefix}type-curve-delete-loader',
#                         children=[],
#                         color=LoadersSettings.COLOR,
#                         type=LoadersSettings.FULLSCREEN_LOADER,
#                         fullscreen=True,
#                         style={"zIndex": 9999},
#                     ),
#                     dcc.Loading(
#                         id=f'{self.prefix}type-curve-cancel-loader',
#                         children=[],
#                         color=LoadersSettings.COLOR,
#                         type=LoadersSettings.FULLSCREEN_LOADER,
#                         fullscreen=True,
#                         style={"zIndex": 9999},
#                     ),
#                     self.make_data_store(name='available-type-curves'),
#                     self.make_data_store(name='novi-type-curves'),
#                     self.make_data_store(name='type-curves-overrides'),
#                     self.make_data_store(name='type-curve-store'),
#                     self.make_data_store(name='type-curve-mode'),
#                     self.make_data_store(name='unsaved-applied-changes-bool'),
#
#                     self._make_type_curve_tabs(),
#
#                     dbc.Row([
#                         dbc.Col(
#                             html.Div(id=f"{self.prefix}notification-div"),
#                             width=12
#                         ),
#                     ], style={'marginTop': '10px'}),
#                 ])
#             ], style=card_style())
#         ], width=12)