import pandas as pd
from typing import Tuple, List, Dict, Any
import plotly.graph_objects as go
from argentina_prod.configs.enums import ModelMetadata
from argentina_prod.configs.scenarios import ScenarioTypes
from argentina_prod.pipeline.global_pipeline import GlobalPipeline

# from pages.modeling.callbacks.utilities.visual_builders.drilled_wells_ratios import DrilledWellsRatios
from pages.modeling.callbacks.utilities.visual_builders.visuals_builders import DataTypes, VisualsBuilder
from pages.utilities import ChartTitles

# class DrilledWellsVisualiser(VisualsBuilder):
#     @staticmethod
#     def process_and_visualise_data(history_df: pd.DataFrame,
#                                    forecast_df: pd.DataFrame,
#                                    stacked: bool = True,
#                                    ):
#         eia_basin = VisualsBuilder.get_eia_basin_from_df(df=history_df)
#
#         history_df, forecast_df, columns, data, fig = VisualsBuilder.process_and_visualise_data(history_df=history_df,
#                                                                                          forecast_df=forecast_df,
#                                                                                          history_data_type=DataTypes.BASIN_LEVEL,
#                                                                                          stacked=stacked,
#                                                                                          title=ChartTitles.DRILLED_WELLS
#                                                                                          )
#
#         fig = DrilledWellsVisualiser.add_connector_from_history_to_forecast(history_df=history_df,
#                                                                             forecast_df=forecast_df,
#                                                                             fig=fig)
#
#         forecasting_start = min(forecast_df.index)
#         fig = VisualsBuilder._add_first_forecast_line(fig=fig, first_forecast_date=forecasting_start)
#         previous_psm_series = DrilledWellsVisualiser.previous_psm_series(history=history_df, forecast=forecast_df, eia_basin=eia_basin)
#         fig = VisualsBuilder.add_ea_library_current_snapshot_comparison(fig, previous_psm_series)
#
#         return history_df, forecast_df, columns, data, fig
#
#     @staticmethod
#     def visualise_data(history_df: pd.DataFrame,
#                        forecast_df: pd.DataFrame,
#                        title: ChartTitles,
#                        stacked: bool = True,
#                        ) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]], go.Figure]:
#         eia_basin = history_df.columns[0]
#
#         columns, data, fig = VisualsBuilder.visualise_data(history_df, forecast_df, title, stacked)
#         previous_psm_series = DrilledWellsVisualiser.previous_psm_series(history=history_df, forecast=forecast_df, eia_basin=eia_basin)
#         fig = VisualsBuilder.add_ea_library_current_snapshot_comparison(fig, previous_psm_series)
#
#         return columns, data, fig
#
#     @staticmethod
#     def update_drilled_wells(rig_count_history: pd.DataFrame, rig_count_forecast: pd.DataFrame,
#                              drilled_wells_history: pd.DataFrame, drilled_wells_ratios: pd.DataFrame) -> Tuple[
#         pd.DataFrame, list, List[Dict], go.Figure]:
#         continuous_rig_count = pd.concat([rig_count_history, rig_count_forecast])
#         new_drilled_wells = DrilledWellsRatios.recalculate_drilled_wells(
#             continuous_rig_count=continuous_rig_count,
#             plays_ratios=drilled_wells_ratios
#         )
#
#         drilled_wells_columns, drilled_wells_data, drilled_wells_fig = DrilledWellsVisualiser.visualise_data(
#             history_df=drilled_wells_history,
#             forecast_df=new_drilled_wells,
#             title=ChartTitles.DRILLED_WELLS,
#         )
#
#         return new_drilled_wells, drilled_wells_columns, drilled_wells_data, drilled_wells_fig
#
#     @staticmethod
#     def add_connector_from_history_to_forecast(history_df, forecast_df, fig):
#         if not history_df.empty and not forecast_df.empty:
#             last_history_date = max(history_df.index)
#             first_forecast_date = min(forecast_df.index)
#
#             last_history_total = history_df.sum(axis=1).iloc[-1]
#             first_forecast_total = forecast_df.loc[first_forecast_date].sum()
#
#             history_line_color = fig.data[00].line.color
#
#             fig.add_trace(go.Scatter(
#                 x=[last_history_date, first_forecast_date],
#                 y=[last_history_total, first_forecast_total],
#                 mode='lines',
#                 line=dict(color=history_line_color),
#                 fill='tozeroy',
#                 fillcolor=history_line_color,
#                 opacity=0.8,
#                 showlegend=False,
#                 hoverinfo='skip'
#             ))
#
#         return fig
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
#         drilled_wells_history_previous_psm = previous_psm_pipeline.eia_drilled_wells_history[ModelMetadata.VAL]
#         drilled_wells_forecast_previous_psm = previous_psm_pipeline.drilled_wells_forecasts.groupby(level=0)[ModelMetadata.VAL].sum()
#
#         all_indexes = drilled_wells_history_previous_psm.index.union(drilled_wells_forecast_previous_psm.index)
#
#         drilled_wells_history_previous_psm = drilled_wells_history_previous_psm.reindex(all_indexes, fill_value=0)
#         drilled_wells_forecast_previous_psm = drilled_wells_forecast_previous_psm.reindex(all_indexes, fill_value=0)
#
#         previous_psm_series = drilled_wells_history_previous_psm + drilled_wells_forecast_previous_psm
#
#         return previous_psm_series