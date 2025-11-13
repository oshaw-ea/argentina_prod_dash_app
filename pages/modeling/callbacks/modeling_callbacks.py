# import pandas as pd
# from botocore.eventstream import NoInitialResponseError
# from dash import callback, Input, Output, State, ctx, no_update
# import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate
# from datetime import datetime
# from typing import List, Optional, Any
#
# from dateutil.relativedelta import relativedelta
# from argentina_prod.configs.enums import ModelMetadata, TypeCurveMetadata, Models
# from argentina_prod.configs.model_sids_config import ScenarioTypes, Spaces
# from argentina_prod.configs.models_config import TimeManagement
# from argentina_prod.models.eia_adjustment_series.eia_adjustment_series import EIAAdjustmentSeriesModel
# from argentina_prod.scenarios.scenario import Scenario
# from argentina_prod.configs.missing_data import MissingData
# from helper_functions_ea.metadata.metadata_fields import EnergyProduct
#
# from pages.modeling.callbacks.utilities.run_end_to_end_model_utilities import filter_by_date_range, \
#     filter_by_basins_filter, run_chain_model
# from pages.modeling.callbacks.utilities.type_curve_utilities import populate_existing_table, populate_graph, \
#     update_available_type_curves_from_table_data, update_table_data_from_selected_table_data, \
#     update_type_curve_metrics_from_parameter_table_data, create_new_available_type_curves_from_selected_table_data, \
#     get_vintages_in_forecasting_period
# from pages.utilities import *
# from pages.modeling.callbacks.utilities.visual_builders.rig_count_visualiser import RigCountVisualiser
# from pages.modeling.callbacks.utilities.load_initial_tiles import *
# from argentina_prod.models.type_curves.type_curve import TypeCurveLoader, TypeCurve, TypeCurveCollection
# from templates.assets.tiles import TypeCurveTile
# import io, base64, copy, numpy as np
#
#
# def define_modeling_callbacks(prefix: str) -> None:
#     @callback(
#         Output(f'{prefix}rig-count-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}rig-count-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}rig-count-history', 'data', allow_duplicate=True),
#         Output(f'{prefix}rig-count-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}rig-count-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}rig-count-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}permits-graph', 'figure', allow_duplicate=True),
#
#         Output(f'{prefix}drilled-wells-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-history', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-ratios', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}drilled-ratio-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}drilled-wells-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}drilled-wells-table-total", "data", allow_duplicate=True),
#
#         Output(f'{prefix}completions-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}completions-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-forecast', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-history', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-ratios', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}completions-ratio-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}completions-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}completions-table-total", "data", allow_duplicate=True),
#
#         Output(f'{prefix}ducs-data', 'data', allow_duplicate=True),
#         Output(f'{prefix}ducs-graph', 'figure', allow_duplicate=True),
#
#         Output(f'{prefix}frac-fleets-graph', 'figure', allow_duplicate=True),
#
#         Output(f'{prefix}unconventional-existing', 'data', allow_duplicate=True),
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}conventional-continuous', 'data', allow_duplicate=True),
#         Output(f'{prefix}eia-production', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#
#         Output(f'{prefix}available-type-curves', 'data', allow_duplicate=True),
#         Output(f'{prefix}novi-type-curves', 'data', allow_duplicate=True),
#         Output(f'{prefix}type-curves-overrides', 'data', allow_duplicate=True),
#
#         Output(f'{prefix}create-new-tab', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}edit-tab', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}delete-tab', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}type-curve-tabs', 'active_tab', allow_duplicate=True),
#
#         Output(f'{prefix}download-data-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}save-to-db-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}production-snap-to-eia-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}rig-count-run-chain-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}rig-count-naive-extension-btn', "disabled", allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-run-chain-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}completions-run-chain-btn', 'disabled', allow_duplicate=True),
#
#         Input(f'{prefix}basin-selection-ddown', 'value'),
#         Input(f'{prefix}energy-selection-ddown', 'value'),
#         Input(f'{prefix}scenario-type-ddown', 'value'),
#         Input(f'{prefix}start-date-ddown', 'value'),
#         Input(f'{prefix}end-date-ddown', 'value'),
#         prevent_initial_call=True
#     )
#     def load_initial_data(basin: UsBasins,
#                           energy_product: EnergyProduct,
#                           scenario_type: ScenarioTypes,
#                           start_date: str,
#                           end_date: str
#                           ) -> List[Any]:
#         if None in [basin, energy_product, scenario_type, start_date, end_date]:
#             raise PreventUpdate
#
#         if scenario_type == ScenarioTypes.SCENARIO:
#             raise NotImplementedError
#
#         start_date = datetime.fromisoformat(start_date)
#         end_date = datetime.fromisoformat(end_date)
#
#         basins_filter = get_basins_filter(basin)
#
#         pipeline = GlobalPipeline(
#             basins_filter=basins_filter,
#             scenario_type=scenario_type,
#             start_date=start_date,
#             end_date=end_date,
#             energy_product_filter=[energy_product]
#         )
#
#         (rig_count_history, rig_count_forecast, rig_count_columns, rig_count_data, rig_count_store, rig_count_fig,
#          rig_count_total_columns, rig_count_total_data,
#          permits_fig,
#          drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data,
#          drilled_wells_store, drilled_wells_fig, drilled_well_total_columns, drilled_well_total_data,
#          drilled_wells_ratios, drilled_wells_ratio_fig,
#          completions_history, completions_forecast, completions_columns, completions_data, completions_store,
#          completions_fig, completions_total_columns, completions_total_data,
#          completions_ratios, completions_ratio_fig,
#          ducs_data, ducs_fig,
#          frac_fleets_fig,
#          available_type_curves, type_curves_data, novi_type_curves, type_curve_overrides,
#          unconventional_existing_data, unconventional_future_data, continuous_conventional_data, eia_data, prod_fig,
#          prod_columns, prod_data, prod_total_column, prod_total_data) = load_data(basin, energy_product, pipeline)
#
#         packed_completions_forecast = pack_data(completions_forecast)
#
#         create_tab_disabled = False
#         edit_tab_disabled = False
#         delete_tab_disabled = False
#         active_tab = "create-new"
#
#         download_button_disabled = False
#         save_button_disabled = False
#
#         snap_to_eia_disabled = False
#         naive_extension_disabled = False
#         if basin == UsBasins().REST_OF_L48_METAVALUE:
#             rig_count_run_chain_disabled = True
#         else:
#             rig_count_run_chain_disabled = False
#
#         drilled_wells_run_chain_disabled = False
#         completions_run_chain_disabled = False
#
#
#         res = [
#             rig_count_columns, rig_count_data, rig_count_store, rig_count_fig, rig_count_total_columns, rig_count_total_data, permits_fig,
#             drilled_wells_columns, drilled_wells_data, drilled_wells_store, drilled_wells_ratios, drilled_wells_fig, drilled_wells_ratio_fig,
#             drilled_well_total_columns, drilled_well_total_data,
#             completions_columns, completions_data, packed_completions_forecast, completions_store, completions_ratios,
#             completions_fig, completions_ratio_fig, completions_total_columns, completions_total_data, ducs_data, ducs_fig, frac_fleets_fig,
#             unconventional_existing_data, unconventional_future_data, continuous_conventional_data, eia_data,
#             prod_columns, prod_data, prod_fig, prod_total_column, prod_total_data,
#             type_curves_data, novi_type_curves, type_curve_overrides,
#             create_tab_disabled, edit_tab_disabled, delete_tab_disabled, active_tab,
#             download_button_disabled, save_button_disabled, snap_to_eia_disabled, rig_count_run_chain_disabled, naive_extension_disabled,
#             drilled_wells_run_chain_disabled, completions_run_chain_disabled
#         ]
#         return res
#
#     @callback(
#         Output(f'{prefix}rig-count-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}rig-count-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}completions-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}ducs-data', 'data', allow_duplicate=True),
#         Output(f'{prefix}ducs-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}download-data-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}save-to-db-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}rig-count-table-total', 'data', allow_duplicate=True),
#         Output(f'{prefix}rig-count-table-previous', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-table-total', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-table-previous', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-table-total', 'data', allow_duplicate=True),
#
#         Input(f'{prefix}rig-count-table', 'data'),
#         State(f'{prefix}rig-count-table', 'data_previous'),
#         State(f'{prefix}rig-count-table-previous', 'data'),
#         State(f'{prefix}rig-count-history', 'data'),
#
#         State(f'{prefix}drilled-wells-ratios', 'data'),
#         State(f'{prefix}drilled-wells-history', 'data'),
#
#         State(f'{prefix}completions-forecast', 'data'),
#         State(f'{prefix}completions-history', 'data'),
#         State(f'{prefix}completions-ratios', 'data'),
#         State(f'{prefix}ducs-data', 'data'),
#
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#
#         State(f'{prefix}available-type-curves', 'data'),
#         State(f'{prefix}novi-type-curves', 'data'),
#         State(f'{prefix}type-curves-overrides', 'data'),
#
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#
#         State(f'{prefix}rig-count-graph', 'figure'),
#         State(f'{prefix}drilled-wells-graph', 'figure'),
#         State(f'{prefix}completions-graph', 'figure'),
#         State(f'{prefix}ducs-graph', 'figure'),
#         State(f'{prefix}production-graph', 'figure'),
#         prevent_initial_call=True
#     )
#     def rig_count_table_update(rig_count_table_data: List[Dict],
#                                rig_count_table_previous_data: Optional[List[Dict]],
#                                stored_previous_data: Optional[List[Dict]],
#                                rig_count_history: List[Dict],
#                                drilled_wells_ratios: List[Dict],
#                                drilled_wells_history: List[Dict],
#
#                                completions_forecast: List[Dict],
#
#                                completions_history: List[Dict],
#                                completions_ratios: List[Dict],
#                                ducs_data: List[Dict],
#
#                                basin: UsBasins,
#                                energy_product: EnergyProduct,
#
#                                available_type_curves: List[Dict],
#                                novi_type_curves: List[Dict],
#                                type_curve_overrides: List[Dict],
#
#                                unconventional_existing_data: List[Dict],
#                                unconventional_future_data: List[Dict],
#                                continuous_conventional_data: List[Dict],
#                                eia_data: List[Dict],
#
#                                previous_rig_count_fig,
#                                previous_drilled_wells_fig,
#                                previous_completions_fig,
#                                previous_ducs_fig,
#                                previous_prod_fig,
#                                ) -> tuple:
#         """We are here because a user updated the rig count table.
#         We need to recalculate and run the whole chain.
#         We keep the drilled well ratio and get the drilled wells from new rig count forecast.
#         We then propagate changes to completions using the completions ratio.
#         """
#
#
#         if rig_count_table_data is None:
#             raise PreventUpdate
#
#         if rig_count_table_previous_data is None:
#             if not stored_previous_data:
#                 raise PreventUpdate
#
#         if stored_previous_data:
#             rig_count_table_previous_data = stored_previous_data.copy()
#             stored_previous_data = False
#
#
#         rig_count_forecast = unpack_data(rig_count_table_data)
#         previous_rig_count_forecast = unpack_data(rig_count_table_previous_data)
#
#         if is_initial_load(previous_rig_count_forecast, rig_count_forecast):
#             raise PreventUpdate
#
#         if previous_rig_count_forecast.equals(rig_count_forecast):
#             raise PreventUpdate
#
#         drilled_wells_history = unpack_data(drilled_wells_history)
#         rig_count_history = unpack_data(rig_count_history)
#         drilled_wells_ratios = unpack_data(drilled_wells_ratios)
#         completions_forecast = unpack_data(completions_forecast)
#         completions_history = unpack_data(completions_history)
#         completions_ratios = unpack_data(completions_ratios)
#         existing_ducs = unpack_data(ducs_data)
#
#         available_type_curves = unpack_data(available_type_curves)
#         novi_type_curves = unpack_data(novi_type_curves)
#         override_type_curves = unpack_data(type_curve_overrides)
#
#
#         rig_count_columns, rig_count_data, rig_count_fig = RigCountVisualiser.visualise_data(
#             history_df=rig_count_history,
#             forecast_df=rig_count_forecast,
#             title=ChartTitles.RIG_COUNT,
#             eia_basin=basin
#         )
#
#         new_drilled_wells, drilled_wells_columns, drilled_wells_data, drilled_wells_fig = DrilledWellsVisualiser.update_drilled_wells(
#             rig_count_history=rig_count_history,
#             rig_count_forecast=rig_count_forecast,
#             drilled_wells_history=drilled_wells_history,
#             drilled_wells_ratios=drilled_wells_ratios
#         )
#
#         new_completions, completions_columns, completions_data, completions_fig = CompletionsVisualiser.update_completions(
#             drilled_wells_history=drilled_wells_history,
#             drilled_wells_forecast=new_drilled_wells,
#             completions_history=completions_history,
#             completions_ratios=completions_ratios,
#             existing_completions_forecast=completions_forecast,
#             basin=basin
#         )
#
#         new_ducs, ducs_fig = DUCsVisualiser.update_ducs(existing_ducs, new_completions, new_drilled_wells, basin)
#
#         packed_new_ducs = pack_data(new_ducs)
#         packed_drilled_wells = pack_data(new_drilled_wells)
#         packed_completions = pack_data(new_completions)
#
#         unconventional_existing = unpack_data(unconventional_existing_data)
#         unconventional_future = unpack_data(unconventional_future_data)
#         continuous_conventional = unpack_data(continuous_conventional_data)
#         eia_production = unpack_data(eia_data)
#         pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             basins_filter=get_basins_filter(basin),
#             energy_product_filter=[energy_product]
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=unconventional_existing,
#             unconventional_future_df=unconventional_future,
#             continuous_conventional_df=continuous_conventional,
#             eia_df=eia_production,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         modified_plays = production_visual.get_modified_plays_completions(
#             previous_df=previous_rig_count_forecast,
#             new_df=rig_count_forecast
#         )
#
#
#         tc_loader = TypeCurveLoader(
#             novi_type_curves=novi_type_curves,
#             override_type_curves=override_type_curves,
#             available_type_curves=available_type_curves
#         )
#         vintages = list(eia_production.index.year.unique())
#
#         tc_loader.load_type_curves(energy_products=[energy_product], ea_plays=modified_plays, vintages_filter=vintages)
#         type_curves = tc_loader.get_prioritized_type_curves()
#
#         production_visual.recalculate_future_wells_production(
#             type_curves=type_curves,
#             completions_history=completions_history,
#             completions_forecasts=new_completions,
#             plays_to_recalculate=modified_plays
#         )
#
#         prod_fig, prod_columns, prod_data, prod_total_columns, prod_total_data = production_visual.process_and_visualise_data()
#         packed_unconventional_future = pack_data(production_visual.get_storage_format_future_wells_prod())
#
#         rig_count_fig = preserve_figure_state(rig_count_fig, previous_rig_count_fig)
#         drilled_wells_fig = preserve_figure_state(drilled_wells_fig, previous_drilled_wells_fig)
#         completions_fig = preserve_figure_state(completions_fig, previous_completions_fig)
#         ducs_fig = preserve_figure_state(ducs_fig, previous_ducs_fig)
#         prod_fig = preserve_figure_state(prod_fig, previous_prod_fig)
#
#
#         total_rig_count_columns, total_rig_count_data = RigCountVisualiser.make_total_table(rig_count_forecast)
#         total_drilled_wells_columns, total_drilled_wells_data = DrilledWellsVisualiser.make_total_table(
#             new_drilled_wells)
#         total_completions_columns, total_completions_data = CompletionsVisualiser.make_total_table(new_completions)
#         download_button_disabled = False
#         save_button_disabled = False
#         drilled_wells_stored_previous_data = False
#         return (
#             rig_count_table_data, rig_count_fig,
#             packed_drilled_wells, drilled_wells_fig,
#             packed_completions, completions_fig, packed_new_ducs, ducs_fig,
#             packed_unconventional_future, prod_columns, prod_data, prod_total_columns, prod_total_data, prod_fig,
#             download_button_disabled, save_button_disabled,
#             total_rig_count_data, stored_previous_data,
#             total_drilled_wells_data, drilled_wells_stored_previous_data,
#             total_completions_data,
#         )
#
#     @callback(
#         Output(f"{prefix}rig-count-table", "data", allow_duplicate=True),
#         Output(f"{prefix}rig-count-table-previous", "data", allow_duplicate=True),
#         Input(f"{prefix}rig-count-table-total", "data"),
#         State(f"{prefix}rig-count-table-total", "data_previous"),
#         State(f"{prefix}rig-count-table", "data"),
#         prevent_initial_call=True
#     )
#     def update_play_level_rig_count_table_on_total_change(new_total_data, old_total_data, existing_play_level_data):
#         if new_total_data is None or old_total_data is None:
#             raise PreventUpdate
#
#         new_play_level_data = existing_play_level_data.copy()
#         new_play_level_data = unpack_data(new_play_level_data)
#         new_total_data = unpack_total_data(new_total_data)
#         old_total_data = unpack_total_data(old_total_data)
#
#         new_play_level_data = RigCountVisualiser.update_play_level_data_from_totals(new_total_data=new_total_data, old_total_data=old_total_data, play_level_data=new_play_level_data)
#         play_level_data = pack_data(new_play_level_data)
#
#         return play_level_data, existing_play_level_data
#
#     @callback(
#         Output(f'{prefix}rig-count-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-ratios', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-ratio-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-table-total', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-table-previous', 'data', allow_duplicate=True),
#
#         Output(f'{prefix}completions-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}completions-ratios', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-ratio-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}ducs-data', 'data', allow_duplicate=True),
#         Output(f'{prefix}ducs-graph', 'figure', allow_duplicate=True),
#
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#
#         Output(f'{prefix}completions-table-previous', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-table-total', 'data', allow_duplicate=True),
#
#         Output(f'{prefix}download-data-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}save-to-db-btn', 'disabled', allow_duplicate=True),
#
#         Input(f'{prefix}drilled-wells-table', 'data'),
#         State(f'{prefix}drilled-wells-table', 'data_previous'),
#         State(f'{prefix}drilled-wells-history', 'data'),
#         State(f'{prefix}drilled-wells-table-previous', 'data'),
#
#         State(f'{prefix}rig-count-history', 'data'),
#         State(f'{prefix}rig-count-table', 'data'),
#
#         State(f'{prefix}completions-forecast', 'data'),
#         State(f'{prefix}completions-history', 'data'),
#         State(f'{prefix}completions-ratios', 'data'),
#         State(f'{prefix}ducs-data', 'data'),
#
#         State(f'{prefix}available-type-curves', 'data'),
#         State(f'{prefix}novi-type-curves', 'data'),
#         State(f'{prefix}type-curves-overrides', 'data'),
#
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#
#         State(f'{prefix}drilled-wells-graph', 'figure'),
#         State(f'{prefix}drilled-ratio-graph', 'figure'),
#         State(f'{prefix}completions-graph', 'figure'),
#         State(f'{prefix}completions-ratio-graph', 'figure'),
#         State(f'{prefix}ducs-graph', 'figure'),
#         State(f'{prefix}production-graph', 'figure'),
#         prevent_initial_call=True
#     )
#     def drilled_wells_table_update(drilled_wells_table_data: List[Dict],
#                                    drilled_wells_table_previous_data: Optional[List[Dict]],
#                                    drilled_wells_history: List[Dict],
#                                    drilled_wells_stored_previous_data: List[Dict],
#
#                                    rig_count_history: List[Dict],
#                                    rig_count_forecast: List[Dict],
#
#                                    completions_forecast: List[Dict],
#                                    completions_history: List[Dict],
#                                    completions_ratios: List[Dict],
#                                    ducs_data: List[Dict],
#
#                                    available_type_curves: List[Dict],
#                                    novi_type_curves: List[Dict],
#                                    type_curve_overrides: List[Dict],
#
#                                    unconventional_existing_data: List[Dict],
#                                    unconventional_future_data: List[Dict],
#                                    continuous_conventional_data: List[Dict],
#                                    eia_data: List[Dict],
#
#                                    basin: UsBasins,
#                                    energy_product: EnergyProduct,
#
#                                    previous_drilled_wells_fig,
#                                    previous_drilled_ratio_fig,
#                                    previous_completions_fig,
#                                    previous_completions_ratio_fig,
#                                    previous_ducs_fig,
#                                    previous_prod_fig,
#
#                                    ) -> tuple:
#         """We are here because a user updated the drilled wells table.
#         We need to recalculate and run the whole chain,
#         We update the drilled wells ratio to account for the new drilled wells forecast.
#         """
#         if drilled_wells_table_data is None:
#             raise PreventUpdate
#         if drilled_wells_table_previous_data is None:
#             if not drilled_wells_stored_previous_data:
#                 raise PreventUpdate
#
#         if drilled_wells_stored_previous_data:
#             drilled_wells_table_previous_data = drilled_wells_stored_previous_data.copy()
#             drilled_wells_stored_previous_data = False
#
#         drilled_wells_forecast = unpack_data(drilled_wells_table_data)
#         drilled_wells_history = unpack_data(drilled_wells_history)
#         rig_count_history = unpack_data(rig_count_history)
#         rig_count_forecast = unpack_data(rig_count_forecast)
#         previous_drilled_wells_forecast = unpack_data(drilled_wells_table_previous_data)
#         completions_history = unpack_data(completions_history)
#         completions_forecast = unpack_data(completions_forecast)
#         completions_ratios = unpack_data(completions_ratios)
#         existing_ducs = unpack_data(ducs_data)
#         unconventional_existing = unpack_data(unconventional_existing_data)
#         unconventional_future = unpack_data(unconventional_future_data)
#         continuous_conventional = unpack_data(continuous_conventional_data)
#         eia_production = unpack_data(eia_data)
#
#         available_type_curves = unpack_data(available_type_curves)
#         novi_type_curves = unpack_data(novi_type_curves)
#         override_type_curves = unpack_data(type_curve_overrides)
#
#         if is_initial_load(previous_drilled_wells_forecast, drilled_wells_forecast):
#             raise PreventUpdate
#
#         if previous_drilled_wells_forecast.equals(drilled_wells_forecast):
#             raise PreventUpdate
#
#         drilled_wells_columns, drilled_wells_data, drilled_wells_fig = DrilledWellsVisualiser.visualise_data(
#             history_df=drilled_wells_history,
#             forecast_df=drilled_wells_forecast,
#             title=ChartTitles.DRILLED_WELLS
#         )
#
#         drilled_wells_ratios, drilled_wells_ratio_fig = DrilledWellsRatios.update_ratios(
#             drilled_wells_history=drilled_wells_history,
#             drilled_wells_forecast=drilled_wells_forecast,
#             rig_count_history=rig_count_history,
#             rig_count_forecast=rig_count_forecast
#         )
#
#         new_completions, completions_columns, completions_data, completions_fig = CompletionsVisualiser.update_completions(
#             drilled_wells_history=drilled_wells_history,
#             drilled_wells_forecast=drilled_wells_forecast,
#             completions_history=completions_history,
#             completions_ratios=completions_ratios,
#             existing_completions_forecast=completions_forecast,
#             basin=basin
#         )
#
#         completions_ratios, completions_ratio_fig = CompletionsRatios.update_ratios(
#             completions_history=completions_history,
#             completions_forecast=new_completions,
#             drilled_wells_history=drilled_wells_history,
#             drilled_wells_forecast=drilled_wells_forecast
#         )
#         new_ducs, ducs_fig = DUCsVisualiser.update_ducs(
#             existing_ducs=existing_ducs,
#             new_completions=new_completions,
#             new_drilled_wells=drilled_wells_forecast,
#             basin=basin
#         )
#
#         packed_new_drilled_wells_ratios = pack_data(drilled_wells_ratios)
#         packed_new_completions = pack_data(new_completions)
#         packed_new_completions_ratios = pack_data(completions_ratios)
#         packed_new_ducs = pack_data(new_ducs)
#
#         pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             basins_filter=get_basins_filter(basin),
#             energy_product_filter=[energy_product]
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=unconventional_existing,
#             unconventional_future_df=unconventional_future,
#             continuous_conventional_df=continuous_conventional,
#             eia_df=eia_production,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         modified_plays = production_visual.get_modified_plays_completions(
#             previous_df=previous_drilled_wells_forecast,
#             new_df=drilled_wells_forecast
#         )
#         tc_loader = TypeCurveLoader(
#             novi_type_curves=novi_type_curves,
#             override_type_curves=override_type_curves,
#             available_type_curves=available_type_curves
#         )
#         vintages = list(eia_production.index.year.unique())
#
#         tc_loader.load_type_curves(energy_products=[energy_product], ea_plays=modified_plays, vintages_filter=vintages)
#         type_curves = tc_loader.get_prioritized_type_curves()
#
#         production_visual.recalculate_future_wells_production(
#             type_curves=type_curves,
#             completions_history=completions_history,
#             completions_forecasts=new_completions,
#             plays_to_recalculate=modified_plays
#         )
#
#         prod_fig, prod_columns, prod_data, prod_total_columns, prod_total_data = production_visual.process_and_visualise_data()
#         packed_unconventional_future = pack_data(production_visual.get_storage_format_future_wells_prod())
#
#         packed_rig_count_table_data = pack_data(rig_count_forecast)
#
#         drilled_wells_fig = preserve_figure_state(drilled_wells_fig, previous_drilled_wells_fig)
#         drilled_wells_ratio_fig = preserve_figure_state(drilled_wells_ratio_fig, previous_drilled_ratio_fig)
#         completions_fig = preserve_figure_state(completions_fig, previous_completions_fig)
#         completions_ratio_fig = preserve_figure_state(completions_ratio_fig, previous_completions_ratio_fig)
#         ducs_fig = preserve_figure_state(ducs_fig, previous_ducs_fig)
#         prod_fig = preserve_figure_state(prod_fig, previous_prod_fig)
#
#         total_drilled_wells_columns, total_drilled_wells_data = DrilledWellsVisualiser.make_total_table(drilled_wells_forecast)
#         total_completions_columns, total_completions_data = CompletionsVisualiser.make_total_table(new_completions)
#         completions_table_previous_data = False
#         download_button_disabled = False
#         save_button_disabled = False
#
#         return (packed_rig_count_table_data, drilled_wells_table_data,
#             drilled_wells_fig, packed_new_drilled_wells_ratios, drilled_wells_ratio_fig,
#                 total_drilled_wells_data, drilled_wells_stored_previous_data,
#                 packed_new_completions, completions_fig, packed_new_completions_ratios, completions_ratio_fig,
#                 packed_new_ducs, ducs_fig,
#                 packed_unconventional_future, prod_columns, prod_data, prod_total_columns, prod_total_data, prod_fig,
#                 completions_table_previous_data, total_completions_data,
#                 download_button_disabled, save_button_disabled
#                 )
#
#     @callback(
#         Output(f"{prefix}drilled-wells-table", "data", allow_duplicate=True),
#         Output(f"{prefix}drilled-wells-table-previous", "data", allow_duplicate=True),
#         Input(f"{prefix}drilled-wells-table-total", "data"),
#         State(f"{prefix}drilled-wells-table-total", "data_previous"),
#         State(f"{prefix}drilled-wells-table", "data"),
#         prevent_initial_call=True
#     )
#     def update_play_level_drilled_wells_table_on_total_change(new_total_data, old_total_data, existing_play_level_data):
#         if new_total_data is None or old_total_data is None:
#             raise PreventUpdate
#
#         new_play_level_data = existing_play_level_data.copy()
#         new_play_level_data = unpack_data(new_play_level_data)
#         new_total_data = unpack_total_data(new_total_data)
#         old_total_data = unpack_total_data(old_total_data)
#
#         new_play_level_data = DrilledWellsVisualiser.update_play_level_data_from_totals(new_total_data=new_total_data,
#                                                                                     old_total_data=old_total_data,
#                                                                                     play_level_data=new_play_level_data)
#         play_level_data = pack_data(new_play_level_data)
#
#         return play_level_data, existing_play_level_data
#
#     @callback(
#         Output(f'{prefix}completions-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}completions-ratios', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-ratio-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}completions-table-total', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-table-previous', 'data', allow_duplicate=True),
#         Output(f'{prefix}ducs-data', 'data', allow_duplicate=True),
#         Output(f'{prefix}ducs-graph', 'figure', allow_duplicate=True),
#
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#
#         Output(f'{prefix}download-data-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}save-to-db-btn', 'disabled', allow_duplicate=True),
#
#         Output(f'{prefix}drilled-wells-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}rig-count-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-table', 'data', allow_duplicate=True),
#
#         Input(f'{prefix}completions-table', 'data'),
#         State(f'{prefix}completions-table', 'data_previous'),
#         State(f'{prefix}completions-table-previous', 'data'),
#         State(f'{prefix}completions-history', 'data'),
#         State(f'{prefix}drilled-wells-history', 'data'),
#         State(f'{prefix}drilled-wells-table', 'data'),
#         State(f'{prefix}ducs-data', 'data'),
#
#         State(f'{prefix}rig-count-table', 'data'),
#
#         State(f'{prefix}available-type-curves', 'data'),
#         State(f'{prefix}novi-type-curves', 'data'),
#         State(f'{prefix}type-curves-overrides', 'data'),
#
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#
#         State(f'{prefix}completions-graph', 'figure'),
#         State(f'{prefix}completions-ratio-graph', 'figure'),
#         State(f'{prefix}ducs-graph', 'figure'),
#         State(f'{prefix}production-graph', 'figure'),
#         prevent_initial_call=True
#     )
#     def completions_table_update(completions_table_data: List[Dict],
#                                  completions_table_previous_data: List[Dict],
#                                  completions_stored_previous_data: List[Dict],
#                                  completions_history: List[Dict],
#
#                                  drilled_wells_history: List[Dict],
#                                  drilled_wells_forecast: List[Dict],
#                                  ducs_data: List[Dict],
#
#                                  rig_count_table_data: List[Dict],
#
#                                  available_type_curves: List[Dict],
#                                  novi_type_curves: List[Dict],
#                                  type_curve_overrides: List[Dict],
#
#                                  unconventional_existing_data: List[Dict],
#                                  unconventional_future_data: List[Dict],
#                                  continuous_conventional_data: List[Dict],
#                                  eia_data: List[Dict],
#
#                                  basin: UsBasins,
#                                  energy_product: EnergyProduct,
#
#                                  previous_completions_fig,
#                                  previous_completions_ratio_fig,
#                                  previous_ducs_fig,
#                                  previous_prod_fig,
#
#                                  ) -> tuple:
#         """We are here because a user updated the completions table.
#         We need to update the completions to drilled wells ratio.
#         This doesn't affect the rig count or drilled wells data.
#         """
#         if completions_table_data is None:
#             raise PreventUpdate
#         if completions_table_previous_data is None:
#             if not completions_stored_previous_data:
#                 raise PreventUpdate
#
#         if completions_stored_previous_data:
#             completions_table_previous_data = completions_stored_previous_data.copy()
#             completions_stored_previous_data = False
#
#         completions_forecast = unpack_data(completions_table_data)
#         previous_completions_forecast = unpack_data(completions_table_previous_data)
#         completions_history = unpack_data(completions_history)
#         drilled_wells_history = unpack_data(drilled_wells_history)
#         drilled_wells_forecast = unpack_data(drilled_wells_forecast)
#         existing_ducs = unpack_data(ducs_data)
#         available_type_curves = unpack_data(available_type_curves)
#         novi_type_curves = unpack_data(novi_type_curves)
#         override_type_curves = unpack_data(type_curve_overrides)
#
#         unconventional_existing = unpack_data(unconventional_existing_data)
#         unconventional_future = unpack_data(unconventional_future_data)
#         continuous_conventional = unpack_data(continuous_conventional_data)
#         eia_production = unpack_data(eia_data)
#
#         if is_initial_load(previous_completions_forecast, completions_forecast):
#             raise PreventUpdate
#
#         if previous_completions_forecast.equals(completions_forecast):
#             raise PreventUpdate
#
#         completions_columns, completions_data, completions_fig = CompletionsVisualiser.visualise_data(
#             history_df=completions_history,
#             forecast_df=completions_forecast,
#             title=ChartTitles.COMPLETIONS
#         )
#
#         completions_ratios, completions_ratio_fig = CompletionsRatios.update_ratios(
#             completions_history=completions_history,
#             completions_forecast=completions_forecast,
#             drilled_wells_history=drilled_wells_history,
#             drilled_wells_forecast=drilled_wells_forecast
#         )
#
#         new_ducs, ducs_fig = DUCsVisualiser.update_ducs(
#             existing_ducs=existing_ducs,
#             new_completions=completions_forecast,
#             new_drilled_wells=drilled_wells_forecast,
#             basin=basin
#         )
#
#         packed_new_ducs = pack_data(new_ducs)
#         packed_new_completions_ratios = pack_data(completions_ratios)
#
#         pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             basins_filter=get_basins_filter(basin),
#             energy_product_filter=[energy_product]
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=unconventional_existing,
#             unconventional_future_df=unconventional_future,
#             continuous_conventional_df=continuous_conventional,
#             eia_df=eia_production,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         modified_plays = production_visual.get_modified_plays_completions(
#             previous_df=previous_completions_forecast,
#             new_df=completions_forecast
#         )
#
#         tc_loader = TypeCurveLoader(
#             novi_type_curves=novi_type_curves,
#             override_type_curves=override_type_curves,
#             available_type_curves=available_type_curves
#         )
#         vintages = list(eia_production.index.year.unique())
#         tc_loader.load_type_curves(energy_products=[energy_product], ea_plays=modified_plays, vintages_filter=vintages)
#         type_curves = tc_loader.get_prioritized_type_curves()
#
#         production_visual.recalculate_future_wells_production(
#             type_curves=type_curves,
#             completions_history=completions_history,
#             completions_forecasts=completions_forecast,
#             plays_to_recalculate=modified_plays
#         )
#         prod_fig, prod_columns, prod_data, prod_total_columns, prod_total_data = production_visual.process_and_visualise_data()
#         packed_unconventional_future = pack_data(production_visual.get_storage_format_future_wells_prod())
#
#         completions_fig = preserve_figure_state(completions_fig, previous_completions_fig)
#         completions_ratio_fig = preserve_figure_state(completions_ratio_fig, previous_completions_ratio_fig)
#         ducs_fig = preserve_figure_state(ducs_fig, previous_ducs_fig)
#         prod_fig = preserve_figure_state(prod_fig, previous_prod_fig)
#
#         total_completions_columns, total_completions_data = CompletionsVisualiser.make_total_table(
#             completions_forecast)
#
#         download_button_disabled = False
#         save_button_disabled = False
#
#         packed_drilled_wells_table_data = pack_data(drilled_wells_forecast)
#
#         return (completions_fig, packed_new_completions_ratios, completions_ratio_fig, total_completions_data,
#                 completions_stored_previous_data, packed_new_ducs, ducs_fig,
#                 packed_unconventional_future, prod_columns, prod_data, prod_total_columns, prod_total_data, prod_fig,
#                 download_button_disabled, save_button_disabled,
#                 packed_drilled_wells_table_data, rig_count_table_data, completions_table_data
#         )
#
#     @callback(
#         Output(f"{prefix}completions-table", "data", allow_duplicate=True),
#         Output(f"{prefix}completions-table-previous", "data", allow_duplicate=True),
#         Input(f"{prefix}completions-table-total", "data"),
#         State(f"{prefix}completions-table-total", "data_previous"),
#         State(f"{prefix}completions-table", "data"),
#         prevent_initial_call=True
#     )
#     def update_play_level_completions_table_on_total_change(new_total_data, old_total_data, existing_play_level_data):
#         if new_total_data is None or old_total_data is None:
#             raise PreventUpdate
#
#         new_play_level_data = existing_play_level_data.copy()
#         new_play_level_data = unpack_data(new_play_level_data)
#         new_total_data = unpack_total_data(new_total_data)
#         old_total_data = unpack_total_data(old_total_data)
#
#         new_play_level_data = CompletionsVisualiser.update_play_level_data_from_totals(new_total_data=new_total_data,
#                                                                                         old_total_data=old_total_data,
#                                                                                         play_level_data=new_play_level_data)
#         play_level_data = pack_data(new_play_level_data)
#
#         return play_level_data, existing_play_level_data
#
#     @callback(
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}unconventional-existing', 'data', allow_duplicate=True),
#         Output(f'{prefix}download-data-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}save-to-db-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}production-table-total', 'data', allow_duplicate=True),
#
#         Input(f'{prefix}production-table', 'data'),
#         State(f'{prefix}production-table', 'data_previous'),
#         State(f'{prefix}production-table-previous', 'data'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#
#         State(f'{prefix}basin-selection-ddown', 'value'),
#
#         State(f'{prefix}production-graph', 'figure'),
#
#         prevent_initial_call=True
#     )
#     def production_table_update(
#             production_table_data, production_table_previous_data, production_stored_previous_data,
#             unconventional_existing_data, unconventional_future_data,
#             continuous_conventional_data, eia_data, eia_basin, previous_prod_fig,
#     ):
#         if production_table_data is None:
#             raise PreventUpdate
#         if production_table_previous_data is None:
#             if not production_stored_previous_data:
#                 raise PreventUpdate
#
#         if production_stored_previous_data:
#             completions_table_previous_data = production_stored_previous_data.copy()
#             completions_stored_previous_data = False
#
#         new_production_df = unpack_data(production_table_data)
#
#         updated_existing_production = ProductionVisualiser.update_adjustment_series(
#             unconventional_existing_df=unpack_data(unconventional_existing_data),
#             new_production_table=new_production_df
#         )
#
#         pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             basins_filter=get_basins_filter(eia_basin),
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=updated_existing_production,
#             unconventional_future_df=unpack_data(unconventional_future_data),
#             continuous_conventional_df=unpack_data(continuous_conventional_data),
#             eia_df=unpack_data(eia_data),
#             eia_basin=eia_basin,
#             pipeline=pipeline
#         )
#         fig = preserve_figure_state(production_visual.make_chart(), previous_prod_fig)
#
#         new_existing_wells_prod_data = pack_data(updated_existing_production)
#
#         total_table_df = pd.DataFrame({
#             "date": new_production_df.index,
#             "Total": new_production_df.drop(columns=["date"], errors="ignore").sum(axis=1)
#         })
#         total_table_data = total_table_df.to_dict("records")
#
#         download_button_disabled = False
#         save_button_disabled = False
#
#         return fig, new_existing_wells_prod_data, download_button_disabled, save_button_disabled, total_table_data
#
#     @callback(
#
#         Output(f'{prefix}create-new-play-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}create-new-play-dropdown', 'options', allow_duplicate=True),
#
#         Output(f'{prefix}edit-play-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}edit-play-dropdown', 'options', allow_duplicate=True),
#
#         Output(f'{prefix}delete-play-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}delete-play-dropdown', 'options', allow_duplicate=True),
#
#         Output(f'{prefix}type-curve-mode', 'data', allow_duplicate=True),
#
#         Input(f'{prefix}type-curve-tabs', 'active_tab'),
#
#         State(f'{prefix}available-type-curves', 'data'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         State(f'{prefix}start-date-ddown', 'value'),
#         State(f'{prefix}end-date-ddown', 'value'),
#         prevent_initial_call=True
#     )
#     def type_curve_tab_change(active_tab, available_type_curves, energy_product, basin,
#                               scenario_type, start_date, end_date):
#         if active_tab not in ["create-new", "edit", "delete"]:
#             raise PreventUpdate
#
#         create_value = []
#         create_options = []
#         edit_value = []
#         edit_options = []
#         delete_value = []
#         delete_options = []
#
#         if active_tab == "create-new":
#             available_type_curves = unpack_data(available_type_curves)
#             plays = sorted(available_type_curves[ModelMetadata.EA_PLAY].unique())
#             create_options = [{'label': play, 'value': play} for play in plays]
#
#         elif active_tab == "edit":
#             available_type_curves = unpack_data(available_type_curves)
#             plays = sorted(available_type_curves[ModelMetadata.EA_PLAY].unique())
#             edit_options = [{'label': play, 'value': play} for play in plays]
#
#         elif active_tab == "delete":
#             available_type_curves = unpack_data(available_type_curves)
#             override_type_curves = available_type_curves[available_type_curves[TypeCurveMetadata.TYPE_CURVE_TYPE] == TypeCurveMetadata.OVERRIDE]
#
#             if override_type_curves is not None and not override_type_curves.empty:
#                 override_plays = sorted(override_type_curves[ModelMetadata.EA_PLAY].unique())
#                 delete_options = [{'label': play, 'value': play} for play in override_plays]
#
#
#         return (
#             create_value,
#             create_options,
#             edit_value,
#             edit_options,
#             delete_value,
#             delete_options,
#             active_tab,
#         )
#
#     @callback(
#         Output(f'{prefix}create-new-vintage-to-copy-dropdown', 'options', allow_duplicate=True),
#         Output(f'{prefix}create-new-vintage-to-copy-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}create-new-vintage-to-generate-dropdown', 'options', allow_duplicate=True),
#         Output(f'{prefix}create-new-vintage-to-generate-dropdown', 'value', allow_duplicate=True),
#         Input(f'{prefix}create-new-play-dropdown', 'value'),
#         State(f'{prefix}type-curve-mode', 'data'),
#         State(f'{prefix}novi-type-curves', 'data'),
#         State(f'{prefix}type-curves-overrides', 'data'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         State(f'{prefix}start-date-ddown', 'value'),
#         State(f'{prefix}end-date-ddown', 'value'),
#         prevent_initial_call=True
#     )
#     def type_curve_update_create_vintage_options(selected_plays, mode,
#                                                  novi_type_curves, override_type_curves,
#                                                  energy_product, basin, scenario_type,
#                                                  start_date, end_date):
#         if not selected_plays or mode != "create-new" or not isinstance(selected_plays, list):
#             raise PreventUpdate
#
#         basins_filter = get_basins_filter(basin)
#
#         pipeline = GlobalPipeline.build_pipeline_from_parameters(
#             scenario_type=scenario_type,
#             basins_filter=basins_filter,
#             energy_product_filter=[energy_product],
#             start_date=start_date,
#             end_date=end_date
#         )
#
#         novi_type_curves = pipeline.adjusted_type_curves
#         override_type_curves = pipeline.override_type_curves
#
#         existing_vintages = set()
#         for df in [novi_type_curves, override_type_curves]:
#             if df is not None and not df.empty:
#                 mask = df[ModelMetadata.EA_PLAY].isin(selected_plays)
#                 existing_vintages.update(df[mask][ModelMetadata.VINTAGE].unique())
#
#         vintage_to_copy_options = [{'label': str(year), 'value': year}
#                                for year in sorted(existing_vintages)]
#         vintage_to_copy_value = []
#
#         min_year = pd.to_datetime(start_date).year
#         max_year = pd.to_datetime(end_date).year
#         vintage_to_generate_options = [{'label': str(year), 'value': year}
#                                        for year in range(min_year, max_year + 1)
#                                        if year not in existing_vintages]
#         vintage_to_generate_value = []
#
#         return (
#             vintage_to_copy_options,
#             vintage_to_copy_value,
#             vintage_to_generate_options,
#             vintage_to_generate_value
#         )
#
#     @callback(
#         Output(f'{prefix}edit-vintage-dropdown', 'options', allow_duplicate=True),
#         Output(f'{prefix}edit-vintage-dropdown', 'value', allow_duplicate=True),
#         Input(f'{prefix}edit-play-dropdown', 'value'),
#         State(f'{prefix}type-curve-mode', 'data'),
#         State(f'{prefix}novi-type-curves', 'data'),
#         State(f'{prefix}type-curves-overrides', 'data'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         State(f'{prefix}start-date-ddown', 'value'),
#         State(f'{prefix}end-date-ddown', 'value'),
#         prevent_initial_call=True
#     )
#     def type_curve_update_edit_vintage_options(selected_plays, mode,
#                                                novi_type_curves, override_type_curves,
#                                                energy_product, basin, scenario_type,
#                                                start_date, end_date):
#         if not selected_plays or mode != "edit" or not isinstance(selected_plays, list):
#             raise PreventUpdate
#
#         basins_filter = get_basins_filter(basin)
#
#         pipeline = GlobalPipeline.build_pipeline_from_parameters(
#             scenario_type=scenario_type,
#             basins_filter=basins_filter,
#             energy_product_filter=[energy_product],
#             start_date=start_date,
#             end_date=end_date
#         )
#
#         novi_type_curves = pipeline.adjusted_type_curves
#         override_type_curves = pipeline.override_type_curves
#
#         existing_vintages = set()
#         for df in [novi_type_curves, override_type_curves]:
#             if df is not None and not df.empty:
#                 mask = df[ModelMetadata.EA_PLAY].isin(selected_plays)
#                 existing_vintages.update(df[mask][ModelMetadata.VINTAGE].unique())
#
#         vintage_options = [{'label': str(year), 'value': year}
#                            for year in sorted(existing_vintages)]
#
#         edit_vintage_dropdown_value = []
#         return vintage_options, edit_vintage_dropdown_value
#
#     @callback(
#         Output(f'{prefix}delete-vintage-dropdown', 'options', allow_duplicate=True),
#         Output(f'{prefix}delete-vintage-dropdown', 'value', allow_duplicate=True),
#         Input(f'{prefix}delete-play-dropdown', 'value'),
#         State(f'{prefix}type-curve-mode', 'data'),
#         State(f'{prefix}available-type-curves', 'data'),
#         prevent_initial_call=True
#     )
#     def type_curve_update_delete_vintage_options(selected_plays, mode, available_type_curves):
#         if not selected_plays or mode != "delete" or not isinstance(selected_plays, list):
#             raise PreventUpdate
#
#         available_type_curves = unpack_data(available_type_curves)
#         override_type_curves = available_type_curves[available_type_curves[TypeCurveMetadata.TYPE_CURVE_TYPE]==TypeCurveMetadata.OVERRIDE]
#
#         existing_vintages = set()
#         if override_type_curves is not None and not override_type_curves.empty:
#             mask = override_type_curves[ModelMetadata.EA_PLAY].isin(selected_plays)
#             existing_vintages.update(override_type_curves[mask][ModelMetadata.VINTAGE].unique())
#
#         vintage_options = [{'label': str(year), 'value': year}
#                            for year in sorted(existing_vintages)]
#
#         delete_vintage_dropdown_value = []
#         return vintage_options, delete_vintage_dropdown_value
#
#     @callback(
#         Output(f'{prefix}create-new-generate-btn', 'disabled'),
#         Input(f'{prefix}create-new-play-dropdown', 'value'),
#         Input(f'{prefix}create-new-vintage-to-copy-dropdown', 'value'),
#         Input(f'{prefix}type-curve-tabs', 'active_tab'),
#     )
#     def update_create_generate_button_state(create_plays, vintage_to_copy, active_tab):
#         if active_tab != "create-new":
#             return True
#
#         if not create_plays or len(create_plays) == 0:
#             return True
#
#         if not (vintage_to_copy and len(vintage_to_copy) > 0):
#             return True
#
#         return False
#
#     @callback(
#         Output(f'{prefix}edit-generate-btn', 'disabled'),
#         Input(f'{prefix}edit-play-dropdown', 'value'),
#         Input(f'{prefix}edit-vintage-dropdown', 'value'),
#         Input(f'{prefix}type-curve-tabs', 'active_tab'),
#     )
#     def update_edit_generate_button_state(edit_plays, edit_vintage, active_tab):
#         if active_tab != "edit":
#             return True
#
#         if not edit_plays or len(edit_plays) == 0:
#             return True
#
#         if not edit_vintage or len(edit_vintage) == 0:
#             return True
#
#         return False
#
#     @callback(
#         Output(f'{prefix}delete-generate-btn', 'disabled'),
#         Input(f'{prefix}delete-play-dropdown', 'value'),
#         Input(f'{prefix}delete-vintage-dropdown', 'value'),
#         Input(f'{prefix}type-curve-tabs', 'active_tab'),
#     )
#     def update_delete_generate_button_state(delete_plays, delete_vintage, active_tab):
#         if active_tab != "delete":
#             return True
#
#         if not delete_plays or len(delete_plays) == 0:
#             return True
#
#         if not delete_vintage or len(delete_vintage) == 0:
#             return True
#
#         return False
#
#     @callback(
#         Output(f'{prefix}create-new-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}create-new-parameter-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}create-new-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}create-new-selected-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}create-new-parameter-table', 'selected_rows', allow_duplicate=True),
#
#         Input(f'{prefix}create-new-generate-btn', 'n_clicks'),
#
#         State(f'{prefix}create-new-play-dropdown', 'value'),
#         State(f'{prefix}create-new-vintage-to-copy-dropdown', 'value'),
#         State(f'{prefix}available-type-curves', 'data'),
#         State(f'{prefix}type-curve-mode', 'data'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#
#         prevent_initial_call=True
#     )
#     def display_create_new_type_curves(n_clicks, selected_plays, vintages_to_copy, available_type_curves,
#                                  mode, scenario_type):
#         if not n_clicks or mode != "create-new":
#             raise PreventUpdate
#
#         if not isinstance(selected_plays, list) or not isinstance(vintages_to_copy, list):
#             raise PreventUpdate
#
#         if not selected_plays or not vintages_to_copy:
#             raise PreventUpdate
#
#         available_type_curves = unpack_data(available_type_curves)
#         available_type_curves_to_copy = available_type_curves[
#             (available_type_curves[ModelMetadata.VINTAGE].isin(vintages_to_copy)) &
#             (available_type_curves[ModelMetadata.EA_PLAY].isin(selected_plays))
#             ]
#         pipe = GlobalPipeline(scenario_type=scenario_type)
#         pipe._adjusted_type_curves = available_type_curves_to_copy[available_type_curves_to_copy[TypeCurveMetadata.TYPE_CURVE_TYPE]==TypeCurveMetadata.NOVI]
#         pipe._override_type_curves = available_type_curves_to_copy[available_type_curves_to_copy[TypeCurveMetadata.TYPE_CURVE_TYPE]==TypeCurveMetadata.OVERRIDE]
#         prioritised_type_curves_to_copy = pipe.prioritized_type_curves
#
#         table_data = populate_existing_table(prioritised_type_curves_to_copy, selected_plays, vintages_to_copy)
#
#         fig = populate_graph(table_data)
#
#         columns = TypeCurveTile.make_parameter_table_value_column(editable=False)
#
#         selected_table_data = []
#         table_selected_rows = []
#
#         return table_data, columns, fig, selected_table_data, table_selected_rows
#
#     @callback(
#         Output(f'{prefix}edit-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}edit-parameter-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}edit-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}edit-selected-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}edit-parameter-table', 'selected_rows', allow_duplicate=True),
#
#         Input(f'{prefix}edit-generate-btn', 'n_clicks'),
#
#         State(f'{prefix}edit-play-dropdown', 'value'),
#         State(f'{prefix}edit-vintage-dropdown', 'value'),
#         State(f'{prefix}available-type-curves', 'data'),
#         State(f'{prefix}type-curve-mode', 'data'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#
#         prevent_initial_call=True
#     )
#     def display_edit_type_curves(n_clicks, selected_plays, selected_vintages, available_type_curves,
#                                  mode, scenario_type):
#         if not n_clicks or mode != "edit":
#             raise PreventUpdate
#
#         if not isinstance(selected_plays, list) or not isinstance(selected_vintages, list):
#             raise PreventUpdate
#
#         if not selected_plays or not selected_vintages:
#             raise PreventUpdate
#
#         available_type_curves = unpack_data(available_type_curves)
#         available_type_curves = available_type_curves[
#             (available_type_curves[ModelMetadata.VINTAGE].isin(selected_vintages)) &
#             (available_type_curves[ModelMetadata.EA_PLAY].isin(selected_plays))
#             ]
#         pipe = GlobalPipeline(scenario_type=scenario_type)
#         pipe._adjusted_type_curves = available_type_curves[available_type_curves[TypeCurveMetadata.TYPE_CURVE_TYPE]==TypeCurveMetadata.NOVI]
#         pipe._override_type_curves = available_type_curves[available_type_curves[TypeCurveMetadata.TYPE_CURVE_TYPE]==TypeCurveMetadata.OVERRIDE]
#         prioritised_type_curves = pipe.prioritized_type_curves
#
#         table_data = populate_existing_table(prioritised_type_curves, selected_plays, selected_vintages)
#
#         fig = populate_graph(table_data)
#
#         columns = TypeCurveTile.make_parameter_table_value_column(editable=False)
#
#         selected_table_data = []
#         table_selected_rows = []
#
#         return table_data, columns, fig, selected_table_data, table_selected_rows
#
#     @callback(
#         Output(f'{prefix}delete-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}delete-parameter-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}delete-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}delete-selected-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}delete-parameter-table', 'selected_rows', allow_duplicate=True),
#
#         Input(f'{prefix}delete-generate-btn', 'n_clicks'),
#
#         State(f'{prefix}delete-play-dropdown', 'value'),
#         State(f'{prefix}delete-vintage-dropdown', 'value'),
#         State(f'{prefix}available-type-curves', 'data'),
#         State(f'{prefix}type-curve-mode', 'data'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#
#         prevent_initial_call=True
#     )
#     def display_delete_type_curves(n_clicks, selected_plays, selected_vintages, available_type_curves,
#                                     mode, scenario_type):
#         if not n_clicks or mode != "delete":
#             raise PreventUpdate
#
#         if not isinstance(selected_plays, list) or not isinstance(selected_vintages, list):
#             raise PreventUpdate
#
#         if not selected_plays or not selected_vintages:
#             raise PreventUpdate
#
#         available_type_curves = unpack_data(available_type_curves)
#         available_type_curves = available_type_curves[
#             (available_type_curves[ModelMetadata.VINTAGE].isin(selected_vintages)) &
#             (available_type_curves[ModelMetadata.EA_PLAY].isin(selected_plays))
#             ]
#         override_type_curves = available_type_curves[available_type_curves[TypeCurveMetadata.TYPE_CURVE_TYPE]==TypeCurveMetadata.OVERRIDE]
#
#         table_data = populate_existing_table(override_type_curves, selected_plays, selected_vintages)
#         fig = populate_graph(table_data)
#         columns = TypeCurveTile.make_parameter_table_value_column(editable=False)
#
#         selected_table_data = []
#         table_selected_rows = []
#
#         return table_data, columns, fig, selected_table_data, table_selected_rows
#
#     @callback(
#         Output(f'{prefix}create-new-selected-parameter-table', 'data'),
#         Output(f'{prefix}create-new-selected-table-container', 'style'),
#         Input(f'{prefix}create-new-parameter-table', 'selected_rows'),
#         Input(f'{prefix}create-new-vintage-to-generate-dropdown', 'value'),
#         State(f'{prefix}create-new-parameter-table', 'data'),
#         State(f'{prefix}create-new-selected-parameter-table', 'data'),
#         prevent_initial_call=True
#     )
#     def update_create_new_selected_type_curves_table(selected_rows, vintages_to_generate, main_table_data, existing_selected_type_curves_data):
#         if not selected_rows or not vintages_to_generate:
#             return [], {'display': 'none'}
#         new_selected_data = []
#         for i in selected_rows:
#             existing_play = next(
#                 (selected_dict for selected_dict in existing_selected_type_curves_data
#                  if selected_dict[ModelMetadata.EA_PLAY] == main_table_data[i][ModelMetadata.EA_PLAY]),
#                 None
#             )
#
#             if not existing_play:
#                 for vintage in vintages_to_generate:
#                     new_vintage_data = main_table_data[i].copy()
#                     new_vintage_data[ModelMetadata.VINTAGE] = vintage
#                     new_selected_data.append(new_vintage_data)
#             else:
#                 already_in_new_data = any(
#                     item[ModelMetadata.EA_PLAY] == main_table_data[i][ModelMetadata.EA_PLAY] for item in new_selected_data
#                 )
#                 if not already_in_new_data:
#                     new_selected_data.append(existing_play)
#
#         selected_data = [
#             {**row, TypeCurveMetadata.TYPE_CURVE_TYPE: f'New {TypeCurveMetadata.OVERRIDE}'}
#             for row in new_selected_data
#         ]
#         return selected_data, {'display': 'block'}
#
#     @callback(
#         Output(f'{prefix}create-new-parameter-table', 'style_data_conditional'),
#         Input(f'{prefix}create-new-parameter-table', 'selected_rows'),
#         State(f'{prefix}create-new-parameter-table', 'data'),
#         prevent_initial_call=True
#     )
#     def create_new_grey_out_plays_already_selected(selected_rows, table_data):
#         styles = []
#
#         if not selected_rows:
#             return styles
#
#         selected_plays = set()
#         for row_idx in selected_rows:
#             selected_plays.add(table_data[row_idx][ModelMetadata.EA_PLAY])
#
#         for i, row in enumerate(table_data):
#             current_play = row[ModelMetadata.EA_PLAY]
#             if current_play in selected_plays and i not in selected_rows:
#                 styles.append({
#                     'if': {'row_index': i},
#                     'opacity': 0.5,
#                     'cursor': 'not-allowed',
#                     'background-color': '#f0f0f0',
#                 })
#
#         return styles
#
#     @callback(
#         Output(f'{prefix}create-new-parameter-table', 'selected_rows'),
#         Input(f'{prefix}create-new-parameter-table', 'selected_rows'),
#         State(f'{prefix}create-new-parameter-table', 'data'),
#         prevent_initial_call=True
#     )
#     def create_new_reject_erroneous_selected_rows(selected_rows, table_data):
#         if not selected_rows:
#             return []
#
#         processed_plays = set()
#         filtered_selected_rows = []
#
#         for row_idx in selected_rows:
#             current_play = table_data[row_idx][ModelMetadata.EA_PLAY]
#
#             if current_play not in processed_plays:
#                 processed_plays.add(current_play)
#                 filtered_selected_rows.append(row_idx)
#
#         return filtered_selected_rows
#
#     @callback(
#         Output(f'{prefix}edit-selected-parameter-table', 'data'),
#         Output(f'{prefix}edit-selected-table-container', 'style'),
#         Input(f'{prefix}edit-parameter-table', 'selected_rows'),
#         State(f'{prefix}edit-parameter-table', 'data'),
#         State(f'{prefix}edit-selected-parameter-table', 'data'),
#         prevent_initial_call=True
#     )
#     def update_edit_selected_type_curves_table(selected_rows, main_table_data, existing_selected_type_curves_data):
#         if not selected_rows:
#             return [], {'display': 'none'}
#         new_selected_data = []
#         for i in selected_rows:
#             existing_play_vintage_combination = next(
#                 (selected_dict for selected_dict in existing_selected_type_curves_data
#                  if (selected_dict[ModelMetadata.EA_PLAY] == main_table_data[i][ModelMetadata.EA_PLAY] and
#                      selected_dict[ModelMetadata.VINTAGE] == main_table_data[i][ModelMetadata.VINTAGE])),
#                 None
#             )
#
#             if not existing_play_vintage_combination:
#                 new_selected_data.append(main_table_data[i])
#             else:
#                 new_selected_data.append(existing_play_vintage_combination)
#
#         selected_data = [
#             {**row, TypeCurveMetadata.TYPE_CURVE_TYPE: f'New {TypeCurveMetadata.OVERRIDE}'}
#             for row in new_selected_data
#         ]
#         return selected_data, {'display': 'block'}
#
#
#     @callback(
#         Output(f'{prefix}delete-selected-parameter-table', 'data'),
#         Output(f'{prefix}delete-selected-table-container', 'style'),
#         Input(f'{prefix}delete-parameter-table', 'selected_rows'),
#         State(f'{prefix}delete-parameter-table', 'data'),
#         prevent_initial_call=True
#     )
#     def update_delete_selected_type_curves_table(selected_rows, main_table_data):
#         if not selected_rows:
#             return [], {'display': 'none'}
#         selected_data = [main_table_data[i] for i in selected_rows]
#         return selected_data, {'display': 'block'}
#
#     @callback(
#         Output(f'{prefix}create-new-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}create-new-selected-parameter-table', 'data', allow_duplicate=True),
#         Input(f'{prefix}create-new-selected-parameter-table', 'data'),
#         State(f'{prefix}create-new-parameter-table', 'data'),
#
#         prevent_initial_call=True
#     )
#     def create_new_selected_parameter_table_update(selected_table_data, parameter_table_data):
#         if not selected_table_data:
#             raise PreventUpdate
#
#         selected_table_data = update_type_curve_metrics_from_parameter_table_data(selected_table_data)
#
#         fig = populate_graph(parameter_table_data)
#
#         fig = populate_graph(selected_table_data, existing_figure=fig)
#
#         return fig, selected_table_data
#
#     @callback(
#         Output(f'{prefix}edit-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}edit-selected-parameter-table', 'data', allow_duplicate=True),
#         Input(f'{prefix}edit-selected-parameter-table', 'data'),
#         State(f'{prefix}edit-parameter-table', 'data'),
#
#         prevent_initial_call=True
#     )
#     def edit_selected_parameter_table_update(selected_table_data, parameter_table_data):
#         if not selected_table_data:
#             raise PreventUpdate
#
#         selected_table_data = update_type_curve_metrics_from_parameter_table_data(selected_table_data)
#
#         fig = populate_graph(parameter_table_data)
#
#         fig = populate_graph(selected_table_data, existing_figure=fig)
#
#         return fig, selected_table_data
#
#     @callback(
#         Output(f'{prefix}create-new-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}create-new-selected-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}create-new-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}type-curve-save-loader', 'children', allow_duplicate=True),
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}available-type-curves', 'data', allow_duplicate=True),
#         Output(f'{prefix}unsaved-applied-changes-bool', 'data', allow_duplicate=True),
#
#         Input(f'{prefix}create-save-btn', 'n_clicks'),
#
#         State(f'{prefix}create-new-play-dropdown', 'value'),
#         State(f'{prefix}create-new-vintage-to-generate-dropdown', 'value'),
#         State(f'{prefix}create-new-parameter-table', 'data'),
#         State(f'{prefix}create-new-selected-parameter-table', 'data'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         State(f'{prefix}start-date-ddown', 'value'),
#         State(f'{prefix}end-date-ddown', 'value'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#         State(f'{prefix}completions-history', 'data'),
#         State(f'{prefix}completions-table', 'data'),
#         State(f'{prefix}rig-count-table', 'data'),
#         State(f'{prefix}drilled-wells-table', 'data'),
#         State(f'{prefix}available-type-curves', 'data'),
#         prevent_initial_call=True
#     )
#     def create_new_tab_type_curve_save(
#             create_clicks,
#             selected_plays: List[str],
#             vintages_to_generate: List[int],
#             standard_parameter_data: List[Dict],
#             selected_parameter_data: List[Dict],
#             energy_product: EnergyProduct,
#             basin: UsBasins,
#             scenario_type: ScenarioTypes,
#             start_date: str,
#             end_date: str,
#             unconventional_existing_data: List[Dict],
#             unconventional_future_data: List[Dict],
#             continuous_conventional_data: List[Dict],
#             eia_data: List[Dict],
#             completions_history: List[Dict],
#             completions_forecast: List[Dict],
#             rig_count_data: List[Dict],
#             drilled_wells_data: List[Dict],
#             available_type_curves
#     ) -> tuple:
#         if not ctx.triggered_id:
#             raise PreventUpdate
#         elif ctx.triggered_id == f'{prefix}create-save-btn':
#             if not all([selected_plays, vintages_to_generate, selected_parameter_data]):
#                 raise PreventUpdate
#         else:
#             raise PreventUpdate
#
#         unconventional_existing = unpack_data(unconventional_existing_data)
#         unconventional_future = unpack_data(unconventional_future_data)
#         continuous_conventional = unpack_data(continuous_conventional_data)
#         eia_production = unpack_data(eia_data)
#         rig_count_data = unpack_data(rig_count_data)
#         drilled_wells_data = unpack_data(drilled_wells_data)
#         completions_history = unpack_data(completions_history)
#         completions_forecast = unpack_data(completions_forecast)
#         available_type_curves = unpack_data(available_type_curves)
#
#         new_type_curves = []
#         vintages_by_play = {}
#         for row in selected_parameter_data:
#             ea_play = row[ModelMetadata.EA_PLAY]
#             vintage = row[ModelMetadata.VINTAGE]
#
#             if ea_play not in vintages_by_play:
#                 vintages_by_play[ea_play] = []
#
#             if vintage not in vintages_by_play[ea_play]:
#                 vintages_by_play[ea_play].append(vintage)
#
#             type_curve = TypeCurve.from_characteristics(
#                 vintage=row[ModelMetadata.VINTAGE],
#                 energy_product=row[ModelMetadata.ENERGY_PRODUCT],
#                 ea_play=row[ModelMetadata.EA_PLAY],
#                 qi=float(row[TypeCurveMetadata.QI]),
#                 b=float(row[TypeCurveMetadata.B]),
#                 di=float(row[TypeCurveMetadata.DI]),
#                 lateral_length=TypeCurve.safe_convert_to_int(row[TypeCurveMetadata.LATERAL_LENGTH]),
#                 first_completion_stages=TypeCurve.safe_convert_to_int(row[TypeCurveMetadata.FIRST_COMPLETION_STAGES]),
#                 first_completion_fluid_volume=TypeCurve.safe_convert_to_int(
#                     row[TypeCurveMetadata.FIRST_COMPLETION_FLUID_VOLUME]),
#                 first_completion_proppant_mass=TypeCurve.safe_convert_to_int(
#                     row[TypeCurveMetadata.FIRST_COMPLETION_PROPPANT_MASS]),
#             )
#             new_type_curves.append(type_curve)
#
#         vintages_required_in_forecasting_period = get_vintages_in_forecasting_period(completions_forecast)
#         missing_type_curves = pd.DataFrame()
#         for play, vintages in vintages_by_play.items():
#             missing_vintages = [v for v in vintages_required_in_forecasting_period if v not in vintages]
#             missing_type_curves_play = available_type_curves[(available_type_curves[ModelMetadata.EA_PLAY]==play) & (available_type_curves[ModelMetadata.VINTAGE].isin(missing_vintages))]
#             missing_type_curves = pd.concat([missing_type_curves, missing_type_curves_play])
#
#         missing_type_curves_collection = TypeCurveCollection.from_pipeline_data(missing_type_curves)
#         all_required_type_curves = new_type_curves + missing_type_curves_collection.type_curves
#
#         all_required_type_curves_collection = TypeCurveCollection(all_required_type_curves)
#
#         pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             basins_filter=get_basins_filter(basin),
#             energy_product_filter=[energy_product]
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=unconventional_existing,
#             unconventional_future_df=unconventional_future,
#             continuous_conventional_df=continuous_conventional,
#             eia_df=eia_production,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         production_visual.recalculate_future_wells_production(
#             type_curves=all_required_type_curves_collection.make_pipeline_entry(),
#             completions_history=completions_history,
#             completions_forecasts=completions_forecast,
#             plays_to_recalculate=selected_plays
#         )
#
#         prod_fig, prod_columns, prod_data, prod_total_columns, prod_total_data = production_visual.process_and_visualise_data()
#         new_unconventional_future = production_visual.get_storage_format_future_wells_prod()
#         packed_unconventional_future = pack_data(new_unconventional_future)
#
#         override_type_curves_collection = TypeCurveCollection(new_type_curves)
#
#         basins_filter = get_basins_filter(basin)
#         pipeline = GlobalPipeline.build_pipeline_from_parameters(
#             scenario_type=scenario_type,
#             basins_filter=basins_filter,
#             energy_product_filter=[energy_product],
#             start_date=start_date,
#             end_date=end_date,
#             override_type_curves=override_type_curves_collection.make_pipeline_entry()
#         )
#
#         previous_completions_forecast = pipeline.completions_forecasts
#
#         if basin != UsBasins.REST_OF_L48_METAVALUE:
#             rig_count_forecast_price_sensitive = melt_and_add_fields_rig_price_sensitive(rig_count_data, basin)
#             pipeline._rig_count_forecasts_price_sensitive = rig_count_forecast_price_sensitive
#         else:
#             rig_count_forecast_baseline = melt_and_add_fields_rigs_baseline(rig_count_data)
#             pipeline._rig_count_forecasts = rig_count_forecast_baseline
#
#         pipeline._drilled_wells_forecasts = melt_and_add_fields(drilled_wells_data, basin)
#         pipeline._completions_forecasts = melt_and_add_fields(completions_forecast, basin)
#
#         new_unconventional_future = add_padd(new_unconventional_future)
#         pipeline._future_wells_unconventional_production = new_unconventional_future
#
#         space_to_data = {
#             Spaces.RIG_COUNT_FORECAST: pipeline._rig_count_forecasts,
#             Spaces.RIG_COUNT_FORECAST_PRICE_SENSITIVE: pipeline._rig_count_forecasts_price_sensitive,
#             Spaces.DRILLED_WELLS_FORECAST: pipeline._drilled_wells_forecasts,
#             Spaces.COMPLETIONS_FORECAST: pipeline._completions_forecasts,
#             Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION: pipeline._future_wells_unconventional_production,
#             Spaces.OVERRIDE_TYPE_CURVES: pipeline._override_type_curves
#         }
#
#         for space in [Spaces.RIG_COUNT_FORECAST, Spaces.RIG_COUNT_FORECAST_PRICE_SENSITIVE, Spaces.DRILLED_WELLS_FORECAST, Spaces.COMPLETIONS_FORECAST,
#                       Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION, Spaces.OVERRIDE_TYPE_CURVES]:
#             data = space_to_data.get(space)
#             if data is not None and not data.empty:
#                 pipeline.save(space=space, scenario=Scenario.ea_library())
#
#         new_available_type_curves = create_new_available_type_curves_from_selected_table_data(selected_parameter_data, available_type_curves)
#
#         type_curve_fig = TypeCurveTile.EMPTY_FIGURE
#
#         new_available_type_curves = pack_data(new_available_type_curves)
#         parameter_data = []
#         selected_parameter_data = []
#         type_curve_loader_children = []
#         unsaved_applied_changes = False
#
#         """
#         Production for both energy product is affected by changes to completions, so we need to recalculate the production for the non active energy product.
#         """
#         pipeline_other_energy_product = GlobalPipeline.build_pipeline_from_parameters(
#             basins_filter=basins_filter,
#             scenario_type=scenario_type,
#             energy_product_filter=[get_other_energy_product(energy_product)],
#             completions_forecasts=pipeline._completions_forecasts
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=pipeline_other_energy_product.existing_wells_unconventional_production,
#             unconventional_future_df=pipeline_other_energy_product.future_wells_unconventional_production,
#             continuous_conventional_df=pipeline_other_energy_product.conventional_continuous,
#             eia_df=None,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         modified_plays = production_visual.get_modified_plays_completions(
#             previous_df=previous_completions_forecast.pivot(columns=ModelMetadata.EA_PLAY, values=ModelMetadata.VAL),
#             new_df=completions_forecast
#         )
#
#         if modified_plays != []:
#             model_sequence_config_from_production = {
#                 Models.RIG_COUNT_PRICE_SENSITIVE: False,
#                 Models.DRILLED_WELLS: False,
#                 Models.COMPLETIONS: False,
#                 Models.CONVENTIONAL_PRODUCTION: False,
#                 Models.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION: False,
#                 Models.TYPE_CURVES_CALIBRATOR: False,
#                 Models.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION: True,
#             }
#
#             pipeline_other_energy_product = run_chain_model(pipeline_other_energy_product, model_sequence_config=model_sequence_config_from_production)
#             pipeline_other_energy_product = filter_by_basins_filter(pipeline_other_energy_product, basins_filter)
#
#             pipeline_other_energy_product.save(space=Spaces.CONVENTIONAL_PRODUCTION_FORECAST, scenario=Scenario.ea_library())
#             pipeline_other_energy_product.save(space=Spaces.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION,
#                                                scenario=Scenario.ea_library())
#             pipeline_other_energy_product.save(space=Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION, scenario=Scenario.ea_library())
#
#
#         return (
#             parameter_data, selected_parameter_data, type_curve_fig, type_curve_loader_children,
#             packed_unconventional_future, prod_columns, prod_data, prod_total_columns, prod_total_data, prod_fig, new_available_type_curves,
#             unsaved_applied_changes
#         )
#
#     @callback(
#         Output(f'{prefix}create-new-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}create-new-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}type-curve-save-loader', 'children', allow_duplicate=True),
#         Output(f'{prefix}unsaved-applied-changes-bool', 'data', allow_duplicate=True),
#
#         Input(f'{prefix}create-new-apply-btn', 'n_clicks'),
#
#         State(f'{prefix}create-new-play-dropdown', 'value'),
#         State(f'{prefix}create-new-vintage-to-generate-dropdown', 'value'),
#         State(f'{prefix}create-new-parameter-table', 'data'),
#         State(f'{prefix}create-new-selected-parameter-table', 'data'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#         State(f'{prefix}completions-history', 'data'),
#         State(f'{prefix}completions-table', 'data'),
#         State(f'{prefix}start-date-ddown', 'value'),
#         State(f'{prefix}end-date-ddown', 'value'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}available-type-curves', 'data'),
#
#         prevent_initial_call=True
#     )
#     def create_new_tab_type_curve_apply(
#             apply_clicks,
#             selected_plays: List[str],
#             vintages_to_generate: List[int],
#             standard_parameter_data: List[Dict],
#             selected_parameter_data: List[Dict],
#             basin: UsBasins,
#             unconventional_existing_data: List[Dict],
#             unconventional_future_data: List[Dict],
#             continuous_conventional_data: List[Dict],
#             eia_data: List[Dict],
#             completions_history: List[Dict],
#             completions_forecast: List[Dict],
#             start_date,
#             end_date,
#             energy_product,
#             available_type_curves
#     ) -> tuple:
#         if not ctx.triggered_id:
#             raise PreventUpdate
#
#         if not all([selected_plays, vintages_to_generate, selected_parameter_data]):
#             raise PreventUpdate
#
#         unconventional_existing = unpack_data(unconventional_existing_data)
#         unconventional_future = unpack_data(unconventional_future_data)
#         continuous_conventional = unpack_data(continuous_conventional_data)
#         eia_production = unpack_data(eia_data)
#         completions_history = unpack_data(completions_history)
#         completions_forecast = unpack_data(completions_forecast)
#         available_type_curves = unpack_data(available_type_curves)
#
#         apply_loader_children = []
#
#         new_type_curves = []
#         vintages_by_play = {}
#         for row in selected_parameter_data:
#             ea_play = row[ModelMetadata.EA_PLAY]
#             vintage = row[ModelMetadata.VINTAGE]
#
#             if ea_play not in vintages_by_play:
#                 vintages_by_play[ea_play] = []
#
#             if vintage not in vintages_by_play[ea_play]:
#                 vintages_by_play[ea_play].append(vintage)
#
#             type_curve = TypeCurve.from_characteristics(
#                 vintage=row[ModelMetadata.VINTAGE],
#                 energy_product=row[ModelMetadata.ENERGY_PRODUCT],
#                 ea_play=row[ModelMetadata.EA_PLAY],
#                 qi=float(row[TypeCurveMetadata.QI]),
#                 b=float(row[TypeCurveMetadata.B]),
#                 di=float(row[TypeCurveMetadata.DI]),
#                 lateral_length=TypeCurve.safe_convert_to_int(row[TypeCurveMetadata.LATERAL_LENGTH]),
#                 first_completion_stages=TypeCurve.safe_convert_to_int(row[TypeCurveMetadata.FIRST_COMPLETION_STAGES]),
#                 first_completion_fluid_volume=TypeCurve.safe_convert_to_int(
#                     row[TypeCurveMetadata.FIRST_COMPLETION_FLUID_VOLUME]),
#                 first_completion_proppant_mass=TypeCurve.safe_convert_to_int(
#                     row[TypeCurveMetadata.FIRST_COMPLETION_PROPPANT_MASS]),
#             )
#             new_type_curves.append(type_curve)
#
#         vintages_required_in_forecasting_period = get_vintages_in_forecasting_period(completions_forecast)
#         missing_type_curves = pd.DataFrame()
#         for play, vintages in vintages_by_play.items():
#             missing_vintages = [v for v in vintages_required_in_forecasting_period if v not in vintages]
#             missing_type_curves_play = available_type_curves[(available_type_curves[ModelMetadata.EA_PLAY]==play) & (available_type_curves[ModelMetadata.VINTAGE].isin(missing_vintages))]
#             missing_type_curves = pd.concat([missing_type_curves, missing_type_curves_play])
#
#         missing_type_curves_collection = TypeCurveCollection.from_pipeline_data(missing_type_curves)
#         all_required_type_curves = new_type_curves + missing_type_curves_collection.type_curves
#
#
#         collection = TypeCurveCollection(all_required_type_curves)
#
#         pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             basins_filter=get_basins_filter(basin),
#             energy_product_filter=[energy_product]
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=unconventional_existing,
#             unconventional_future_df=unconventional_future,
#             continuous_conventional_df=continuous_conventional,
#             eia_df=eia_production,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         production_visual.recalculate_future_wells_production(
#             type_curves=collection.make_pipeline_entry(),
#             completions_history=completions_history,
#             completions_forecasts=completions_forecast,
#             plays_to_recalculate=selected_plays
#         )
#
#         prod_fig, prod_columns, prod_data, prod_total_columns, prod_total_data = production_visual.process_and_visualise_data()
#         new_unconventional_future = production_visual.get_storage_format_future_wells_prod()
#         packed_unconventional_future = pack_data(new_unconventional_future)
#
#         new_parameter_data = update_table_data_from_selected_table_data(selected_parameter_data,
#                                                                         standard_parameter_data)
#         type_curve_fig = populate_graph(new_parameter_data)
#
#         unsaved_applied_changes = True
#
#         return (
#             new_parameter_data,
#             type_curve_fig,
#             packed_unconventional_future,
#             prod_columns,
#             prod_data, prod_total_columns, prod_total_data,
#             prod_fig,
#             apply_loader_children,
#             unsaved_applied_changes
#         )
#
#     @callback(
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}type-curve-edit-loader', 'children', allow_duplicate=True),
#         Output(f'{prefix}unsaved-applied-changes-bool', 'data', allow_duplicate=True),
#
#         Input(f'{prefix}edit-apply-btn', 'n_clicks'),
#
#         State(f'{prefix}edit-play-dropdown', 'value'),
#         State(f'{prefix}edit-vintage-dropdown', 'value'),
#         State(f'{prefix}edit-selected-parameter-table', 'data'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#         State(f'{prefix}completions-history', 'data'),
#         State(f'{prefix}completions-table', 'data'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}available-type-curves', 'data'),
#
#         prevent_initial_call=True
#     )
#     def edit_tab_type_curve_apply(
#             apply_clicks,
#             selected_plays: List[str],
#             selected_vintages: List[int],
#             selected_parameter_data: List[Dict],
#             basin: UsBasins,
#             unconventional_existing_data: List[Dict],
#             unconventional_future_data: List[Dict],
#             continuous_conventional_data: List[Dict],
#             eia_data: List[Dict],
#             completions_history: List[Dict],
#             completions_forecast: List[Dict],
#             energy_product,
#             available_type_curves
#     ) -> tuple:
#         if not ctx.triggered_id:
#             raise PreventUpdate
#         elif ctx.triggered_id == f'{prefix}edit-apply-btn':
#             if not all([selected_plays, selected_vintages, selected_parameter_data]):
#                 raise PreventUpdate
#         else:
#             raise PreventUpdate
#
#         unconventional_existing = unpack_data(unconventional_existing_data)
#         unconventional_future = unpack_data(unconventional_future_data)
#         continuous_conventional = unpack_data(continuous_conventional_data)
#         eia_production = unpack_data(eia_data)
#         completions_history = unpack_data(completions_history)
#         completions_forecast = unpack_data(completions_forecast)
#         available_type_curves = unpack_data(available_type_curves)
#
#         new_type_curves = []
#         vintages_by_play = {}
#         for row in selected_parameter_data:
#             ea_play = row[ModelMetadata.EA_PLAY]
#             vintage = row[ModelMetadata.VINTAGE]
#
#             if ea_play not in vintages_by_play:
#                 vintages_by_play[ea_play] = []
#
#             if vintage not in vintages_by_play[ea_play]:
#                 vintages_by_play[ea_play].append(vintage)
#
#             type_curve = TypeCurve.from_characteristics(
#                 vintage=row[ModelMetadata.VINTAGE],
#                 energy_product=row[ModelMetadata.ENERGY_PRODUCT],
#                 ea_play=row[ModelMetadata.EA_PLAY],
#                 qi=float(row[TypeCurveMetadata.QI]),
#                 b=float(row[TypeCurveMetadata.B]),
#                 di=float(row[TypeCurveMetadata.DI]),
#                 lateral_length=TypeCurve.safe_convert_to_int(row[TypeCurveMetadata.LATERAL_LENGTH]),
#                 first_completion_stages=TypeCurve.safe_convert_to_int(row[TypeCurveMetadata.FIRST_COMPLETION_STAGES]),
#                 first_completion_fluid_volume=TypeCurve.safe_convert_to_int(
#                     row[TypeCurveMetadata.FIRST_COMPLETION_FLUID_VOLUME]),
#                 first_completion_proppant_mass=TypeCurve.safe_convert_to_int(
#                     row[TypeCurveMetadata.FIRST_COMPLETION_PROPPANT_MASS]),
#             )
#             new_type_curves.append(type_curve)
#
#
#         vintages_required_in_forecasting_period = get_vintages_in_forecasting_period(completions_forecast)
#         missing_type_curves = pd.DataFrame()
#         for play, vintages in vintages_by_play.items():
#             missing_vintages = [v for v in vintages_required_in_forecasting_period if v not in vintages]
#             missing_type_curves_play = available_type_curves[(available_type_curves[ModelMetadata.EA_PLAY]==play) & (available_type_curves[ModelMetadata.VINTAGE].isin(missing_vintages))]
#             missing_type_curves = pd.concat([missing_type_curves, missing_type_curves_play])
#
#         missing_type_curves_collection = TypeCurveCollection.from_pipeline_data(missing_type_curves)
#         all_required_type_curves = new_type_curves + missing_type_curves_collection.type_curves
#
#         collection = TypeCurveCollection(all_required_type_curves)
#
#         pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             basins_filter=get_basins_filter(basin),
#             energy_product_filter=[energy_product]
#         )
#
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=unconventional_existing,
#             unconventional_future_df=unconventional_future,
#             continuous_conventional_df=continuous_conventional,
#             eia_df=eia_production,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         production_visual.recalculate_future_wells_production(
#             type_curves=collection.make_pipeline_entry(),
#             completions_history=completions_history,
#             completions_forecasts=completions_forecast,
#             plays_to_recalculate=selected_plays
#         )
#
#         prod_fig, prod_columns, prod_data, prod_total_columns, prod_total_data = production_visual.process_and_visualise_data()
#         new_unconventional_future = production_visual.get_storage_format_future_wells_prod()
#         packed_unconventional_future = pack_data(new_unconventional_future)
#
#         type_curve_loader_children = []
#
#         unsaved_applied_changes = True
#
#         return (
#             packed_unconventional_future,
#             prod_columns, prod_data, prod_total_columns, prod_total_data, prod_fig,
#             type_curve_loader_children,
#             unsaved_applied_changes
#         )
#
#
#     @callback(
#         Output(f'{prefix}edit-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}edit-selected-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}edit-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}type-curve-save-loader', 'children', allow_duplicate=True),
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}available-type-curves', 'data', allow_duplicate=True),
#         Output(f'{prefix}unsaved-applied-changes-bool', 'data', allow_duplicate=True),
#
#         Input(f'{prefix}edit-save-btn', 'n_clicks'),
#
#         State(f'{prefix}edit-play-dropdown', 'value'),
#         State(f'{prefix}edit-vintage-dropdown', 'value'),
#         State(f'{prefix}edit-parameter-table', 'data'),
#         State(f'{prefix}edit-selected-parameter-table', 'data'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         State(f'{prefix}start-date-ddown', 'value'),
#         State(f'{prefix}end-date-ddown', 'value'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#         State(f'{prefix}completions-history', 'data'),
#         State(f'{prefix}completions-table', 'data'),
#         State(f'{prefix}rig-count-table', 'data'),
#         State(f'{prefix}drilled-wells-table', 'data'),
#         State(f'{prefix}available-type-curves', 'data'),
#         prevent_initial_call=True
#     )
#     def edit_type_curve_save(
#             edit_clicks,
#             selected_plays: List[str],
#             selected_vintages: List[int],
#             standard_parameter_data: List[Dict],
#             selected_parameter_data: List[Dict],
#             energy_product: EnergyProduct,
#             basin: UsBasins,
#             scenario_type: ScenarioTypes,
#             start_date: str,
#             end_date: str,
#             unconventional_existing_data: List[Dict],
#             unconventional_future_data: List[Dict],
#             continuous_conventional_data: List[Dict],
#             eia_data: List[Dict],
#             completions_history: List[Dict],
#             completions_forecast: List[Dict],
#             rig_count_data: List[Dict],
#             drilled_wells_data: List[Dict],
#             available_type_curves
#     ) -> tuple:
#         if not ctx.triggered_id:
#             raise PreventUpdate
#         elif ctx.triggered_id == f'{prefix}edit-save-btn':
#             if not all([selected_plays, selected_vintages, selected_parameter_data]):
#                 raise PreventUpdate
#         else:
#             raise PreventUpdate
#
#         unconventional_existing = unpack_data(unconventional_existing_data)
#         unconventional_future = unpack_data(unconventional_future_data)
#         continuous_conventional = unpack_data(continuous_conventional_data)
#         eia_production = unpack_data(eia_data)
#         rig_count_data = unpack_data(rig_count_data)
#         drilled_wells_data = unpack_data(drilled_wells_data)
#         completions_history = unpack_data(completions_history)
#         completions_forecast = unpack_data(completions_forecast)
#         available_type_curves = unpack_data(available_type_curves)
#
#         new_type_curves = []
#         vintages_by_play = {}
#         for row in selected_parameter_data:
#             ea_play = row[ModelMetadata.EA_PLAY]
#             vintage = row[ModelMetadata.VINTAGE]
#
#             if ea_play not in vintages_by_play:
#                 vintages_by_play[ea_play] = []
#
#             if vintage not in vintages_by_play[ea_play]:
#                 vintages_by_play[ea_play].append(vintage)
#
#             type_curve = TypeCurve.from_characteristics(
#                 vintage=row[ModelMetadata.VINTAGE],
#                 energy_product=row[ModelMetadata.ENERGY_PRODUCT],
#                 ea_play=row[ModelMetadata.EA_PLAY],
#                 qi=float(row[TypeCurveMetadata.QI]),
#                 b=float(row[TypeCurveMetadata.B]),
#                 di=float(row[TypeCurveMetadata.DI]),
#                 lateral_length=TypeCurve.safe_convert_to_int(row[TypeCurveMetadata.LATERAL_LENGTH]),
#                 first_completion_stages=TypeCurve.safe_convert_to_int(row[TypeCurveMetadata.FIRST_COMPLETION_STAGES]),
#                 first_completion_fluid_volume=TypeCurve.safe_convert_to_int(
#                     row[TypeCurveMetadata.FIRST_COMPLETION_FLUID_VOLUME]),
#                 first_completion_proppant_mass=TypeCurve.safe_convert_to_int(
#                     row[TypeCurveMetadata.FIRST_COMPLETION_PROPPANT_MASS]),
#             )
#             new_type_curves.append(type_curve)
#
#
#         vintages_required_in_forecasting_period = get_vintages_in_forecasting_period(completions_forecast)
#         missing_type_curves = pd.DataFrame()
#         for play, vintages in vintages_by_play.items():
#             missing_vintages = [v for v in vintages_required_in_forecasting_period if v not in vintages]
#             missing_type_curves_play = available_type_curves[(available_type_curves[ModelMetadata.EA_PLAY]==play) & (available_type_curves[ModelMetadata.VINTAGE].isin(missing_vintages))]
#             missing_type_curves = pd.concat([missing_type_curves, missing_type_curves_play])
#
#         missing_type_curves_collection = TypeCurveCollection.from_pipeline_data(missing_type_curves)
#         all_required_type_curves = new_type_curves + missing_type_curves_collection.type_curves
#
#         all_required_type_curves_collection = TypeCurveCollection(all_required_type_curves)
#
#         pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             basins_filter=get_basins_filter(basin),
#             energy_product_filter=[energy_product]
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=unconventional_existing,
#             unconventional_future_df=unconventional_future,
#             continuous_conventional_df=continuous_conventional,
#             eia_df=eia_production,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         production_visual.recalculate_future_wells_production(
#             type_curves=all_required_type_curves_collection.make_pipeline_entry(),
#             completions_history=completions_history,
#             completions_forecasts=completions_forecast,
#             plays_to_recalculate=selected_plays
#         )
#
#         prod_fig, prod_columns, prod_data,prod_total_columns, prod_total_data = production_visual.process_and_visualise_data()
#         new_unconventional_future = production_visual.get_storage_format_future_wells_prod()
#         packed_unconventional_future = pack_data(new_unconventional_future)
#
#         override_type_curves_collection = TypeCurveCollection(new_type_curves)
#
#         basins_filter = get_basins_filter(basin)
#         pipeline = GlobalPipeline.build_pipeline_from_parameters(
#             scenario_type=scenario_type,
#             basins_filter=basins_filter,
#             energy_product_filter=[energy_product],
#             start_date=start_date,
#             end_date=end_date,
#             override_type_curves=override_type_curves_collection.make_pipeline_entry()
#         )
#
#         previous_completions_forecast = pipeline.completions_forecasts
#
#         if basin != UsBasins.REST_OF_L48_METAVALUE:
#             rig_count_forecast_price_sensitive = melt_and_add_fields_rig_price_sensitive(rig_count_data, basin)
#             pipeline._rig_count_forecasts_price_sensitive = rig_count_forecast_price_sensitive
#         else:
#             rig_count_forecast_baseline = melt_and_add_fields_rigs_baseline(rig_count_data)
#             pipeline._rig_count_forecasts = rig_count_forecast_baseline
#         pipeline._drilled_wells_forecasts = melt_and_add_fields(drilled_wells_data, basin)
#         pipeline._completions_forecasts = melt_and_add_fields(completions_forecast, basin)
#
#         new_unconventional_future = add_padd(new_unconventional_future)
#         pipeline._future_wells_unconventional_production = new_unconventional_future
#
#         space_to_data = {
#             Spaces.RIG_COUNT_FORECAST: pipeline._rig_count_forecasts,
#             Spaces.RIG_COUNT_FORECAST_PRICE_SENSITIVE: pipeline._rig_count_forecasts_price_sensitive,
#             Spaces.DRILLED_WELLS_FORECAST: pipeline._drilled_wells_forecasts,
#             Spaces.COMPLETIONS_FORECAST: pipeline._completions_forecasts,
#             Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION: pipeline._future_wells_unconventional_production,
#             Spaces.OVERRIDE_TYPE_CURVES: pipeline._override_type_curves
#         }
#
#         for space in [Spaces.RIG_COUNT_FORECAST, Spaces.RIG_COUNT_FORECAST_PRICE_SENSITIVE, Spaces.DRILLED_WELLS_FORECAST, Spaces.COMPLETIONS_FORECAST,
#                       Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION, Spaces.OVERRIDE_TYPE_CURVES]:
#             data = space_to_data.get(space)
#             if data is not None and not data.empty:
#                 pipeline.save(space=space, scenario=Scenario.ea_library())
#
#         new_parameter_data = update_table_data_from_selected_table_data(selected_parameter_data, standard_parameter_data)
#         new_available_type_curves = update_available_type_curves_from_table_data(new_parameter_data, available_type_curves)
#         type_curve_fig = populate_graph(new_parameter_data)
#
#         new_available_type_curves = pack_data(new_available_type_curves)
#         selected_parameter_data = []
#         type_curve_loader_children = []
#         unsaved_applied_changes = False
#
#         """
#         Production for both energy product is affected by changes to completions, so we need to recalculate the production for the non active energy product.
#         """
#         pipeline_other_energy_product = GlobalPipeline.build_pipeline_from_parameters(
#             basins_filter=basins_filter,
#             scenario_type=scenario_type,
#             energy_product_filter=[get_other_energy_product(energy_product)],
#             completions_forecasts=pipeline._completions_forecasts
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=pipeline_other_energy_product.existing_wells_unconventional_production,
#             unconventional_future_df=pipeline_other_energy_product.future_wells_unconventional_production,
#             continuous_conventional_df=pipeline_other_energy_product.conventional_continuous,
#             eia_df=None,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         modified_plays = production_visual.get_modified_plays_completions(
#             previous_df=previous_completions_forecast.pivot(columns=ModelMetadata.EA_PLAY, values=ModelMetadata.VAL),
#             new_df=completions_forecast
#         )
#
#         if modified_plays != []:
#             model_sequence_config_from_production = {
#                 Models.RIG_COUNT_PRICE_SENSITIVE: False,
#                 Models.DRILLED_WELLS: False,
#                 Models.COMPLETIONS: False,
#                 Models.CONVENTIONAL_PRODUCTION: False,
#                 Models.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION: False,
#                 Models.TYPE_CURVES_CALIBRATOR: False,
#                 Models.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION: True,
#             }
#
#             pipeline_other_energy_product = run_chain_model(pipeline_other_energy_product, model_sequence_config=model_sequence_config_from_production)
#             pipeline_other_energy_product = filter_by_basins_filter(pipeline_other_energy_product, basins_filter)
#
#             pipeline_other_energy_product.save(space=Spaces.CONVENTIONAL_PRODUCTION_FORECAST, scenario=Scenario.ea_library())
#             pipeline_other_energy_product.save(space=Spaces.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION,
#                                                scenario=Scenario.ea_library())
#             pipeline_other_energy_product.save(space=Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION, scenario=Scenario.ea_library())
#
#
#
#         return (
#             new_parameter_data, selected_parameter_data, type_curve_fig, type_curve_loader_children,
#             packed_unconventional_future, prod_columns, prod_data, prod_total_columns, prod_total_data, prod_fig, new_available_type_curves,
#             unsaved_applied_changes
#         )
#
#     @callback(
#         Output(f'{prefix}create-new-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}create-new-parameter-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}create-new-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}create-new-selected-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}create-new-parameter-table', 'selected_rows', allow_duplicate=True),
#         Output(f'{prefix}create-new-play-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}create-new-vintage-to-copy-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}create-new-vintage-to-generate-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}type-curve-cancel-loader', 'children', allow_duplicate=True),
#         Output(f'{prefix}unsaved-applied-changes-bool', 'data', allow_duplicate=True),
#
#         Input(f'{prefix}create-cancel-btn', 'n_clicks'),
#         Input(f'{prefix}type-curve-tabs', 'active_tab'),
#
#         State(f'{prefix}type-curve-mode', 'data'),
#         State(f'{prefix}create-new-parameter-table', 'data'),
#         State(f'{prefix}create-new-play-dropdown', 'value'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#         State(f'{prefix}completions-history', 'data'),
#         State(f'{prefix}completions-table', 'data'),
#         State(f'{prefix}unsaved-applied-changes-bool', 'data'),
#         prevent_initial_call=True
#     )
#     def create_new_type_curve_cancel(
#             cancel_clicks,
#             active_tab,
#             mode,
#             standard_parameter_data: List[Dict],
#             selected_plays: List[str],
#             basin: UsBasins,
#             unconventional_existing_data: List[Dict],
#             unconventional_future_data: List[Dict],
#             continuous_conventional_data: List[Dict],
#             eia_data: List[Dict],
#             completions_history: List[Dict],
#             completions_forecast: List[Dict],
#             unsaved_applied_changes
#     ):
#         triggered_id = ctx.triggered_id
#
#         if not unsaved_applied_changes:
#             raise PreventUpdate
#
#         if active_tab != "create-new" and mode != "create-new":
#             raise PreventUpdate
#
#         if triggered_id == f'{prefix}type-curve-tabs' and active_tab == "create-new":
#             raise PreventUpdate
#
#         table_data = []
#         columns = TypeCurveTile.make_parameter_table_value_column(editable=False)
#         fig = TypeCurveTile.EMPTY_FIGURE
#         selected_table_data = []
#         table_selected_rows = []
#         play_dropdown_value = None
#         vintage_to_copy_value = None
#         vintage_to_generate_value = None
#         packed_unconventional_future = unconventional_future_data
#         prod_columns = []
#         prod_data = []
#         prod_fig = {}
#         type_curve_loader_children = []
#
#         unconventional_existing = unpack_data(unconventional_existing_data)
#         unconventional_future = unpack_data(unconventional_future_data)
#         continuous_conventional = unpack_data(continuous_conventional_data)
#         eia_production = unpack_data(eia_data)
#         completions_history = unpack_data(completions_history)
#         completions_forecast = unpack_data(completions_forecast)
#
#         standard_type_curves = []
#         for row in standard_parameter_data:
#             if row[ModelMetadata.EA_PLAY] in selected_plays:
#                 type_curve = TypeCurve.from_characteristics(
#                     vintage=row[ModelMetadata.VINTAGE],
#                     energy_product=row[ModelMetadata.ENERGY_PRODUCT],
#                     ea_play=row[ModelMetadata.EA_PLAY],
#                     qi=float(row[TypeCurveMetadata.QI]),
#                     b=float(row[TypeCurveMetadata.B]),
#                     di=float(row[TypeCurveMetadata.DI]),
#                     lateral_length=TypeCurve.safe_convert_to_int(row[TypeCurveMetadata.LATERAL_LENGTH]),
#                     first_completion_stages=TypeCurve.safe_convert_to_int(
#                         row[TypeCurveMetadata.FIRST_COMPLETION_STAGES]),
#                     first_completion_fluid_volume=TypeCurve.safe_convert_to_int(
#                         row[TypeCurveMetadata.FIRST_COMPLETION_FLUID_VOLUME]),
#                     first_completion_proppant_mass=TypeCurve.safe_convert_to_int(
#                         row[TypeCurveMetadata.FIRST_COMPLETION_PROPPANT_MASS]),
#                 )
#                 standard_type_curves.append(type_curve)
#
#         collection = TypeCurveCollection(standard_type_curves)
#
#         pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             basins_filter=get_basins_filter(basin),
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=unconventional_existing,
#             unconventional_future_df=unconventional_future,
#             continuous_conventional_df=continuous_conventional,
#             eia_df=eia_production,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         production_visual.recalculate_future_wells_production(
#             type_curves=collection.make_pipeline_entry(),
#             completions_history=completions_history,
#             completions_forecasts=completions_forecast,
#             plays_to_recalculate=selected_plays
#         )
#
#         prod_fig, prod_columns, prod_data, prod_total_columns, prod_total_data = production_visual.process_and_visualise_data()
#         new_unconventional_future = production_visual.get_storage_format_future_wells_prod()
#         packed_unconventional_future = pack_data(new_unconventional_future)
#         unsaved_applied_changes = False
#
#         return (
#             table_data,
#             columns,
#             fig,
#             selected_table_data,
#             table_selected_rows,
#             play_dropdown_value,
#             vintage_to_copy_value,
#             vintage_to_generate_value,
#             packed_unconventional_future,
#             prod_columns,
#             prod_data, prod_total_columns, prod_total_data,
#             prod_fig,
#             type_curve_loader_children,
#             unsaved_applied_changes
#         )
#
#
#     @callback(
#         Output(f'{prefix}edit-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}edit-parameter-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}edit-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}edit-selected-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}edit-parameter-table', 'selected_rows', allow_duplicate=True),
#         Output(f'{prefix}edit-play-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}edit-vintage-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}type-curve-cancel-loader', 'children', allow_duplicate=True),
#         Output(f'{prefix}unsaved-applied-changes-bool', 'data', allow_duplicate=True),
#
#         Input(f'{prefix}edit-cancel-btn', 'n_clicks'),
#         Input(f'{prefix}type-curve-tabs', 'active_tab'),
#
#         State(f'{prefix}type-curve-mode', 'data'),
#         State(f'{prefix}edit-parameter-table', 'data'),
#         State(f'{prefix}edit-play-dropdown', 'value'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#         State(f'{prefix}completions-history', 'data'),
#         State(f'{prefix}completions-table', 'data'),
#         State(f'{prefix}unsaved-applied-changes-bool', 'data'),
#         prevent_initial_call=True
#     )
#     def edit_type_curve_cancel(
#             cancel_clicks,
#             active_tab,
#             mode,
#             standard_parameter_data: List[Dict],
#             selected_plays: List[str],
#             basin: UsBasins,
#             unconventional_existing_data: List[Dict],
#             unconventional_future_data: List[Dict],
#             continuous_conventional_data: List[Dict],
#             eia_data: List[Dict],
#             completions_history: List[Dict],
#             completions_forecast: List[Dict],
#             unsaved_applied_changes
#     ):
#         triggered_id = ctx.triggered_id
#
#         if not unsaved_applied_changes:
#             raise PreventUpdate
#
#         if standard_parameter_data is None or not standard_parameter_data:
#             raise PreventUpdate
#
#         if active_tab != "edit" and mode != "edit":
#             raise PreventUpdate
#
#         if triggered_id == f'{prefix}type-curve-tabs' and active_tab == "edit":
#             raise PreventUpdate
#
#         table_data = []
#         columns = TypeCurveTile.make_parameter_table_value_column(editable=False)
#         fig = TypeCurveTile.EMPTY_FIGURE
#         selected_table_data = []
#         table_selected_rows = []
#         play_dropdown_value = None
#         vintage_dropdown_value = None
#         packed_unconventional_future = unconventional_future_data
#         prod_columns = []
#         prod_data = []
#         prod_fig = {}
#         type_curve_loader_children = []
#
#         unconventional_existing = unpack_data(unconventional_existing_data)
#         unconventional_future = unpack_data(unconventional_future_data)
#         continuous_conventional = unpack_data(continuous_conventional_data)
#         eia_production = unpack_data(eia_data)
#         completions_history = unpack_data(completions_history)
#         completions_forecast = unpack_data(completions_forecast)
#
#         standard_type_curves = []
#         for row in standard_parameter_data:
#             if row[ModelMetadata.EA_PLAY] in selected_plays:
#                 type_curve = TypeCurve.from_characteristics(
#                     vintage=row[ModelMetadata.VINTAGE],
#                     energy_product=row[ModelMetadata.ENERGY_PRODUCT],
#                     ea_play=row[ModelMetadata.EA_PLAY],
#                     qi=float(row[TypeCurveMetadata.QI]),
#                     b=float(row[TypeCurveMetadata.B]),
#                     di=float(row[TypeCurveMetadata.DI]),
#                     lateral_length=TypeCurve.safe_convert_to_int(row[TypeCurveMetadata.LATERAL_LENGTH]),
#                     first_completion_stages=TypeCurve.safe_convert_to_int(
#                         row[TypeCurveMetadata.FIRST_COMPLETION_STAGES]),
#                     first_completion_fluid_volume=TypeCurve.safe_convert_to_int(
#                         row[TypeCurveMetadata.FIRST_COMPLETION_FLUID_VOLUME]),
#                     first_completion_proppant_mass=TypeCurve.safe_convert_to_int(
#                         row[TypeCurveMetadata.FIRST_COMPLETION_PROPPANT_MASS]),
#                 )
#                 standard_type_curves.append(type_curve)
#
#         collection = TypeCurveCollection(standard_type_curves)
#
#         pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             basins_filter=get_basins_filter(basin),
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=unconventional_existing,
#             unconventional_future_df=unconventional_future,
#             continuous_conventional_df=continuous_conventional,
#             eia_df=eia_production,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         production_visual.recalculate_future_wells_production(
#             type_curves=collection.make_pipeline_entry(),
#             completions_history=completions_history,
#             completions_forecasts=completions_forecast,
#             plays_to_recalculate=selected_plays
#         )
#
#         prod_fig, prod_columns, prod_data, prod_total_columns, prod_total_data = production_visual.process_and_visualise_data()
#         new_unconventional_future = production_visual.get_storage_format_future_wells_prod()
#         packed_unconventional_future = pack_data(new_unconventional_future)
#         unsaved_applied_changes = False
#
#         return (
#             table_data,
#             columns,
#             fig,
#             selected_table_data,
#             table_selected_rows,
#             play_dropdown_value,
#             vintage_dropdown_value,
#             packed_unconventional_future,
#             prod_columns,
#             prod_data,prod_total_columns, prod_total_data,
#             prod_fig,
#             type_curve_loader_children,
#             unsaved_applied_changes
#
#         )
#
#     @callback(
#         Output(f'{prefix}delete-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}delete-parameter-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}delete-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}delete-selected-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}delete-parameter-table', 'selected_rows', allow_duplicate=True),
#         Output(f'{prefix}delete-play-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}delete-vintage-dropdown', 'value', allow_duplicate=True),
#
#         Input(f'{prefix}delete-cancel-btn', 'n_clicks'),
#
#         State(f'{prefix}type-curve-mode', 'data'),
#         prevent_initial_call=True
#     )
#     def delete_type_curve_cancel(cancel_clicks, mode):
#         if cancel_clicks is None or mode != "delete":
#             raise PreventUpdate
#
#         table_data = []
#         columns = TypeCurveTile.make_parameter_table_value_column(editable=False)
#         fig = TypeCurveTile.EMPTY_FIGURE
#         selected_table_data = []
#         table_selected_rows = []
#         play_dropdown_value = None
#         vintage_dropdown_value = None
#
#         return (
#             table_data,
#             columns,
#             fig,
#             selected_table_data,
#             table_selected_rows,
#             play_dropdown_value,
#             vintage_dropdown_value
#         )
#
#     @callback(
#         Output(f'{prefix}download-data', 'data', allow_duplicate=True),
#         Input(f'{prefix}download-data-btn', 'n_clicks'),
#         State(f'{prefix}rig-count-table', 'data'),
#         State(f'{prefix}rig-count-history', 'data'),
#         State(f'{prefix}drilled-wells-table', 'data'),
#         State(f'{prefix}drilled-wells-history', 'data'),
#         State(f'{prefix}completions-table', 'data'),
#         State(f'{prefix}completions-history', 'data'),
#         State(f'{prefix}production-table', 'data'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         State(f'{prefix}unconventional-future', 'data'),
#         prevent_initial_call=True
#     )
#     def download_data(n_clicks, rig_count_data, rig_count_history, drilled_wells_data, drilled_wells_history, completions_data, completions_history, production_data, basin,
#                       energy_product, scenario_type, unconventional_future_data):
#         if n_clicks is None:
#             raise PreventUpdate
#
#         dfs = {}
#         if rig_count_data:
#             dfs[DataCategories.RIG_COUNT] = make_continuous_df_with_forecast_flag(
#                 history_df=unpack_data(rig_count_history),
#                 forecast_df=unpack_data(rig_count_data)
#             )
#         if drilled_wells_data:
#             dfs[DataCategories.DRILLED_WELLS] = make_continuous_df_with_forecast_flag(
#                 history_df=unpack_data(drilled_wells_history),
#                 forecast_df=unpack_data(drilled_wells_data)
#             )
#         if completions_data:
#             dfs[DataCategories.COMPLETIONS] = make_continuous_df_with_forecast_flag(
#                 history_df=unpack_data(completions_history),
#                 forecast_df=unpack_data(completions_data)
#             )
#         if production_data:
#             prod_df = unpack_data(production_data)
#             prod_df[Enums.IS_FORECAST] = False
#             prod_df.loc[prod_df.index >= unpack_data(unconventional_future_data).index.min(), Enums.IS_FORECAST] = True
#             dfs[DataCategories.PRODUCTION] = prod_df
#
#         if not dfs:
#             raise PreventUpdate
#
#
#
#         return download_excel(
#             dataframes=dfs,
#             filename_prefix='us_production_data',
#             identifiers={ModelMetadata.SCENARIO_TYPE: scenario_type, ModelMetadata.ENERGY_PRODUCT: energy_product, ModelMetadata.EIA_BASIN: basin}
#         )
#
#     @callback(
#         Output(f'{prefix}save-modal', 'is_open', allow_duplicate=True),
#         Output(f'{prefix}save-loader', 'children', allow_duplicate=True),
#         Input(f'{prefix}save-to-db-btn', 'n_clicks'),
#
#         State(f'{prefix}rig-count-table', 'data'),
#         State(f'{prefix}drilled-wells-table', 'data'),
#         State(f'{prefix}completions-table', 'data'),
#
#         State(f'{prefix}completions-history', 'data'),
#
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}unconventional-existing', 'data'),
#
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         prevent_initial_call=True
#     )
#     def save_to_database(n_clicks,
#                          rig_count_data, drilled_wells_data, completions_data, completions_history,
#                          unconventional_future_production, unconventional_existing_production,
#                          basin, energy_product, scenario_type):
#         if n_clicks is None:
#             raise PreventUpdate
#
#         basins_filter = get_basins_filter(basin)
#         pipeline = GlobalPipeline(
#             basins_filter=basins_filter,
#             scenario_type=scenario_type,
#             energy_product_filter=[energy_product],
#             end_date=TimeManagement.MAX_DATE
#         )
#
#         rig_count_data = unpack_data(rig_count_data)
#         drilled_wells_data = unpack_data(drilled_wells_data)
#         completions_data = unpack_data(completions_data)
#         unconventional_future_production = unpack_data(unconventional_future_production)
#         unconventional_future_production = add_padd(df=unconventional_future_production)
#
#
#         unconventional_existing_production = unpack_data(unconventional_existing_production)
#         pipeline = update_existing_wells_in_pipeline(pipeline=pipeline, unconventional_existing_production=unconventional_existing_production)
#
#         previous_completions_forecast = pipeline.completions_forecasts
#
#         if basin != UsBasins.REST_OF_L48_METAVALUE:
#             rig_count_forecast_price_sensitive = melt_and_add_fields_rig_price_sensitive(rig_count_data, basin)
#             pipeline._rig_count_forecasts_price_sensitive = rig_count_forecast_price_sensitive
#         else:
#             rig_count_forecast_baseline = melt_and_add_fields_rigs_baseline(rig_count_data)
#             pipeline._rig_count_forecasts = rig_count_forecast_baseline
#
#         drilled_wells_forecast = melt_and_add_fields(drilled_wells_data, basin)
#         completions_forecast = melt_and_add_fields(completions_data, basin)
#
#         pipeline._future_wells_unconventional_production = unconventional_future_production
#         pipeline._drilled_wells_forecasts = drilled_wells_forecast
#         pipeline._completions_forecasts = completions_forecast
#         pipeline._existing_wells_unconventional_production = unconventional_existing_production_full
#
#         space_to_data = {
#             Spaces.RIG_COUNT_FORECAST: pipeline._rig_count_forecasts,
#             Spaces.RIG_COUNT_FORECAST_PRICE_SENSITIVE: pipeline._rig_count_forecasts_price_sensitive,
#             Spaces.DRILLED_WELLS_FORECAST: pipeline._drilled_wells_forecasts,
#             Spaces.COMPLETIONS_FORECAST: pipeline._completions_forecasts,
#             Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION: pipeline._future_wells_unconventional_production,
#             Spaces.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION: pipeline._existing_wells_unconventional_production,
#         }
#
#         for space in [Spaces.RIG_COUNT_FORECAST, Spaces.RIG_COUNT_FORECAST_PRICE_SENSITIVE, Spaces.DRILLED_WELLS_FORECAST, Spaces.COMPLETIONS_FORECAST, Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION, Spaces.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION]:
#             data = space_to_data.get(space)
#             if data is not None and not data.empty:
#                 pipeline.save(space=space, scenario=Scenario.ea_library())
#
#         """
#         Production for both energy product is affected by changes to completions, so we need to recalculate the production for the non active energy product.
#         """
#         pipeline_other_energy_product = GlobalPipeline.build_pipeline_from_parameters(
#             basins_filter=basins_filter,
#             scenario_type=scenario_type,
#             energy_product_filter=[get_other_energy_product(energy_product)],
#             completions_forecasts=pipeline._completions_forecasts
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=pipeline_other_energy_product.existing_wells_unconventional_production,
#             unconventional_future_df=pipeline_other_energy_product.future_wells_unconventional_production,
#             continuous_conventional_df=pipeline_other_energy_product.conventional_continuous,
#             eia_df=None,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         modified_plays = production_visual.get_modified_plays_completions(
#             previous_df=previous_completions_forecast.pivot(columns=ModelMetadata.EA_PLAY, values=ModelMetadata.VAL),
#             new_df=completions_data
#         )
#
#         if modified_plays != []:
#             model_sequence_config_from_production = {
#                 Models.RIG_COUNT_PRICE_SENSITIVE: False,
#                 Models.DRILLED_WELLS: False,
#                 Models.COMPLETIONS: False,
#                 Models.CONVENTIONAL_PRODUCTION: False,
#                 Models.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION: False,
#                 Models.TYPE_CURVES_CALIBRATOR: False,
#                 Models.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION: True,
#             }
#
#             pipeline_other_energy_product = run_chain_model(pipeline_other_energy_product, model_sequence_config=model_sequence_config_from_production)
#             pipeline_other_energy_product = filter_by_basins_filter(pipeline_other_energy_product, basins_filter)
#
#             pipeline_other_energy_product.save(space=Spaces.CONVENTIONAL_PRODUCTION_FORECAST, scenario=Scenario.ea_library())
#             pipeline_other_energy_product.save(space=Spaces.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION,
#                                                scenario=Scenario.ea_library())
#             pipeline_other_energy_product.save(space=Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION, scenario=Scenario.ea_library())
#
#
#         saved_popup = True
#         loading_children = []
#
#         return saved_popup, loading_children
#
#
#     @callback(
#         Output(f'{prefix}type-curves-overrides', 'data', allow_duplicate=True),
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}available-type-curves', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}delete-play-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}delete-vintage-dropdown', 'value', allow_duplicate=True),
#         Output(f'{prefix}delete-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}delete-selected-parameter-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}delete-type-curve-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}type-curve-delete-loader', 'children'),
#
#         Input(f'{prefix}delete-confirm-btn', 'n_clicks'),
#
#         State(f'{prefix}delete-play-dropdown', 'value'),
#         State(f'{prefix}delete-vintage-dropdown', 'value'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         State(f'{prefix}start-date-ddown', 'value'),
#         State(f'{prefix}end-date-ddown', 'value'),
#         State(f'{prefix}available-type-curves', 'data'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#         State(f'{prefix}rig-count-table', 'data'),
#         State(f'{prefix}drilled-wells-table', 'data'),
#         State(f'{prefix}completions-history', 'data'),
#         State(f'{prefix}completions-table', 'data'),
#         State(f'{prefix}delete-selected-parameter-table', 'data'),
#         prevent_initial_call=True
#     )
#     def delete_type_curve_override(
#             delete_clicks,
#             selected_plays: List[str],
#             selected_vintages: List[int],
#             energy_product: EnergyProduct,
#             basin: UsBasins,
#             scenario_type: ScenarioTypes,
#             start_date: str,
#             end_date: str,
#             available_type_curves: List[Dict],
#             unconventional_existing_data: List[Dict],
#             unconventional_future_data: List[Dict],
#             continuous_conventional_data: List[Dict],
#             eia_data: List[Dict],
#             rig_count_forecast: List[Dict],
#             drilled_wells_forecast: List[Dict],
#             completions_history: List[Dict],
#             completions_forecast: List[Dict],
#             selected_parameter_table_data
#     ) -> tuple:
#         if delete_clicks is None or not all([selected_plays, selected_vintages]):
#             raise PreventUpdate
#
#         available_type_curves = unpack_data(available_type_curves)
#         rig_count_forecast = unpack_data(rig_count_forecast)
#         drilled_wells_forecast = unpack_data(drilled_wells_forecast)
#         completions_history = unpack_data(completions_history)
#         completions_forecast = unpack_data(completions_forecast)
#         novi_type_curves = available_type_curves[available_type_curves[TypeCurveMetadata.TYPE_CURVE_TYPE]==TypeCurveMetadata.NOVI]
#         novi_collection = TypeCurveCollection.from_pipeline_data(df=novi_type_curves)
#         existing_override_type_curves = available_type_curves[
#             available_type_curves[TypeCurveMetadata.TYPE_CURVE_TYPE] == TypeCurveMetadata.OVERRIDE]
#         existing_override_collection = TypeCurveCollection.from_pipeline_data(df=existing_override_type_curves)
#
#         basins_filter = get_basins_filter(basin)
#         pipeline = GlobalPipeline.build_pipeline_from_parameters(
#                     scenario_type=scenario_type,
#                     basins_filter=basins_filter,
#                     energy_product_filter=[energy_product],
#                     start_date=start_date,
#                     end_date=end_date,
#                     adjusted_type_curves =novi_collection.make_pipeline_entry(),
#                     override_type_curves=existing_override_collection.make_pipeline_entry()
#                 )
#         previous_completions_forecast = pipeline.completions_forecasts
#
#         type_curves_to_delete = []
#         for type_curve_characteristics in selected_parameter_table_data:
#             type_curve = TypeCurve.from_characteristics(
#                                             vintage=type_curve_characteristics[ModelMetadata.VINTAGE],
#                                             energy_product=energy_product,
#                                            ea_play=type_curve_characteristics[ModelMetadata.EA_PLAY],
#                                            qi=type_curve_characteristics[TypeCurveMetadata.QI],
#                                            di=type_curve_characteristics[TypeCurveMetadata.DI],
#                                            b=type_curve_characteristics[TypeCurveMetadata.B],
#                                             lateral_length=TypeCurve.safe_convert_to_int(type_curve_characteristics[TypeCurveMetadata.LATERAL_LENGTH]),
#                                             first_completion_stages=TypeCurve.safe_convert_to_int(type_curve_characteristics[TypeCurveMetadata.FIRST_COMPLETION_STAGES]),
#                                             first_completion_fluid_volume=TypeCurve.safe_convert_to_int(
#                                                 type_curve_characteristics[TypeCurveMetadata.FIRST_COMPLETION_FLUID_VOLUME]),
#                                             first_completion_proppant_mass=TypeCurve.safe_convert_to_int(
#                                                 type_curve_characteristics[TypeCurveMetadata.FIRST_COMPLETION_PROPPANT_MASS]),
#                                            )
#             type_curves_to_delete.append(type_curve)
#             mask = (
#                     (pipeline._override_type_curves[ModelMetadata.VINTAGE] == type_curve_characteristics[
#                         ModelMetadata.VINTAGE]) &
#                     (pipeline._override_type_curves[ModelMetadata.ENERGY_PRODUCT] == energy_product) &
#                     (pipeline._override_type_curves[ModelMetadata.EA_PLAY] == type_curve_characteristics[
#                         ModelMetadata.EA_PLAY])
#             )
#
#             pipeline._override_type_curves = pipeline._override_type_curves[~mask]
#
#             available_type_curves_mask = (
#                 (available_type_curves[ModelMetadata.VINTAGE] == type_curve_characteristics[ModelMetadata.VINTAGE]) &
#                 (available_type_curves[ModelMetadata.ENERGY_PRODUCT] == energy_product) &
#                 (available_type_curves[ModelMetadata.EA_PLAY] == type_curve_characteristics[ModelMetadata.EA_PLAY]) &
#                 (available_type_curves[TypeCurveMetadata.TYPE_CURVE_TYPE] == TypeCurveMetadata.OVERRIDE)
#             )
#
#             available_type_curves = available_type_curves[~available_type_curves_mask]
#
#
#         delete_collection = TypeCurveCollection(type_curves_to_delete)
#         delete_collection.delete_overrides(
#             scenario_type=scenario_type
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=unpack_data(unconventional_existing_data),
#             unconventional_future_df=unpack_data(unconventional_future_data),
#             continuous_conventional_df=unpack_data(continuous_conventional_data),
#             eia_df=unpack_data(eia_data),
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         production_visual.recalculate_future_wells_production(
#             type_curves=pipeline.prioritized_type_curves,
#             completions_history=completions_history,
#             completions_forecasts=completions_forecast,
#             plays_to_recalculate=selected_plays
#         )
#
#         prod_fig, prod_columns, prod_data, prod_total_columns, prod_total_data = production_visual.process_and_visualise_data()
#         new_unconventional_future = production_visual.get_storage_format_future_wells_prod()
#         new_unconventional_future = add_padd(new_unconventional_future)
#
#         if basin != UsBasins.REST_OF_L48_METAVALUE:
#             rig_count_forecast_price_sensitive = melt_and_add_fields_rig_price_sensitive(rig_count_forecast, basin)
#             pipeline._rig_count_forecasts_price_sensitive = rig_count_forecast_price_sensitive
#         else:
#             rig_count_forecast_baseline = melt_and_add_fields_rigs_baseline(rig_count_forecast)
#             pipeline._rig_count_forecasts = rig_count_forecast_baseline
#
#         pipeline._drilled_wells_forecasts = melt_and_add_fields(drilled_wells_forecast, basin)
#         pipeline._completions_forecasts = melt_and_add_fields(completions_forecast, basin)
#         pipeline._future_wells_unconventional_production = new_unconventional_future
#         space_to_data = {
#             Spaces.RIG_COUNT_FORECAST: pipeline._rig_count_forecasts,
#             Spaces.RIG_COUNT_FORECAST_PRICE_SENSITIVE: pipeline._rig_count_forecasts_price_sensitive,
#             Spaces.DRILLED_WELLS_FORECAST: pipeline._drilled_wells_forecasts,
#             Spaces.COMPLETIONS_FORECAST: pipeline._completions_forecasts,
#             Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION: pipeline._future_wells_unconventional_production,
#         }
#
#         for space in [Spaces.RIG_COUNT_FORECAST, Spaces.RIG_COUNT_FORECAST_PRICE_SENSITIVE,
#                       Spaces.DRILLED_WELLS_FORECAST, Spaces.COMPLETIONS_FORECAST,
#                       Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION]:
#             data = space_to_data.get(space)
#             if data is not None and not data.empty:
#                 pipeline.save(space=space, scenario=Scenario.ea_library())
#
#         packed_available_type_curves = pack_data(available_type_curves)
#         packed_unconventional_future = pack_data(new_unconventional_future)
#         packed_overrides = pack_data(pipeline.override_type_curves)
#
#         """
#         Production for both energy product is affected by changes to completions, so we need to recalculate the production for the non active energy product.
#         """
#         pipeline_other_energy_product = GlobalPipeline.build_pipeline_from_parameters(
#             basins_filter=basins_filter,
#             scenario_type=scenario_type,
#             energy_product_filter=[get_other_energy_product(energy_product)],
#             completions_forecasts=pipeline._completions_forecasts
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=pipeline_other_energy_product.existing_wells_unconventional_production,
#             unconventional_future_df=pipeline_other_energy_product.future_wells_unconventional_production,
#             continuous_conventional_df=pipeline_other_energy_product.conventional_continuous,
#             eia_df=None,
#             eia_basin=basin,
#             pipeline=pipeline
#         )
#
#         modified_plays = production_visual.get_modified_plays_completions(
#             previous_df=previous_completions_forecast.pivot(columns=ModelMetadata.EA_PLAY, values=ModelMetadata.VAL),
#             new_df=completions_forecast
#         )
#
#         if modified_plays != []:
#             model_sequence_config_from_production = {
#                 Models.RIG_COUNT_PRICE_SENSITIVE: False,
#                 Models.DRILLED_WELLS: False,
#                 Models.COMPLETIONS: False,
#                 Models.CONVENTIONAL_PRODUCTION: False,
#                 Models.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION: False,
#                 Models.TYPE_CURVES_CALIBRATOR: False,
#                 Models.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION: True,
#             }
#
#             pipeline_other_energy_product = run_chain_model(pipeline_other_energy_product, model_sequence_config=model_sequence_config_from_production)
#             pipeline_other_energy_product = filter_by_basins_filter(pipeline_other_energy_product, basins_filter)
#
#             pipeline_other_energy_product.save(space=Spaces.CONVENTIONAL_PRODUCTION_FORECAST, scenario=Scenario.ea_library())
#             pipeline_other_energy_product.save(space=Spaces.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION,
#                                                scenario=Scenario.ea_library())
#             pipeline_other_energy_product.save(space=Spaces.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION, scenario=Scenario.ea_library())
#
#
#
#         play_dropdown_value = None
#         vintage_dropdown_value = None
#         type_curve_figure = TypeCurveTile.EMPTY_FIGURE
#         parameter_table_data = []
#         selected_parameter_table_data = []
#         type_curve_loader_children = []
#
#         return (
#             packed_overrides,
#             packed_unconventional_future,
#             packed_available_type_curves,
#             prod_columns,
#             prod_data, prod_total_columns, prod_total_data,
#             prod_fig,
#             play_dropdown_value,
#             vintage_dropdown_value,
#             parameter_table_data,
#             selected_parameter_table_data,
#             type_curve_figure,
#             type_curve_loader_children
#         )
#
#     @callback(
#         Output(f'{prefix}save-to-db-btn', 'disabled'),
#         Output(f'{prefix}rig-count-upload', 'disabled'),
#         Output(f'{prefix}drilled-wells-upload', 'disabled'),
#         Output(f'{prefix}completions-upload', 'disabled'),
#         Output(f'{prefix}production-upload', 'disabled'),
#
#         Input(f'{prefix}unsaved-applied-changes-bool', 'data'),
#         Input(f'{prefix}rig-count-table', 'data'),
#         Input(f'{prefix}drilled-wells-table', 'data'),
#         Input(f'{prefix}completions-table', 'data'),
#         Input(f'{prefix}production-table', 'data'),
#
#         prevent_initial_call=True
#     )
#     def manage_button_state(unsaved_applied_changes, *_):
#         trigger = ctx.triggered_id
#         rig_count_upload_btn_disabled = False
#         drilled_wells_upload_btn_disabled = False
#         completions_upload_btn_disabled = False
#
#         if trigger == f'{prefix}unsaved-applied-changes' and unsaved_applied_changes:
#             save_btn_disabled = True
#             return save_btn_disabled, rig_count_upload_btn_disabled, drilled_wells_upload_btn_disabled, completions_upload_btn_disabled, completions_upload_btn_disabled
#
#         if trigger == f'{prefix}unsaved-applied-changes' and not unsaved_applied_changes:
#             save_btn_disabled = False
#             return save_btn_disabled, rig_count_upload_btn_disabled, drilled_wells_upload_btn_disabled, completions_upload_btn_disabled, completions_upload_btn_disabled
#
#         if unsaved_applied_changes:
#             save_btn_disabled = True
#             return save_btn_disabled, rig_count_upload_btn_disabled, drilled_wells_upload_btn_disabled, completions_upload_btn_disabled, completions_upload_btn_disabled
#
#         save_btn_disabled = False
#         return save_btn_disabled, rig_count_upload_btn_disabled, drilled_wells_upload_btn_disabled, completions_upload_btn_disabled, completions_upload_btn_disabled
#
#     graph_ids = [
#         'rig-count-graph',
#         'permits-graph',
#         'drilled-wells-graph',
#         'drilled-ratio-graph',
#         'completions-graph',
#         'completions-ratio-graph',
#         'ducs-graph',
#         'production-graph',
#         'create-new-type-curve-graph',
#         'edit-type-curve-graph',
#         'delete-type-curve-graph',
#         'frac-fleets-graph'
#     ]
#
#     for graph_id in graph_ids:
#         @callback(
#             Output(f'{prefix}{graph_id}-modal', 'is_open'),
#             Output(f'{prefix}{graph_id}-modal-graph', 'figure'),
#             Input(f'{prefix}{graph_id}-expand-btn', 'n_clicks'),
#             State(f'{prefix}{graph_id}', 'figure'),
#             State(f'{prefix}{graph_id}-modal', 'is_open'),
#             prevent_initial_call=True
#         )
#         def toggle_modal(n_clicks, figure, is_open):
#             if n_clicks is None:
#                 return no_update, no_update
#             return not is_open, figure
#
#         toggle_modal.__name__ = f'toggle_modal_{graph_id}'
#         globals()[toggle_modal.__name__] = toggle_modal
#
#     for graph_id in graph_ids:
#         @callback(
#             Output(f'{prefix}{graph_id}-modal', 'is_open', allow_duplicate=True),
#             Input(f'{prefix}{graph_id}-modal-close', 'n_clicks'),
#             prevent_initial_call=True
#         )
#         def close_modal(n_clicks):
#             if n_clicks is None:
#                 return no_update
#             return False
#
#         close_modal.__name__ = f'close_modal_{graph_id}'
#         globals()[close_modal.__name__] = close_modal
#
#     @callback(
#         Output(f'{prefix}rig-count-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}rig-count-table-previous', 'data', allow_duplicate=True),
#         Output(f'{prefix}rig-count-upload-error-text', 'children'),
#         Output(f'{prefix}rig-count-upload-error-modal', 'is_open'),
#         Input(f'{prefix}rig-count-upload', 'contents'),
#         State(f'{prefix}rig-count-upload', 'filename'),
#         State(f'{prefix}rig-count-table', 'data'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         prevent_initial_call=True
#     )
#     def update_rig_count_from_excel(contents, filename, current_data, basin):
#         if contents is None:
#             raise PreventUpdate
#
#         table_name = DataCategories.RIG_COUNT
#
#         return extract_excel_upload(contents, filename, current_data, table_name, basin)
#
#     @callback(
#         Output(f'{prefix}drilled-wells-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-table-previous', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-upload-error-text', 'children'),
#         Output(f'{prefix}drilled-wells-upload-error-modal', 'is_open'),
#         Input(f'{prefix}drilled-wells-upload', 'contents'),
#         State(f'{prefix}drilled-wells-upload', 'filename'),
#         State(f'{prefix}drilled-wells-table', 'data'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         prevent_initial_call=True
#     )
#     def update_drilled_wells_from_excel(contents, filename, current_data, basin):
#         if contents is None:
#             raise PreventUpdate
#
#         table_name = DataCategories.DRILLED_WELLS
#
#         return extract_excel_upload(contents, filename, current_data, table_name, basin)
#
#     @callback(
#         Output(f'{prefix}completions-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-table-previous', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-upload-error-text', 'children'),
#         Output(f'{prefix}completions-upload-error-modal', 'is_open'),
#         Input(f'{prefix}completions-upload', 'contents'),
#         State(f'{prefix}completions-upload', 'filename'),
#         State(f'{prefix}completions-table', 'data'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         prevent_initial_call=True
#     )
#     def update_completions_from_excel(contents, filename, current_data, basin):
#         if contents is None:
#             raise PreventUpdate
#
#         table_name = DataCategories.COMPLETIONS
#
#         return extract_excel_upload(contents, filename, current_data, table_name, basin)
#
#     @callback(
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table-previous', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-upload-error-text', 'children'),
#         Output(f'{prefix}production-upload-error-modal', 'is_open'),
#         Input(f'{prefix}production-upload', 'contents'),
#         State(f'{prefix}production-upload', 'filename'),
#         State(f'{prefix}production-table', 'data'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         prevent_initial_call=True
#     )
#     def update_production_from_excel(contents, filename, current_data, basin):
#         if contents is None:
#             raise PreventUpdate
#
#         table_name = DataCategories.PRODUCTION
#
#         return extract_excel_upload(contents, filename, current_data, table_name, basin)
#
#     component_names = [
#         'rig-count',
#         'drilled-wells',
#         'completions'
#     ]
#     for component_name in component_names:
#         @callback(
#             Output(f'{prefix}{component_name}-upload-error-modal', 'is_open', allow_duplicate=True),
#             Input(f'{prefix}{component_name}-upload-error-close', 'n_clicks'),
#             prevent_initial_call=True
#         )
#         def close_error_modal(n_clicks):
#             if n_clicks:
#                 return False
#             raise PreventUpdate
#
#         close_error_modal.__name__ = f'close_{component_name}_error_modal'
#         globals()[close_error_modal.__name__] = close_error_modal
#
#
#     @callback(
#         Output(f'{prefix}snap-to-eia-modal', 'is_open'),
#         Input(f'{prefix}production-snap-to-eia-btn', 'n_clicks'),
#         State(f'{prefix}snap-to-eia-modal', 'is_open'),
#         prevent_initial_call=True
#     )
#     def open_snap_to_eia_modal(n_clicks, is_open):
#         if n_clicks is None:
#             raise PreventUpdate
#         return not is_open
#
#     @callback(
#         Output(f'{prefix}snap-to-eia-modal', 'is_open', allow_duplicate=True),
#         Input(f'{prefix}snap-to-eia-cancel', 'n_clicks'),
#         prevent_initial_call=True
#     )
#     def cancel_snap_to_eia(n_clicks):
#         if not n_clicks:
#             raise PreventUpdate
#         return False
#
#     @callback(
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}unconventional-existing', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}download-data-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}save-to-db-btn', 'disabled', allow_duplicate=True),
#         Output(f'{prefix}snap-to-eia-modal', 'is_open', allow_duplicate=True),
#
#         Input(f'{prefix}snap-to-eia-confirm', 'n_clicks'),
#
#         State(f'{prefix}snap-to-eia-delta-option', 'value'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         State(f'{prefix}unconventional-future', 'data'),
#         State(f'{prefix}conventional-continuous', 'data'),
#         State(f'{prefix}eia-production', 'data'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         State(f'{prefix}start-date-ddown', 'value'),
#         State(f'{prefix}end-date-ddown', 'value'),
#         State(f'{prefix}production-graph', 'figure'),
#
#         prevent_initial_call=True
#     )
#     def snap_to_eia_confirm(
#             n_clicks,
#             delta_option: str,
#             unconventional_existing_data: List[Dict],
#             unconventional_future_data: List[Dict],
#             continuous_conventional_data: List[Dict],
#             eia_data: List[Dict],
#             eia_basin: UsBasins,
#             energy_product: EnergyProduct,
#             scenario_type: ScenarioTypes,
#             start_date: str,
#             end_date: str,
#             previous_prod_fig,
#     ):
#         if n_clicks is None:
#             raise PreventUpdate
#
#         maintain_forecast_delta = (delta_option == "maintain")
#
#         unconventional_existing = unpack_data(unconventional_existing_data)
#         unconventional_future = unpack_data(unconventional_future_data)
#         continuous_conventional = unpack_data(continuous_conventional_data)
#         eia_production = unpack_data(eia_data)
#
#         start_date = datetime.fromisoformat(start_date)
#         end_date = datetime.fromisoformat(end_date)
#         basins_filter = get_basins_filter(eia_basin)
#
#         pipeline = GlobalPipeline(
#             basins_filter=basins_filter,
#             scenario_type=scenario_type,
#             start_date=start_date,
#             end_date=end_date,
#             energy_product_filter=[energy_product]
#         )
#
#         pipeline._existing_wells_unconventional_production = unconventional_existing
#         pipeline._future_wells_unconventional_production = unconventional_future
#         pipeline._conventional_continuous = continuous_conventional
#         pipeline._eia_steo_basin_production = eia_production
#
#         adjustment_model = EIAAdjustmentSeriesModel(
#             pipeline=pipeline,
#             chart_results=False,
#             maintain_forecast_delta=maintain_forecast_delta
#         )
#
#         updated_existing_wells = adjustment_model.run()
#
#         pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             basins_filter=get_basins_filter(eia_basin),
#             energy_product_filter=[energy_product]
#         )
#
#         production_visual = ProductionVisualiser(
#             unconventional_existing_df=updated_existing_wells,
#             unconventional_future_df=unconventional_future,
#             continuous_conventional_df=continuous_conventional,
#             eia_df=eia_production,
#             eia_basin=eia_basin,
#             pipeline=pipeline
#         )
#
#         fig = production_visual.make_chart()
#         fig = preserve_figure_state(fig, previous_prod_fig)
#
#         new_existing_wells_prod_data = pack_data(updated_existing_wells)
#
#         _, table_data, total_columns, total_data = production_visual.make_table_elements()
#
#         download_button_disabled = False
#         save_button_disabled = False
#         modal_is_open = False
#
#         return (
#             fig,
#             new_existing_wells_prod_data,
#             table_data,
#             total_columns,
#             total_data,
#             download_button_disabled,
#             save_button_disabled,
#             modal_is_open
#         )
#
#     @callback(
#         Output(f'{prefix}rig-count-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}rig-count-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}rig-count-history', 'data', allow_duplicate=True),
#         Output(f'{prefix}rig-count-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}rig-count-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}rig-count-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}permits-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-history', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-ratios', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}drilled-ratio-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}drilled-wells-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}drilled-wells-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}completions-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}completions-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-forecast', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-history', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-ratios', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}completions-ratio-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}completions-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}completions-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}ducs-data', 'data', allow_duplicate=True),
#         Output(f'{prefix}ducs-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}unconventional-existing', 'data', allow_duplicate=True),
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}conventional-continuous', 'data', allow_duplicate=True),
#         Output(f'{prefix}eia-production', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}available-type-curves', 'data', allow_duplicate=True),
#         Output(f'{prefix}novi-type-curves', 'data', allow_duplicate=True),
#         Output(f'{prefix}type-curves-overrides', 'data', allow_duplicate=True),
#         Input(f'{prefix}rig-count-run-chain-btn', 'n_clicks'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}start-date-ddown', 'value'),
#         State(f'{prefix}end-date-ddown', 'value'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         prevent_initial_call=True
#     )
#     def run_rig_count_chain(n_clicks, eia_basin, scenario_type, energy_product, start_date, end_date, unconventional_existing_production):
#         if n_clicks is None:
#             raise PreventUpdate
#
#         basins_filter = get_basins_filter(eia_basin)
#         scenario = Scenario.ea_library()
#         start_date = pd.to_datetime(start_date)
#         end_date = pd.to_datetime(end_date)
#
#         pipeline = GlobalPipeline(
#             scenario_type=scenario_type,
#             scenario=scenario,
#             basins_filter=basins_filter,
#             energy_product_filter=[energy_product],
#         )
#
#         """
#         Existing wells from the current app state is necessary to be assigned to the pipeline to get current adjustment series
#         """
#         unconventional_existing_production = unpack_data(unconventional_existing_production)
#         pipeline = update_existing_wells_in_pipeline(pipeline=pipeline, unconventional_existing_production=unconventional_existing_production)
#
#         pipeline = run_chain_model(pipeline)
#
#         """
#         This is due to rigs price sensitive modelling requires full history, but we only want from start to end date in the app shown.
#         """
#         pipeline = filter_by_date_range(pipeline, start_date, end_date)
#         pipeline = filter_by_basins_filter(pipeline, basins_filter)
#
#         (rig_count_history, rig_count_forecast, rig_count_columns, rig_count_data, rig_count_store, rig_count_fig,
#          rig_count_total_columns, rig_count_total_data,
#          permits_fig,
#          drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data,
#          drilled_wells_store, drilled_wells_fig, drilled_well_total_columns, drilled_well_total_data,
#          drilled_wells_ratios, drilled_wells_ratio_fig,
#          completions_history, completions_forecast, completions_columns, completions_data, completions_store,
#          completions_fig, completions_total_columns, completions_total_data,
#          completions_ratios, completions_ratio_fig,
#          ducs_data, ducs_fig, frac_fleets_fig,
#          available_type_curves, type_curves_data, novi_type_curves, type_curve_overrides,
#          unconventional_existing_data, unconventional_future_data, continuous_conventional_data, eia_data, prod_fig,
#          prod_columns, prod_data, prod_total_column, prod_total_data) = load_data(eia_basin, energy_product, pipeline)
#
#         packed_completions_forecast = pack_data(completions_forecast)
#
#         return (rig_count_columns, rig_count_data, rig_count_store, rig_count_fig, rig_count_total_columns,
#                 rig_count_total_data, permits_fig,
#                 drilled_wells_columns, drilled_wells_data, drilled_wells_store, drilled_wells_ratios, drilled_wells_fig,
#                 drilled_wells_ratio_fig,
#                 drilled_well_total_columns, drilled_well_total_data,
#                 completions_columns, completions_data, packed_completions_forecast, completions_store,
#                 completions_ratios,
#                 completions_fig, completions_ratio_fig, completions_total_columns, completions_total_data, ducs_data,
#                 ducs_fig,
#                 unconventional_existing_data, unconventional_future_data, continuous_conventional_data, eia_data,
#                 prod_columns, prod_data, prod_fig, prod_total_column, prod_total_data,
#                 type_curves_data, novi_type_curves, type_curve_overrides)
#
#     @callback(
#         Output(f'{prefix}drilled-wells-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-history', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-ratios', 'data', allow_duplicate=True),
#         Output(f'{prefix}drilled-wells-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}drilled-ratio-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}drilled-wells-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}drilled-wells-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}completions-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}completions-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-forecast', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-history', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-ratios', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}completions-ratio-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}completions-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}completions-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}ducs-data', 'data', allow_duplicate=True),
#         Output(f'{prefix}ducs-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}unconventional-existing', 'data', allow_duplicate=True),
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}conventional-continuous', 'data', allow_duplicate=True),
#         Output(f'{prefix}eia-production', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}available-type-curves', 'data', allow_duplicate=True),
#         Output(f'{prefix}novi-type-curves', 'data', allow_duplicate=True),
#         Output(f'{prefix}type-curves-overrides', 'data', allow_duplicate=True),
#         Input(f'{prefix}drilled-wells-run-chain-btn', 'n_clicks'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}start-date-ddown', 'value'),
#         State(f'{prefix}end-date-ddown', 'value'),
#         State(f'{prefix}rig-count-table', 'data'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         prevent_initial_call=True
#     )
#     def run_drilled_wells_chain(n_clicks, eia_basin, scenario_type, energy_product, start_date, end_date, rig_count_table,
#                                 unconventional_existing_production):
#         if n_clicks is None:
#             raise PreventUpdate
#
#         basins_filter = get_basins_filter(eia_basin)
#         scenario = Scenario.ea_library()
#
#         start_date = pd.to_datetime(start_date)
#         end_date = pd.to_datetime(end_date)
#         rig_count_forecast = unpack_data(rig_count_table)
#
#
#         pipeline = GlobalPipeline(
#             scenario_type=scenario_type,
#             scenario=scenario,
#             basins_filter=basins_filter,
#             energy_product_filter=[energy_product],
#             start_date=start_date,
#             end_date=end_date
#         )
#
#         if eia_basin != UsBasins.REST_OF_L48_METAVALUE:
#             rig_count_forecast_price_sensitive = melt_and_add_fields_rig_price_sensitive(rig_count_forecast, eia_basin)
#             pipeline._rig_count_forecasts_price_sensitive = rig_count_forecast_price_sensitive
#         else:
#             rig_count_forecast_baseline = melt_and_add_fields_rigs_baseline(rig_count_forecast)
#             pipeline._rig_count_forecasts = rig_count_forecast_baseline
#
#         """
#         Existing wells from the current app state is necessary to be assigned to the pipeline to get current adjustment series
#         """
#         unconventional_existing_production = unpack_data(unconventional_existing_production)
#         pipeline = update_existing_wells_in_pipeline(pipeline=pipeline, unconventional_existing_production=unconventional_existing_production)
#
#         model_sequence_config_from_completions = {
#             Models.RIG_COUNT_PRICE_SENSITIVE: False,
#             Models.DRILLED_WELLS: True,
#             Models.COMPLETIONS: True,
#             Models.CONVENTIONAL_PRODUCTION: True,
#             Models.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION: True,
#             Models.TYPE_CURVES_CALIBRATOR: True,
#             Models.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION: True,
#         }
#
#         pipeline = run_chain_model(pipeline, model_sequence_config=model_sequence_config_from_completions)
#         pipeline = filter_by_basins_filter(pipeline, basins_filter)
#
#         (rig_count_history, rig_count_forecast, rig_count_columns, rig_count_data, rig_count_store, rig_count_fig,
#          rig_count_total_columns, rig_count_total_data,
#          permits_fig,
#          drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data,
#          drilled_wells_store, drilled_wells_fig, drilled_well_total_columns, drilled_well_total_data,
#          drilled_wells_ratios, drilled_wells_ratio_fig,
#          completions_history, completions_forecast, completions_columns, completions_data, completions_store,
#          completions_fig, completions_total_columns, completions_total_data,
#          completions_ratios, completions_ratio_fig,
#          ducs_data, ducs_fig, frac_fleet_fig,
#          available_type_curves, type_curves_data, novi_type_curves, type_curve_overrides,
#          unconventional_existing_data, unconventional_future_data, continuous_conventional_data, eia_data, prod_fig,
#          prod_columns, prod_data, prod_total_column, prod_total_data) = load_data(eia_basin, energy_product, pipeline)
#
#         packed_completions_forecast = pack_data(completions_forecast)
#
#         return (drilled_wells_columns, drilled_wells_data, drilled_wells_store, drilled_wells_ratios, drilled_wells_fig,
#                 drilled_wells_ratio_fig,
#                 drilled_well_total_columns, drilled_well_total_data,
#                 completions_columns, completions_data, packed_completions_forecast, completions_store,
#                 completions_ratios,
#                 completions_fig, completions_ratio_fig, completions_total_columns, completions_total_data, ducs_data,
#                 ducs_fig,
#                 unconventional_existing_data, unconventional_future_data, continuous_conventional_data, eia_data,
#                 prod_columns, prod_data, prod_fig, prod_total_column, prod_total_data,
#                 type_curves_data, novi_type_curves, type_curve_overrides)
#
#     @callback(
#         Output(f'{prefix}completions-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}completions-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-forecast', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-history', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-ratios', 'data', allow_duplicate=True),
#         Output(f'{prefix}completions-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}completions-ratio-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}completions-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}completions-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}ducs-data', 'data', allow_duplicate=True),
#         Output(f'{prefix}ducs-graph', 'figure', allow_duplicate=True),
#         Output(f'{prefix}unconventional-existing', 'data', allow_duplicate=True),
#         Output(f'{prefix}unconventional-future', 'data', allow_duplicate=True),
#         Output(f'{prefix}conventional-continuous', 'data', allow_duplicate=True),
#         Output(f'{prefix}eia-production', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'columns', allow_duplicate=True),
#         Output(f'{prefix}production-table', 'data', allow_duplicate=True),
#         Output(f'{prefix}production-graph', 'figure', allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "columns", allow_duplicate=True),
#         Output(f"{prefix}production-table-total", "data", allow_duplicate=True),
#         Output(f'{prefix}available-type-curves', 'data', allow_duplicate=True),
#         Output(f'{prefix}novi-type-curves', 'data', allow_duplicate=True),
#         Output(f'{prefix}type-curves-overrides', 'data', allow_duplicate=True),
#         Input(f'{prefix}completions-run-chain-btn', 'n_clicks'),
#         State(f'{prefix}basin-selection-ddown', 'value'),
#         State(f'{prefix}scenario-type-ddown', 'value'),
#         State(f'{prefix}energy-selection-ddown', 'value'),
#         State(f'{prefix}start-date-ddown', 'value'),
#         State(f'{prefix}end-date-ddown', 'value'),
#         State(f'{prefix}drilled-wells-table', 'data'),
#         State(f'{prefix}unconventional-existing', 'data'),
#         prevent_initial_call=True
#     )
#     def run_completions_chain(n_clicks, eia_basin, scenario_type, energy_product, start_date, end_date, drilled_wells_table,
#                               unconventional_existing_production):
#         if n_clicks is None:
#             raise PreventUpdate
#
#         basins_filter = get_basins_filter(eia_basin)
#         scenario = Scenario.ea_library()
#
#         start_date = pd.to_datetime(start_date)
#         end_date = pd.to_datetime(end_date)
#         drilled_wells_forecast = unpack_data(drilled_wells_table)
#
#
#         pipeline = GlobalPipeline(
#             scenario_type=scenario_type,
#             scenario=scenario,
#             basins_filter=basins_filter,
#             energy_product_filter=[energy_product],
#             start_date=start_date,
#             end_date=end_date
#         )
#
#         pipeline._drilled_wells_forecasts = melt_and_add_fields(drilled_wells_forecast, basin=eia_basin, energy_product=energy_product)
#
#         """
#         Existing wells from the current app state is necessary to be assigned to the pipeline to get current adjustment series
#         """
#         unconventional_existing_production = unpack_data(unconventional_existing_production)
#         pipeline = update_existing_wells_in_pipeline(pipeline=pipeline, unconventional_existing_production=unconventional_existing_production)
#
#         model_sequence_config_from_completions = {
#             Models.RIG_COUNT_PRICE_SENSITIVE: False,
#             Models.DRILLED_WELLS: False,
#             Models.COMPLETIONS: True,
#             Models.CONVENTIONAL_PRODUCTION: True,
#             Models.EXISTING_WELLS_UNCONVENTIONAL_PRODUCTION: True,
#             Models.TYPE_CURVES_CALIBRATOR: False,
#             Models.FUTURE_WELLS_UNCONVENTIONAL_PRODUCTION: True,
#         }
#
#         pipeline = run_chain_model(pipeline, model_sequence_config=model_sequence_config_from_completions)
#         pipeline = filter_by_basins_filter(pipeline, basins_filter)
#
#         (rig_count_history, rig_count_forecast, rig_count_columns, rig_count_data, rig_count_store, rig_count_fig,
#          rig_count_total_columns, rig_count_total_data,
#          permits_fig,
#          drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data,
#          drilled_wells_store, drilled_wells_fig, drilled_well_total_columns, drilled_well_total_data,
#          drilled_wells_ratios, drilled_wells_ratio_fig,
#          completions_history, completions_forecast, completions_columns, completions_data, completions_store,
#          completions_fig, completions_total_columns, completions_total_data,
#          completions_ratios, completions_ratio_fig,
#          ducs_data, ducs_fig, frac_fleets_fig,
#          available_type_curves, type_curves_data, novi_type_curves, type_curve_overrides,
#          unconventional_existing_data, unconventional_future_data, continuous_conventional_data, eia_data, prod_fig,
#          prod_columns, prod_data, prod_total_column, prod_total_data) = load_data(eia_basin, energy_product, pipeline)
#
#         packed_completions_forecast = pack_data(completions_forecast)
#
#         return (completions_columns, completions_data, packed_completions_forecast, completions_store,
#                 completions_ratios,
#                 completions_fig, completions_ratio_fig, completions_total_columns, completions_total_data, ducs_data,
#                 ducs_fig,
#                 unconventional_existing_data, unconventional_future_data, continuous_conventional_data, eia_data,
#                 prod_columns, prod_data, prod_fig, prod_total_column, prod_total_data,
#                 type_curves_data, novi_type_curves, type_curve_overrides)
#
#
#     @callback(
#         Output(f"{prefix}rig-count-table", "data"),
#         Output(f'{prefix}rig-count-table-previous', 'data', allow_duplicate=True),
#
#         Input(f"{prefix}rig-count-naive-extension-btn", "n_clicks"),
#
#         State(f"{prefix}rig-count-table", "data"),
#         State(f'{prefix}end-date-ddown', 'value'),
#         prevent_initial_call=True
#     )
#     def extend_rig_data_naively(n_clicks, rig_count_data, dropdown_end_date):
#         if n_clicks is None or rig_count_data is None or dropdown_end_date is None:
#             raise PreventUpdate
#
#         rig_count_data = unpack_data(rig_count_data)
#         dropdown_end_date = pd.to_datetime(dropdown_end_date)
#
#         if rig_count_data.index.max() >= dropdown_end_date:
#             raise PreventUpdate
#
#         plays_recent_mean = rig_count_data.tail(3).mean().round()
#
#         last_date = rig_count_data.index.max()
#         missing_dates = pd.date_range(start=last_date + relativedelta(months=1),
#                                       end=dropdown_end_date,
#                                       freq='MS')
#
#         extension_data = {}
#         for col in rig_count_data.columns:
#             extension_data[col] = [plays_recent_mean[col]] * len(missing_dates)
#
#         extension_df = pd.DataFrame(extension_data, index=missing_dates)
#         extension_df.index.name = ModelMetadata.DT
#
#         extended_rig_count_data = pd.concat([rig_count_data, extension_df])
#         extended_rig_count_data.index = extended_rig_count_data.index.strftime('%Y-%m')
#         extended_rig_count_data = pack_data(extended_rig_count_data)
#         original_rig_count_data = pack_data(rig_count_data)
#
#         return extended_rig_count_data, original_rig_count_data