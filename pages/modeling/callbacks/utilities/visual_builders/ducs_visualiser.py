import pandas as pd
from typing import Tuple
import plotly.graph_objects as go
from argentina_prod.configs.models_config import CompletionsConfig

from ea_dash_elements.utilities.visual_settings import VisualSettings
from pages.modeling.callbacks.utilities.visual_builders.visuals_builders import VisualsBuilder
from pages.utilities import DataCategories, ChartTitles


# class DUCsVisualiser(VisualsBuilder):
#     duc_floors = CompletionsConfig.DUC_FLOORS
#
#     @staticmethod
#     def calculate_ducs_from_drilled_wells_and_completions(
#             ducs_history: pd.Series,
#             drilled_wells_forecast: pd.DataFrame,
#             completions_forecast: pd.DataFrame) -> pd.Series:
#         drilled_wells_sum = drilled_wells_forecast.sum(axis=1)
#         completions_sum = completions_forecast.sum(axis=1)
#         ducs_history = ducs_history[ducs_history.columns[0]]
#
#         computation_df = pd.DataFrame()
#         computation_df[f'{DataCategories.DRILLED_WELLS}_t'] = drilled_wells_sum
#         computation_df[f'{DataCategories.COMPLETIONS}_t'] = completions_sum
#         computation_df[f'{DataCategories.DUCS}_t'] = ducs_history
#
#         forecast_period = computation_df.index
#         last_known_duc = ducs_history.iloc[-1]
#         last_history_date = max(ducs_history.dropna().index)
#         if last_history_date not in computation_df.index:
#             computation_df.loc[last_history_date, f'{DataCategories.DUCS}_t'] = last_known_duc
#         computation_df = computation_df.sort_index()
#
#         for idx in forecast_period:
#             prev_idx = computation_df.index.get_indexer([idx])[0] - 1
#             if prev_idx >= 0:
#                 prev_duc = computation_df.loc[computation_df.index[prev_idx], f'{DataCategories.DUCS}_t']
#                 drilled = computation_df.loc[idx, f'{DataCategories.DRILLED_WELLS}_t']
#                 completed = computation_df.loc[idx, f'{DataCategories.COMPLETIONS}_t']
#                 computation_df.loc[idx, f'{DataCategories.DUCS}_t'] = prev_duc + drilled - completed
#
#         return computation_df[f'{DataCategories.DUCS}_t']
#
#     @staticmethod
#     def get_data_for_ducs_visuals(
#                                     basin: UsBasins,
#                                   history_df: pd.DataFrame,
#                                   forecast_series: pd.Series) -> Tuple[
#         pd.Series, pd.Series, pd.Index, pd.Index, int, int, pd.Index]:
#         history_series = history_df[history_df.columns[0]]
#         start_date = min(history_series.index)
#         end_date = max(forecast_series.index)
#         if basin in DUCsVisualiser.duc_floors:
#             soft_floor = DUCsVisualiser.duc_floors[basin]['soft_floor']
#             hard_floor = DUCsVisualiser.duc_floors[basin]['hard_floor']
#         else:
#             soft_floor = None
#             hard_floor = None
#         first_forecast_date = min(forecast_series.index)
#
#         return history_series, forecast_series, start_date, end_date, soft_floor, hard_floor, first_forecast_date
#
#     @staticmethod
#     def visualise_ducs(history_series: pd.Series,
#                        forecast_series: pd.Series,
#                        start_date: pd.Index,
#                        end_date: pd.Index,
#                        soft_floor: int,
#                        hard_floor: int,
#                        first_forecast_date: pd.Index) -> Tuple[pd.Series, pd.Series, pd.Series, go.Figure]:
#
#         fig = go.Figure()
#         colors = VisualSettings().make_rgba_color_iterator(opacity=VisualSettings.STACKED_CHARTS_OPACITY)
#
#         color = next(colors)
#         fig.add_trace(go.Scatter(
#             x=history_series.index,
#             y=history_series,
#             mode='lines',
#             name='Historical DUCs',
#             line=dict(color=color)
#         ))
#
#         color = next(colors)
#         fig.add_trace(go.Scatter(
#             x=forecast_series.index,
#             y=forecast_series,
#             mode='lines',
#             name='Forecast DUCs',
#             line=dict(color=color)
#         ))
#
#         if soft_floor is not None:
#             fig.add_trace(go.Scatter(
#                 x=[start_date, end_date],
#                 y=[soft_floor, soft_floor],
#                 mode='lines',
#                 name=f'Soft Floor ({soft_floor})',
#                 line=dict(color='orange', dash='dash', width=2)
#             ))
#
#         if hard_floor is not None:
#             fig.add_trace(go.Scatter(
#                 x=[start_date, end_date],
#                 y=[hard_floor, hard_floor],
#                 mode='lines',
#                 name=f'Hard Floor ({hard_floor})',
#                 line=dict(color='red', dash='dash', width=2)
#             ))
#
#         fig = VisualsBuilder._add_first_forecast_line(fig=fig, first_forecast_date=first_forecast_date)
#
#         fig.update_layout(
#             title=ChartTitles.DUCS,
#             xaxis_title="Date",
#             yaxis_title="Count",
#             template="plotly_white"
#         )
#
#         combined_series = pd.concat([history_series, forecast_series])
#         combined_series = combined_series[~combined_series.index.duplicated(keep='first')]
#
#         return history_series, forecast_series, combined_series, fig
#
#     @staticmethod
#     def update_ducs(existing_ducs: pd.DataFrame, new_completions: pd.DataFrame,
#                     new_drilled_wells: pd.DataFrame, basin: UsBasins) -> Tuple[pd.DataFrame, go.Figure]:
#         if basin in UsBasins().steo_basins:
#             forecasting_start = min(new_completions.index)
#             ducs_history = existing_ducs[existing_ducs.index < forecasting_start]
#             new_ducs_forecast = DUCsVisualiser.calculate_ducs_from_drilled_wells_and_completions(ducs_history=ducs_history,
#                                                                                                  drilled_wells_forecast=new_drilled_wells,
#                                                                                                  completions_forecast=new_completions)
#
#             history_series, forecast_series, start_date, end_date, soft_floor, hard_floor, first_forecast_date = DUCsVisualiser.get_data_for_ducs_visuals(
#                 basin=basin,
#                 history_df=ducs_history,
#                 forecast_series=new_ducs_forecast
#             )
#
#             ducs_history, new_ducs_forecast, ducs_series, ducs_fig = DUCsVisualiser.visualise_ducs(
#                 history_series=history_series,
#                 forecast_series=forecast_series,
#                 start_date=start_date,
#                 end_date=end_date,
#                 soft_floor=soft_floor,
#                 hard_floor=hard_floor,
#                 first_forecast_date=first_forecast_date
#             )
#
#             new_ducs = existing_ducs.copy()
#             new_ducs[new_ducs.columns[0]] = ducs_series
#         else:
#             error_message = f"{basin} Not in STEO Basins - Cannot Calculate DUCs"
#             ducs_fig = VisualsBuilder.create_empty_figure(
#                 title=error_message,
#                 y_label="DUCs Count"
#             )
#             new_ducs = pd.Series()
#
#         return new_ducs, ducs_fig

