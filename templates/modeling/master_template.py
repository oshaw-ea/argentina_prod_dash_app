from datetime import datetime
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from ea_dash_elements.utilities.loader_setting import LoadersSettings
from ea_dash_elements.utilities.styles import card_style
from templates.assets.tiles import DrilledWellsTile, CompletionsTile, ProductionTile
from argentina_prod.configs.models_config import TimeManagement
from pages.modeling.utilities import IndexMapping
from helper_functions_ea.metadata.metadata_fields import EnergyProduct
from argentina_prod.configs.scenarios import ScenarioTypes
from helper_functions_ea import Logger

class MasterTemplate:
    def __init__(self, prefix):
        self.prefix = prefix

    def make_template(self):
        selection_ribbon = self._make_selection_ribbon()
        tiles = self._make_tiles()

        content = []
        content.append(selection_ribbon)
        content.extend(tiles)

        return dbc.Container(children=content, id=f"{self.prefix}master-container", fluid=True,
                             style={'max-width': '100%'})

    def _make_tiles(self):
        content = [
            dbc.Row(
                [
                    dbc.Col([
                        DrilledWellsTile(prefix=self.prefix, title='Drilled wells',
                                         index=IndexMapping.DRILLED_WELLS).make_tile(),
                        ProductionTile(prefix=self.prefix, title='Production',
                                       index=IndexMapping.PRODUCTION).make_tile(),
                    ], width=6),

                    dbc.Col([
                        CompletionsTile(prefix=self.prefix, title='Completions',
                                        index=IndexMapping.COMPLETIONS).make_tile()
                    ], width=6)
                ]
            ),

        ]
        return content

    def _make_selection_ribbon(self):
        energy_product = EnergyProduct()
        energy_product_df = energy_product.get_metadata_df()

        energy_options = []
        for e in [energy_product.CRUDE_OIL, energy_product.NATURAL_GAS]:
            energy_options.append(
                {'label': energy_product_df.set_index('energy_product').loc[e, 'display_name'], 'value': e})

        scenario_options = [ScenarioTypes.EA_LIBRARY, ScenarioTypes.SCENARIO]
        scenario_options = [{'label': ScenarioTypes.make_display_name(s), 'value': s} for s in scenario_options]

        last_date = TimeManagement.END_DATE
        all_timestamps = TimeManagement.make_available_timestamps(
            start=TimeManagement.FIRST_DATA,
            end=last_date
        )
        default_start = TimeManagement.make_default_start_date().strftime('%Y-%m-%d')
        default_end = last_date.strftime('%Y-%m-%d')
        time_options = [{'label': t.strftime('%b %Y'), 'value': t.strftime('%Y-%m-%d')} for t in all_timestamps]
        temporary_end_date_single_option_only = [{'label':datetime.strptime(default_end, '%Y-%m-%d').strftime('%b %Y'), 'value': default_end}]

        card = dbc.Card([
            dbc.CardBody([
                dbc.Row([

                    dbc.Col([dcc.Dropdown(id=f'{self.prefix}energy-selection-ddown', options=energy_options, value=None,
                                          placeholder='Select energy product')], width=2),
                    dbc.Col([dcc.Dropdown(id=f'{self.prefix}scenario-type-ddown', options=scenario_options,
                                          value=ScenarioTypes.EA_LIBRARY,
                                          placeholder='Select scenario type')], width=2),
                    dbc.Col(
                        [dcc.Dropdown(id=f'{self.prefix}start-date-ddown', options=time_options, value=default_start,
                                      placeholder='Start date')], width=2),
                    dbc.Col([dcc.Dropdown(id=f'{self.prefix}end-date-ddown', options=temporary_end_date_single_option_only, value=default_end,
                                          placeholder='End date')], width=2),
                    dbc.Col([
                        dbc.ButtonGroup([
                            dbc.Button(
                                "Download",
                                id=f'{self.prefix}download-data-btn',
                                color="primary",
                                className="me-1",
                                disabled=True,
                            ),
                            dbc.Button(
                                "Save",
                                id=f'{self.prefix}save-to-db-btn',
                                color="success",
                                className="ms-1",
                                disabled=True,
                            ),
                        ]),
                        dcc.Download(id=f'{self.prefix}download-data'),
                        dcc.Loading(
                            id=f'{self.prefix}save-loader',
                            children=[],
                            color=LoadersSettings.COLOR,
                            type=LoadersSettings.FULLSCREEN_LOADER,
                            fullscreen=True,
                            style={
                                "zIndex": 9999,
                            },
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("Success"),
                                dbc.ModalBody("Changes have been saved to the database successfully."),
                            ],
                            id=f'{self.prefix}save-modal',
                            is_open=False,
                            centered=True
                        )
                    ], width=2)
                ], justify='start')
            ])
        ],
        style=card_style())

        return dbc.Row(dbc.Col([card], width=12))
