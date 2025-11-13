import pandas as pd
from typing import Optional, Tuple
import plotly.graph_objects as go
from dateutil.relativedelta import relativedelta
from google.auth.compute_engine import detect_gce_residency_linux
from argentina_prod.configs.enums import ModelMetadata
from argentina_prod.configs.models_config import CompletionsConfig

from ea_dash_elements.utilities.visual_settings import VisualSettings
from pages.modeling.callbacks.utilities.visual_builders.visuals_builders import VisualsBuilder

#
# class CompletionsRatios(VisualsBuilder):
#     def __init__(self, completions_history: pd.DataFrame, completions_forecast: pd.DataFrame,
#                  drilled_wells_history: pd.DataFrame, drilled_wells_forecast: pd.DataFrame) -> None:
#         self._basin_ratio: Optional[pd.Series] = None
#         self._play_ratios: Optional[pd.DataFrame] = None
#
#         self.completions_history: pd.DataFrame = completions_history
#         self.completions_forecast: pd.DataFrame = completions_forecast
#         self.drilled_wells_history: pd.DataFrame = drilled_wells_history
#         self.drilled_wells_forecast: pd.DataFrame = drilled_wells_forecast
#
#     @property
#     def basin_ratio(self) -> Optional[pd.Series]:
#         if self._basin_ratio is None:
#             self._basin_ratio = self.make_basin_ratio()
#         return self._basin_ratio
#
#     @property
#     def play_ratios(self) -> Optional[pd.DataFrame]:
#         if self._play_ratios is None:
#             self._play_ratios = self.make_play_ratios()
#         return self._play_ratios
#
#     def make_chart(self) -> go.Figure:
#         fig = go.Figure()
#         colors = VisualSettings().make_rgba_color_iterator(opacity=VisualSettings.STACKED_CHARTS_OPACITY)
#
#         if self.basin_ratio is not None:
#             color = next(colors)
#             params = dict(
#                 name='Basin Ratio',
#                 x=self.basin_ratio.index,
#                 y=self.basin_ratio,
#                 mode='lines',
#                 line=dict(color=color),
#             )
#             fig.add_trace(go.Scatter(**params))
#
#         if self.play_ratios is not None:
#             for play in self.play_ratios.columns:
#                 color = next(colors)
#                 params = dict(
#                     name=play,
#                     x=self.play_ratios.index,
#                     y=self.play_ratios[play],
#                     mode='lines',
#                     line=dict(color=color),
#                 )
#                 fig.add_trace(go.Scatter(**params))
#
#         base_layout = VisualSettings().make_base_layout_dict()
#         base_layout["title"] = "C2D Ratio"
#         fig.update_layout(base_layout)
#         tickformat = ",.2f"
#
#         fig.update_layout(
#             yaxis=dict(tickformat=tickformat),
#             showlegend=True,
#         )
#         return fig
#
#     def make_basin_ratio(self) -> Optional[pd.Series]:
#         if any(x is None for x in [self.completions_history, self.completions_forecast,
#                                    self.drilled_wells_history, self.drilled_wells_forecast]):
#             return None
#
#         drilled_wells_forecasts = self.drilled_wells_forecast.sum(axis=1)
#         drilled_wells_history = self.drilled_wells_history.sum(axis=1)
#         if not drilled_wells_history.empty:
#             drilled_wells_forecasts = drilled_wells_forecasts.loc[
#                 drilled_wells_forecasts.index > max(drilled_wells_history.index)]
#         completions_forecasts = self.completions_forecast.sum(axis=1)
#         completions_history = self.completions_history.sum(axis=1)
#         if not completions_history.empty:
#             completions_forecasts = completions_forecasts.loc[completions_forecasts.index > max(completions_history.index)]
#
#         drilled_wells = pd.concat([drilled_wells_history, drilled_wells_forecasts], axis=0)
#         completions = pd.concat([completions_history, completions_forecasts], axis=0)
#
#         basin_ratio = completions / drilled_wells
#         return VisualsBuilder.round_up_on_half(basin_ratio, 2)
#
#     def make_play_ratios(self) -> Optional[pd.DataFrame]:
#         if any(x is None for x in [self.drilled_wells_history, self.drilled_wells_forecast, self.completions_history,
#                                    self.completions_forecast]):
#             return None
#         drilled_wells_history = self.drilled_wells_history
#         drilled_wells_forecasts = self.drilled_wells_forecast
#
#         if not drilled_wells_history.empty:
#             if self.history_is_basin_and_forecast_is_play(history=drilled_wells_history,
#                                                           forecast=drilled_wells_forecasts):
#                 drilled_wells = drilled_wells_forecasts
#             else:
#                 drilled_wells_forecasts = drilled_wells_forecasts.loc[
#                     drilled_wells_forecasts.index > max(drilled_wells_history.index)]
#                 drilled_wells = pd.concat([drilled_wells_history, drilled_wells_forecasts])
#
#         completions_forecasts = self.completions_forecast.loc[
#             self.completions_forecast.index > max(self.completions_history.index)]
#         completions = pd.concat([self.completions_history, completions_forecasts], axis=0)
#
#         common_index = completions.index.intersection(drilled_wells.index)
#         drilled_wells = drilled_wells.loc[common_index]
#         completions = completions.loc[common_index]
#
#         common_plays = drilled_wells.columns.intersection(completions.columns).tolist()
#         drilled_wells = drilled_wells[common_plays]
#         completions = completions[common_plays]
#
#         ratio = completions / drilled_wells
#         ratio = ratio.fillna(0)
#         ratio = self.fill_zeros_with_average_for_play(ratio)
#         return VisualsBuilder.round_up_on_half(ratio, 2)
#
#     @staticmethod
#     def recalculate_completions(drilled_wells_history: pd.DataFrame, drilled_wells_forecast: pd.DataFrame,
#                                 plays_ratios: pd.DataFrame) -> pd.DataFrame:
#         continuous_drilled_wells = pd.concat([drilled_wells_history, drilled_wells_forecast])
#         plays_ratios = plays_ratios.dropna(how='all')
#         plays_ratios.fillna(0, inplace=True)
#         plays_ratios = CompletionsRatios.extend_ratios(plays_ratios, continuous_drilled_wells)
#         completions = plays_ratios.astype(float) * continuous_drilled_wells.astype(float)
#         completions = completions.dropna(how='all')
#         completions.fillna(0, inplace=True)
#         completions = VisualsBuilder.round_up_on_half(completions, decimals=0)
#         return completions.astype(int)
#
#
#     def fill_zeros_with_average_for_play(self, play_ratios):
#         play_ratios_filled = play_ratios.copy()
#         play_ratios_filled = play_ratios_filled.apply(lambda col: col.replace(0, col[col != 0].mean())).fillna(0)
#         play_ratios_filled = self.fill_zero_ratio_series_with_basin_average(play_ratios_filled)
#
#         return play_ratios_filled
#
#     def fill_zero_ratio_series_with_basin_average(self, play_ratios):
#         play_ratios_filled = play_ratios.copy()
#
#         for col in play_ratios.columns:
#             zero_mask = play_ratios[col] == 0
#             if zero_mask.any():
#                 for idx in play_ratios.index[zero_mask]:
#                     play_ratios_filled.loc[idx, col] = self.basin_ratio[idx]
#
#         return play_ratios_filled
#
#     @staticmethod
#     def fill_zeros_with_average_for_play(play_ratios):
#         play_ratios_filled = play_ratios.copy()
#         play_ratios_filled = play_ratios_filled.apply(lambda col: col.replace(0, col[col != 0].mean())).fillna(0)
#         play_ratios_filled = CompletionsRatios.fill_zero_ratio_series_with_basin_average(play_ratios_filled)
#
#         return play_ratios_filled
#
#     @staticmethod
#     def fill_zero_ratio_series_with_basin_average(play_ratios):
#         play_ratios_filled = play_ratios.copy()
#
#         for col in play_ratios.columns:
#             zero_mask = play_ratios[col] == 0
#             if zero_mask.any():
#                 for idx in play_ratios.index[zero_mask]:
#                     other_cols = [c for c in play_ratios.columns if c != col]
#                     row_values = play_ratios.loc[idx, other_cols]
#                     row_mean = row_values[row_values != 0].mean()
#
#                     play_ratios_filled.loc[idx, col] = row_mean
#
#         return play_ratios_filled
#
#     @staticmethod
#     def fill_zeros_with_average_for_play(play_ratios):
#         play_ratios_filled = play_ratios.copy()
#         play_ratios_filled = play_ratios_filled.apply(lambda col: col.replace(0, col[col != 0].mean())).fillna(0)
#         play_ratios_filled = CompletionsRatios.fill_zero_ratio_series_with_basin_average(play_ratios_filled)
#
#         return play_ratios_filled
#
#     @staticmethod
#     def fill_zero_ratio_series_with_basin_average(play_ratios):
#         play_ratios_filled = play_ratios.copy()
#
#         for col in play_ratios.columns:
#             zero_mask = play_ratios[col] == 0
#             if zero_mask.any():
#                 for idx in play_ratios.index[zero_mask]:
#                     other_cols = [c for c in play_ratios.columns if c != col]
#                     row_values = play_ratios.loc[idx, other_cols]
#                     row_mean = row_values[row_values != 0].mean()
#
#                     play_ratios_filled.loc[idx, col] = row_mean
#
#         return play_ratios_filled
#
#     @staticmethod
#     def fill_zeros_with_average_for_play(play_ratios):
#         play_ratios_filled = play_ratios.copy()
#         play_ratios_filled = play_ratios_filled.apply(lambda col: col.replace(0, col[col != 0].mean())).fillna(0)
#         play_ratios_filled = CompletionsRatios.fill_zero_ratio_series_with_basin_average(play_ratios_filled)
#
#         return play_ratios_filled
#
#     @staticmethod
#     def fill_zero_ratio_series_with_basin_average(play_ratios):
#         play_ratios_filled = play_ratios.copy()
#
#         for col in play_ratios.columns:
#             zero_mask = play_ratios[col] == 0
#             if zero_mask.any():
#                 for idx in play_ratios.index[zero_mask]:
#                     other_cols = [c for c in play_ratios.columns if c != col]
#                     row_values = play_ratios.loc[idx, other_cols]
#                     row_mean = row_values[row_values != 0].mean()
#
#                     play_ratios_filled.loc[idx, col] = row_mean
#
#         return play_ratios_filled
#
#     @staticmethod
#     def update_ratios(completions_history: pd.DataFrame, completions_forecast: pd.DataFrame,
#                       drilled_wells_history: pd.DataFrame, drilled_wells_forecast: pd.DataFrame) -> Tuple[
#         pd.DataFrame, go.Figure]:
#         manager = CompletionsRatios(
#             completions_history=completions_history,
#             completions_forecast=completions_forecast,
#             drilled_wells_history=drilled_wells_history,
#             drilled_wells_forecast=drilled_wells_forecast
#         )
#
#         ratio_fig = manager.make_chart()
#
#         nowcasting_start = min(completions_forecast.index)
#         nowcasting_end = nowcasting_start + relativedelta(months=CompletionsConfig.NOVI_DATA_MONTHS_CUTOFF)
#         forecasting_start = nowcasting_end + relativedelta(months=1)
#
#         ratio_fig = VisualsBuilder._add_nowcasting_line(fig=ratio_fig, nowcasting_date=nowcasting_start)
#         ratio_fig = VisualsBuilder._add_first_forecast_line(fig=ratio_fig, first_forecast_date=forecasting_start)
#
#         ratios_data = manager.play_ratios
#
#         return ratios_data, ratio_fig
#
#     @staticmethod
#     def extend_ratios(plays_ratios: pd.DataFrame, continuous_drilled_wells: pd.DataFrame) -> pd.DataFrame:
#         drilled_wells_end_date = continuous_drilled_wells.index.max()
#         play_ratios_extended_index = pd.date_range(start=plays_ratios.index.min(),
#                                           end=drilled_wells_end_date,
#                                           freq='MS')
#         play_ratios_extended = plays_ratios.reindex(play_ratios_extended_index).fillna(0)
#         play_ratios_extended = play_ratios_extended.apply(lambda col: col.replace(0, col[col != 0].mean())).fillna(0)
#         play_ratios_extended.index.name = ModelMetadata.DT
#
#         return play_ratios_extended
#