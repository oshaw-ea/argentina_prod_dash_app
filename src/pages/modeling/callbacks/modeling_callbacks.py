from argentina_prod.configs.scenarios import ScenarioTypes
from argentina_prod.pipeline.global_pipeline import GlobalPipeline

from dash import callback, Input, Output
from dash.exceptions import PreventUpdate
from helper_functions_ea import EnergyProduct
from typing import List, Any
from datetime import datetime
from pages.modeling.callbacks.utilities.load_initial_tiles import *

from pages.utilities import pack_data


def define_modeling_callbacks(prefix: str) -> None:
    @callback(
        Output(f'{prefix}drilled-wells-table', 'columns', allow_duplicate=True),
        Output(f'{prefix}drilled-wells-table', 'data', allow_duplicate=True),
        Output(f'{prefix}drilled-wells-history', 'data', allow_duplicate=True),
        Output(f'{prefix}drilled-wells-graph', 'figure', allow_duplicate=True),

        Output(f'{prefix}completions-table', 'columns', allow_duplicate=True),
        Output(f'{prefix}completions-table', 'data', allow_duplicate=True),
        Output(f'{prefix}completions-forecast', 'data', allow_duplicate=True),
        Output(f'{prefix}completions-history', 'data', allow_duplicate=True),
        Output(f'{prefix}completions-graph', 'figure', allow_duplicate=True),

        Output(f'{prefix}download-data-btn', 'disabled', allow_duplicate=True),
        Output(f'{prefix}save-to-db-btn', 'disabled', allow_duplicate=True),
        Output(f'{prefix}drilled-wells-run-chain-btn', 'disabled', allow_duplicate=True),
        Output(f'{prefix}completions-run-chain-btn', 'disabled', allow_duplicate=True),

        Input(f'{prefix}energy-selection-ddown', 'value'),
        Input(f'{prefix}scenario-type-ddown', 'value'),
        Input(f'{prefix}start-date-ddown', 'value'),
        Input(f'{prefix}end-date-ddown', 'value'),
        prevent_initial_call=True
    )
    def load_initial_data(energy_product: EnergyProduct,
                          scenario_type: ScenarioTypes,
                          start_date: str,
                          end_date: str
                          ) -> List[Any]:
        if None in [energy_product, scenario_type, start_date, end_date]:
            raise PreventUpdate

        if scenario_type == ScenarioTypes.SCENARIO:
            raise NotImplementedError

        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)

        pipeline = GlobalPipeline(
            scenario_type=scenario_type,
            start_date=start_date,
            end_date=end_date,
            energy_product_filter=[energy_product]
        )

        (drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data,
         drilled_wells_store, drilled_wells_fig,
         completions_history, completions_forecast, completions_columns, completions_data, completions_store,
         completions_fig) = load_data(pipeline)

        packed_completions_forecast = pack_data(completions_forecast)

        download_button_disabled = False
        save_button_disabled = False

        drilled_wells_run_chain_disabled = False
        completions_run_chain_disabled = False

        res = [
            drilled_wells_columns, drilled_wells_data, drilled_wells_store, drilled_wells_fig,
            completions_columns, completions_data, packed_completions_forecast, completions_store,
            completions_fig,
            download_button_disabled, save_button_disabled,
            drilled_wells_run_chain_disabled, completions_run_chain_disabled
        ]
        return res