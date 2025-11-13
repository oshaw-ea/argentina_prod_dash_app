import pandas as pd
from typing import Tuple, List, Dict, Any
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta
from argentina_prod.configs.enums import ModelMetadata
from argentina_prod.configs.scenarios import ScenarioTypes
from argentina_prod.configs.models_config import CompletionsConfig
from argentina_prod.pipeline.global_pipeline import GlobalPipeline

from pages.modeling.callbacks.utilities.visual_builders.visuals_builders import DataTypes, VisualsBuilder
from pages.utilities import ChartTitles


# class CompletionsVisualiser(VisualsBuilder):
#     @staticmethod
#     def process_and_visualise_data(history_df: pd.DataFrame,
#                                    forecast_df: pd.DataFrame,
#                                    basin: UsBasins = None,
#                                    stacked: bool = True):
#         eia_basin = VisualsBuilder.get_eia_basin_from_df(df=history_df)
#
#         nowcasting_start, nowcasting_end, forecasting_start, history_df, forecast_df = CompletionsVisualiser._combine_history_nowcast_forecast(history_df, forecast_df)
#
#         history_df, forecast_df, columns, data, fig = VisualsBuilder.process_and_visualise_data(history_df=history_df,
#                                                                                          forecast_df=forecast_df,
#                                                                                          history_data_type=DataTypes.PLAY_LEVEL,
#                                                                                          stacked=stacked,
#                                                                                          title=ChartTitles.COMPLETIONS
#                                                                                          )
#
#         fig = VisualsBuilder._add_nowcasting_line(fig=fig, nowcasting_date=nowcasting_start)
#         fig = VisualsBuilder._add_first_forecast_line(fig=fig, first_forecast_date=forecasting_start)
#
#         previous_psm_series = CompletionsVisualiser.previous_psm_series(history=history_df, forecast=forecast_df, eia_basin=eia_basin)
#         fig = VisualsBuilder.add_ea_library_current_snapshot_comparison(fig, previous_psm_series)
#
#         return history_df, forecast_df, columns, data, fig
#
#     @staticmethod
#     def _combine_history_nowcast_forecast(history_df, forecast_df):
#         nowcasting_start = min(forecast_df.index)
#         nowcasting_end = nowcasting_start + relativedelta(months=CompletionsConfig.NOVI_DATA_MONTHS_CUTOFF)
#         forecasting_start = nowcasting_end + relativedelta(months=1)
#
#         history_df = history_df[history_df.index < nowcasting_start]
#         forecast_df = forecast_df[forecast_df.index >= nowcasting_start]
#
#         return nowcasting_start, nowcasting_end, forecasting_start, history_df, forecast_df
#
#
#     @staticmethod
#     def visualise_data(history_df: pd.DataFrame,
#                        forecast_df: pd.DataFrame,
#                        title: ChartTitles,
#                        stacked: bool = True,
#                        ) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]], go.Figure]:
#         eia_basin = VisualsBuilder.get_eia_basin_from_df(df=history_df)
#
#         columns, data, fig = VisualsBuilder.visualise_data(history_df, forecast_df, title, stacked)
#         previous_psm_series = CompletionsVisualiser.previous_psm_series(history=history_df, forecast=forecast_df, eia_basin=eia_basin)
#         fig = VisualsBuilder.add_ea_library_current_snapshot_comparison(fig, previous_psm_series)
#
#         return columns, data, fig
#
#     @staticmethod
#     def update_completions(drilled_wells_history: pd.DataFrame, drilled_wells_forecast: pd.DataFrame,
#                            completions_history: pd.DataFrame, completions_ratios: pd.DataFrame, existing_completions_forecast: pd.DataFrame,
#                            basin: str) -> Tuple[
#         pd.DataFrame, list, List[Dict], go.Figure]:
#
#         drilled_wells_history = drilled_wells_history.drop(basin, axis=1)
#         new_completions = CompletionsRatios.recalculate_completions(
#             drilled_wells_history=drilled_wells_history,
#             drilled_wells_forecast=drilled_wells_forecast,
#             plays_ratios=completions_ratios
#         )
#         existing_completions_forecast = existing_completions_forecast[~existing_completions_forecast.index.isin(new_completions.index)]
#         new_completions = pd.concat([existing_completions_forecast, new_completions])
#         new_completions.sort_index()
#
#         completions_columns, completions_data, completions_fig = CompletionsVisualiser.visualise_data(
#             history_df=completions_history,
#             forecast_df=new_completions,
#             title=ChartTitles.COMPLETIONS
#         )
#
#         return new_completions, completions_columns, completions_data, completions_fig
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
#
#         completions_history_previous_psm = previous_psm_pipeline.novi_completions_history
#         completions_forecast_previous_psm = previous_psm_pipeline.completions_forecasts
#
#         nowcasting_start, nowcasting_end, forecasting_start, history_df, forecast_df = CompletionsVisualiser._combine_history_nowcast_forecast(completions_history_previous_psm, completions_forecast_previous_psm)
#
#         history_previous_psm_sum = history_df.groupby(level=0)[ModelMetadata.VAL].sum()
#         forecast_previous_psm_sum = forecast_df.groupby(level=0)[ModelMetadata.VAL].sum()
#
#         all_indexes = history_previous_psm_sum.index.union(forecast_previous_psm_sum.index)
#
#         history_previous_psm_sum = history_previous_psm_sum.reindex(all_indexes, fill_value=0)
#         forecast_previous_psm_sum = forecast_previous_psm_sum.reindex(all_indexes, fill_value=0)
#
#         previous_psm_series = history_previous_psm_sum + forecast_previous_psm_sum
#
#
#         return previous_psm_series