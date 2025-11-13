import pandas as pd
from typing import Dict, List, Any, Tuple
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta
from argentina_prod.configs.enums import ModelMetadata
from argentina_prod.configs.scenarios import ScenarioTypes
from argentina_prod.pipeline.global_pipeline import GlobalPipeline

from pages.modeling.callbacks.utilities.visual_builders.visuals_builders import VisualsBuilder, DataTypes
from pages.utilities import ChartTitles
from typing import Union


# class RigCountVisualiser(VisualsBuilder):
#
#     def __init__(self, history: Union[pd.Series, pd.DataFrame, None], forecast: pd.DataFrame = None):
#         super().__init__(history=history, forecast=forecast)
#
#     @staticmethod
#     def process_and_visualise_data(history_df: pd.DataFrame,
#                                    forecast_df: pd.DataFrame,
#                                    stacked: bool = True) -> Tuple[
#         pd.DataFrame, pd.DataFrame, List[Dict[str, str]], List[Dict[str, Any]], go.Figure]:
#         eia_basin = VisualsBuilder.get_eia_basin_from_df(df=history_df)
#         history_df = history_df.round(0)
#         forecast_df = forecast_df.round(0)
#         history_df, forecast_df, columns, data, fig = VisualsBuilder.process_and_visualise_data(history_df=history_df,
#                                                                                          forecast_df=forecast_df,
#                                                                                          history_data_type=DataTypes.PLAY_LEVEL,
#                                                                                          stacked=stacked,
#                                                                                          title=ChartTitles.RIG_COUNT
#                                                                                          )
#
#         if not history_df.empty:
#             history_df = history_df.fillna(0)
#             forecasting_start = max(history_df.index) + relativedelta(months=1)
#         else:
#             forecasting_start = min(forecast_df.index)
#         fig = VisualsBuilder._add_first_forecast_line(fig=fig, first_forecast_date=forecasting_start)
#         previous_psm_series = RigCountVisualiser.previous_psm_series(history=history_df, forecast=forecast_df, eia_basin=eia_basin)
#         fig = VisualsBuilder.add_ea_library_current_snapshot_comparison(fig, previous_psm_series)
#
#         return history_df, forecast_df, columns, data, fig
#
#     @staticmethod
#     def visualise_data(history_df: pd.DataFrame,
#                        forecast_df: pd.DataFrame,
#                        title: ChartTitles,
#                        eia_basin: UsBasins,
#                        stacked: bool = True,
#                        ) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]], go.Figure]:
#
#         columns, data, fig = VisualsBuilder.visualise_data(history_df, forecast_df, title, stacked)
#         previous_psm_series = RigCountVisualiser.previous_psm_series(history=history_df, forecast=forecast_df, eia_basin=eia_basin)
#         fig = VisualsBuilder.add_ea_library_current_snapshot_comparison(fig, previous_psm_series)
#
#         return columns, data, fig
#
#
#     @staticmethod
#     def _add_price_to_figure(fig: go.Figure, price_series: pd.Series,
#                             name: str = 'Price', color: str = 'black') -> go.Figure:
#         dollar_hover_template = '<name> : %{y:$,.2f}<extra></extra>'
#         return VisualsBuilder.add_secondary_axis_line(
#             fig=fig,
#             series=price_series,
#             name=name,
#             line_color=color,
#             hover_template=dollar_hover_template
#         )
#
#     @staticmethod
#     def add_hh_price_to_fig(rig_count_fig: go.Figure, pipeline: GlobalPipeline) -> go.Figure:
#         hh_price_forecast = pipeline.ea_forecast_hh_price[ModelMetadata.VAL]
#         rig_count_fig = RigCountVisualiser._add_price_to_figure(rig_count_fig, hh_price_forecast, name='HH Forecast',
#                                                                color='Gray')
#
#         return rig_count_fig
#
#     @staticmethod
#     def add_wti_price_to_fig(rig_count_fig: go.Figure, pipeline: GlobalPipeline) -> go.Figure:
#         wti_price_forecast = pipeline.smoothed_medium_term_wti_forecast[ModelMetadata.VAL]
#         rig_count_fig = RigCountVisualiser._add_price_to_figure(rig_count_fig, wti_price_forecast, name='WTI Forecast',
#                                                                color='Black')
#
#         return rig_count_fig
#
#     @staticmethod
#     def previous_psm_series(history, forecast, eia_basin):
#         basins_filter = get_basins_filter(eia_basin)
#         previous_psm_pipeline = GlobalPipeline(
#             scenario_type=ScenarioTypes.EA_LIBRARY,
#             asof_datetime=VisualsBuilder.get_last_snapshot_datetime(),
#             basins_filter=basins_filter,
#             start_date=history.index.min(),
#             end_date=forecast.index.max()
#         )
#         rigs_history_previous_psm = previous_psm_pipeline.rig_count_history.groupby(level=0)[ModelMetadata.VAL].sum()
#         rigs_forecast_previous_psm = previous_psm_pipeline.prioritised_rig_count_forecasts.groupby(level=0)[ModelMetadata.VAL].sum()
#
#         all_indexes = rigs_history_previous_psm.index.union(rigs_forecast_previous_psm.index)
#
#         rigs_history_previous_psm = rigs_history_previous_psm.reindex(all_indexes, fill_value=0)
#         rigs_forecast_previous_psm = rigs_forecast_previous_psm.reindex(all_indexes, fill_value=0)
#
#         previous_psm_series = rigs_history_previous_psm + rigs_forecast_previous_psm
#
#         return previous_psm_series