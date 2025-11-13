from typing import Dict
import pandas as pd
import plotly.graph_objects as go
from helper_functions_ea import EnergyProduct
# from argentina_prod.models.type_curves.type_curve import TypeCurveLoader

from argentina_prod.pipeline.global_pipeline import GlobalPipeline

from pages.modeling.callbacks.utilities.visual_builders.completions_ratios import CompletionsRatios
from pages.modeling.callbacks.utilities.visual_builders.completions_visualiser import CompletionsVisualiser
from pages.modeling.callbacks.utilities.visual_builders.drilled_wells_ratios import DrilledWellsRatios
from pages.modeling.callbacks.utilities.visual_builders.drilled_wells_visualiser import DrilledWellsVisualiser
from pages.modeling.callbacks.utilities.visual_builders.ducs_visualiser import DUCsVisualiser
from pages.modeling.callbacks.utilities.visual_builders.rig_count_visualiser import RigCountVisualiser
from pages.modeling.callbacks.utilities.visual_builders.visuals_builders import VisualsBuilder, DataTypes
from pages.modeling.callbacks.utilities.visual_builders.production_visualiser import ProductionVisualiser
from pages.utilities import ChartTitles, DataCategories, pack_data


# def load_initial_rig_count(pipeline: GlobalPipeline, novi_history_availability: Dict[str, bool], basin: UsBasins) -> tuple:
#     if novi_history_availability[DataCategories.RIG_COUNT]:
#         rig_count_history = pipeline.rig_count_history
#     else:
#         rig_count_history = pd.DataFrame()
# 
#     rig_count_forecast = pipeline.prioritised_rig_count_forecasts
#     rig_count_history, rig_count_forecast, rig_count_columns, rig_count_data, rig_count_fig = RigCountVisualiser.process_and_visualise_data(
#         history_df=rig_count_history,
#         forecast_df=rig_count_forecast
#     )
#     price_config = RigCountPrice.PRICE_CONFIG
#     if basin in price_config:
#         basin_price_config = price_config[basin]
# 
#         if EnergyProduct().NATURAL_GAS in basin_price_config:
#             rig_count_fig = RigCountVisualiser.add_hh_price_to_fig(rig_count_fig, pipeline)
# 
#         if EnergyProduct().CRUDE_OIL in basin_price_config:
#             rig_count_fig = RigCountVisualiser.add_wti_price_to_fig(rig_count_fig, pipeline)
#     else:
#         rig_count_fig = RigCountVisualiser.add_hh_price_to_fig(rig_count_fig, pipeline)
#         rig_count_fig = RigCountVisualiser.add_wti_price_to_fig(rig_count_fig, pipeline)
# 
#     total_columns, total_data = RigCountVisualiser.make_total_table(rig_count_forecast)
#     packed_rig_count_history = pack_data(rig_count_history)
# 
#     return rig_count_history, rig_count_forecast, rig_count_columns, rig_count_data, packed_rig_count_history, rig_count_fig, total_columns, total_data
# 
# 
# def load_initial_permits(pipeline: GlobalPipeline, basin: UsBasins,
#                          novi_history_availability: Dict[str, bool]) -> go.Figure:
#     if novi_history_availability[DataCategories.PERMITS]:
#         permits_history = VisualsBuilder.process_data(df=pipeline.permits, data_type=DataTypes.PLAY_LEVEL)
#         permits_fig = VisualsBuilder(history=permits_history, forecast=None).make_chart(stacked=True,
#                                                                                         title=ChartTitles.PERMITS)
#     else:
#         permits_fig = VisualsBuilder.create_empty_figure(
#             title=f"No Permits Data Available for {basin}",
#             y_label="Permits Count"
#         )
#     return permits_fig
# 
# 
# def load_initial_drilled_wells(pipeline: GlobalPipeline) -> tuple:
#     drilled_wells_forecast = pipeline.drilled_wells_forecasts
#     drilled_wells_history = pipeline.eia_drilled_wells_history
#     drilled_wells_forecast = drilled_wells_forecast.loc[
#         drilled_wells_forecast.index > max(drilled_wells_history.index)]
# 
#     drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data, drilled_wells_fig = DrilledWellsVisualiser.process_and_visualise_data(
#         history_df=drilled_wells_history,
#         forecast_df=drilled_wells_forecast,
#     )
#     total_columns, total_data = DrilledWellsVisualiser.make_total_table(drilled_wells_forecast)
#     packed_drilled_wells = pack_data(drilled_wells_history)
# 
#     return drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data, packed_drilled_wells, drilled_wells_fig, total_columns, total_data
# 
# 
# def load_initial_drilled_wells_ratios(rig_count_history: pd.DataFrame,
#                                       rig_count_forecast: pd.DataFrame, drilled_wells_history: pd.DataFrame,
#                                       drilled_wells_forecast: pd.DataFrame) -> tuple:
#     drilled_wells_ratios, drilled_wells_ratio_fig = DrilledWellsRatios.update_ratios(
#         drilled_wells_history=drilled_wells_history,
#         drilled_wells_forecast=drilled_wells_forecast,
#         rig_count_history=rig_count_history,
#         rig_count_forecast=rig_count_forecast)
#     packed_drilled_wells_ratios = pack_data(drilled_wells_ratios)
# 
#     return packed_drilled_wells_ratios, drilled_wells_ratio_fig
# 
# 
# def load_initial_completions(pipeline: GlobalPipeline, novi_history_availability: Dict[str, bool]) -> tuple:
#     if novi_history_availability[DataCategories.COMPLETIONS]:
#         completions_history = pipeline.novi_completions_history
#     else:
#         completions_history = pd.DataFrame()
#     completions_forecast = pipeline.completions_forecasts
# 
#     completions_history, completions_forecast, completions_columns, completions_data, completions_fig = CompletionsVisualiser.process_and_visualise_data(
#         history_df=completions_history,
#         forecast_df=completions_forecast
#     )
#     total_columns, total_data = CompletionsVisualiser.make_total_table(completions_forecast)
#     packed_completions_history = pack_data(completions_history)
# 
#     return completions_history, completions_forecast, completions_columns, completions_data, packed_completions_history, completions_fig, total_columns, total_data
# 
# 
# def load_initial_completions_ratios(drilled_wells_history: pd.DataFrame,
#                                     drilled_wells_forecast: pd.DataFrame, completions_history: pd.DataFrame,
#                                     completions_forecast: pd.DataFrame) -> tuple:
#     completions_ratios, completions_ratio_fig = CompletionsRatios.update_ratios(
#         completions_history=completions_history,
#         completions_forecast=completions_forecast,
#         drilled_wells_history=drilled_wells_history,
#         drilled_wells_forecast=drilled_wells_forecast
#     )
#     packed_completions_ratios = pack_data(completions_ratios)
# 
#     return packed_completions_ratios, completions_ratio_fig
# 
# 
# def load_initial_ducs(pipeline: GlobalPipeline, basin: UsBasins,
#                       drilled_wells_forecast: pd.DataFrame, completions_forecast: pd.DataFrame) -> tuple:
#     if basin in UsBasins().steo_basins:
#         ducs_history = pipeline.ducs_history
#         ducs_forecast = DUCsVisualiser.calculate_ducs_from_drilled_wells_and_completions(
#             ducs_history=ducs_history,
#             drilled_wells_forecast=drilled_wells_forecast,
#             completions_forecast=completions_forecast
#         )
# 
#         history_series, forecast_series, start_date, end_date, soft_floor, hard_floor, first_forecast_date = DUCsVisualiser.get_data_for_ducs_visuals(
#             basin=basin,
#             history_df=ducs_history,
#             forecast_series=ducs_forecast
#         )
#         ducs_history, ducs_forecast, ducs_series, ducs_fig = DUCsVisualiser.visualise_ducs(
#             history_series=history_series,
#             forecast_series=forecast_series,
#             start_date=start_date,
#             end_date=end_date,
#             soft_floor=soft_floor,
#             hard_floor=hard_floor,
#             first_forecast_date=first_forecast_date
#         )
#         ducs_data = pack_data(ducs_series)
#     else:
#         error_message = f"{basin} Not in STEO Basins - Cannot Calculate DUCs"
#         ducs_fig = VisualsBuilder.create_empty_figure(
#             title=error_message,
#             y_label="DUCs Count"
#         )
#         ducs_data = pack_data(pd.DataFrame())
# 
#     return ducs_data, ducs_fig
# 
# 
# def load_initial_frac_fleets(pipeline: GlobalPipeline, basin: UsBasins) -> go.Figure:
#     frac_fleets = pipeline.frac_fleets
#     if frac_fleets is not None and not frac_fleets.empty:
#         frac_fleets_processed = VisualsBuilder.process_data(df=frac_fleets, data_type=DataTypes.PLAY_LEVEL)
#         frac_fleets_fig = VisualsBuilder(history=frac_fleets_processed, forecast=None).make_chart(
#             stacked=True,
#             title=ChartTitles.FRAC_FLEETS
#         )
#     else:
#         frac_fleets_fig = VisualsBuilder.create_empty_figure(
#             title=f"No Frac Fleets Data Available for {basin}",
#             y_label="Frac Fleets Count"
#         )
#     return frac_fleets_fig
# 
# 
# def load_initial_production(pipeline: GlobalPipeline, eia_basin: UsBasins):
#     unconventional_existing_df = pipeline.existing_wells_unconventional_production
#     unconventional_future_df = pipeline.future_wells_unconventional_production
#     continuous_conventional_df = pipeline.conventional_continuous
#     eia_df = pipeline.eia_steo_basin_production
# 
#     fig, columns, data, total_columns, total_data = ProductionVisualiser(
#         unconventional_existing_df=unconventional_existing_df,
#         unconventional_future_df=unconventional_future_df,
#         continuous_conventional_df=continuous_conventional_df,
#         eia_df=eia_df,
#         eia_basin=eia_basin,
#         pipeline=pipeline
#     ).process_and_visualise_data()
# 
# 
#     unconventional_existing_data = pack_data(unconventional_existing_df)
#     unconventional_future_data = pack_data(unconventional_future_df)
#     continuous_conventional_data = pack_data(continuous_conventional_df)
#     eia_data = pack_data(eia_df)
#     return unconventional_existing_data, unconventional_future_data, continuous_conventional_data, eia_data, fig, columns, data, total_columns, total_data
# 
# 
# 
# def load_data(basin, energy_product, pipeline):
#     basins_filter = get_basins_filter(basin)
#     novi_history_availability = {
#         DataCategories.RIG_COUNT: basin not in MissingData.RIG_COUNT,
#         DataCategories.COMPLETIONS: basin not in MissingData.COMPLETIONS,
#         DataCategories.PERMITS: basin not in MissingData.PERMITS,
#         DataCategories.DUCS: basin in UsBasins().steo_basins
#     }
#     rig_count_history, rig_count_forecast, rig_count_columns, rig_count_data, rig_count_store, rig_count_fig, rig_count_total_columns, rig_count_total_data = load_initial_rig_count(
#         pipeline=pipeline,
#         novi_history_availability=novi_history_availability,
#         basin=basin
#     )
#     permits_fig = load_initial_permits(
#         pipeline=pipeline,
#         basin=basin,
#         novi_history_availability=novi_history_availability
#     )
# 
#     drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data, drilled_wells_store, drilled_wells_fig, drilled_well_total_columns, drilled_well_total_data = load_initial_drilled_wells(
#         pipeline=pipeline,
#     )
# 
#     drilled_wells_ratios, drilled_wells_ratio_fig = load_initial_drilled_wells_ratios(
#         rig_count_history=rig_count_history,
#         rig_count_forecast=rig_count_forecast,
#         drilled_wells_history=drilled_wells_history,
#         drilled_wells_forecast=drilled_wells_forecast
#     )
# 
#     completions_history, completions_forecast, completions_columns, completions_data, completions_store, completions_fig, completions_total_columns, completions_total_data = load_initial_completions(
#         pipeline=pipeline,
#         novi_history_availability=novi_history_availability
#     )
# 
#     completions_ratios, completions_ratio_fig = load_initial_completions_ratios(
#         drilled_wells_history=drilled_wells_history,
#         drilled_wells_forecast=drilled_wells_forecast,
#         completions_history=completions_history,
#         completions_forecast=completions_forecast
#     )
# 
#     ducs_data, ducs_fig = load_initial_ducs(
#         pipeline=pipeline,
#         basin=basin,
#         drilled_wells_forecast=drilled_wells_forecast,
#         completions_forecast=completions_forecast
#     )
# 
#     frac_fleets_fig = load_initial_frac_fleets(
#         pipeline=pipeline,
#         basin=basin,
#     )
# 
#     available_type_curves = TypeCurveLoader().get_available_type_curves(
#         eia_basin_filter=basins_filter,
#         energy_product_filter=[energy_product])
#     type_curves_data = pack_data(available_type_curves)
#     # type curves are loaded as needed
#     # this clears the data cache when loading a new basin or product
#     novi_type_curves = None
#     type_curve_overrides = None
# 
#     (unconventional_existing_data,
#      unconventional_future_data,
#      continuous_conventional_data,
#      eia_data,
#      prod_fig,
#      prod_columns,
#      prod_data, prod_total_column, prod_total_data) = load_initial_production(pipeline=pipeline, eia_basin=basin)
# 
#     return (rig_count_history, rig_count_forecast, rig_count_columns, rig_count_data, rig_count_store, rig_count_fig,
#             rig_count_total_columns, rig_count_total_data,
#             permits_fig,
#             drilled_wells_history, drilled_wells_forecast, drilled_wells_columns, drilled_wells_data,
#             drilled_wells_store, drilled_wells_fig, drilled_well_total_columns, drilled_well_total_data,
#             drilled_wells_ratios, drilled_wells_ratio_fig,
#             completions_history, completions_forecast, completions_columns, completions_data, completions_store,
#             completions_fig, completions_total_columns, completions_total_data,
#             completions_ratios, completions_ratio_fig,
#             ducs_data, ducs_fig,
#             frac_fleets_fig,
#             available_type_curves, type_curves_data, novi_type_curves, type_curve_overrides,
#             unconventional_existing_data, unconventional_future_data, continuous_conventional_data, eia_data, prod_fig,
#             prod_columns, prod_data, prod_total_column, prod_total_data)