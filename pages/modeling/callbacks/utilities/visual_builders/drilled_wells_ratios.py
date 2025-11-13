import pandas as pd
from typing import Optional, Tuple
import plotly.graph_objects as go
from argentina_prod.configs.enums import ModelMetadata

from ea_dash_elements.utilities.visual_settings import VisualSettings
from pages.modeling.callbacks.utilities.visual_builders.visuals_builders import VisualsBuilder


# class DrilledWellsRatios(VisualsBuilder):
#     def __init__(self, drilled_wells_history: pd.DataFrame, drilled_wells_forecast: pd.DataFrame,
#                  rig_count_history: pd.DataFrame, rig_count_forecast: pd.DataFrame):
#         self._basin_ratio = None
#         self._play_ratios = None
#
#         self.drilled_wells_history = drilled_wells_history
#         self.rig_count_history = rig_count_history
#         self.drilled_wells_forecast = drilled_wells_forecast
#         self.rig_count_forecast = rig_count_forecast
#         if self.drilled_wells_history is not None and not self.drilled_wells_history.empty:
#             self.drilled_wells_forecast = self.drilled_wells_forecast[self.drilled_wells_forecast.index > max(self.drilled_wells_history.index)]
#         if self.rig_count_history is not None and not self.rig_count_history.empty:
#             self.rig_count_forecast = self.rig_count_forecast[self.rig_count_forecast.index > max(self.rig_count_history.index)]
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
#         if self.drilled_wells_forecast is not None:
#             first_forecast_date = min(self.drilled_wells_forecast.index)
#             fig = self._add_first_forecast_line(fig=fig, first_forecast_date=first_forecast_date)
#
#
#         base_layout = VisualSettings().make_base_layout_dict()
#         base_layout["title"] = "D2R Ratio"
#         fig.update_layout(base_layout)
#         tickformat = ",.1f"
#
#         fig.update_layout(
#             yaxis=dict(tickformat=tickformat),
#             showlegend=True,
#         )
#         return fig
#
#     def make_basin_ratio(self) -> Optional[pd.Series]:
#         if any(x is None for x in [self.drilled_wells_history, self.drilled_wells_forecast, self.rig_count_history,
#                                    self.rig_count_forecast]):
#             return None
#
#         drilled_wells_forecasts = self.drilled_wells_forecast.sum(axis=1)
#         drilled_wells_history = self.drilled_wells_history.sum(axis=1)
#         if not drilled_wells_history.empty:
#             drilled_wells_forecasts = drilled_wells_forecasts.loc[
#                 drilled_wells_forecasts.index > max(drilled_wells_history.index)]
#         rig_count_forecasts = self.rig_count_forecast.sum(axis=1)
#         rig_count_history = self.rig_count_history.sum(axis=1)
#         if not rig_count_history.empty:
#             rig_count_forecasts = rig_count_forecasts.loc[rig_count_forecasts.index > max(rig_count_history.index)]
#
#         drilled_wells = pd.concat([drilled_wells_history, drilled_wells_forecasts], axis=0)
#         rig_count = pd.concat([rig_count_history, rig_count_forecasts], axis=0)
#
#         basin_ratio = drilled_wells / rig_count
#         return VisualsBuilder.round_up_on_half(basin_ratio, 2)
#
#     def make_play_ratios(self) -> Optional[pd.DataFrame]:
#         if any(x is None for x in [self.drilled_wells_history, self.drilled_wells_forecast, self.rig_count_history,
#                                    self.rig_count_forecast]):
#             return None
#         rig_count = pd.concat([self.rig_count_history, self.rig_count_forecast], axis=0)
#         common_index = self.drilled_wells_forecast.index.intersection(rig_count.index)
#         drilled_wells = self.drilled_wells_forecast.loc[common_index]
#         rig_count = rig_count.loc[common_index]
#         common_plays = rig_count.columns.intersection(drilled_wells.columns).tolist()
#
#         rig_count = rig_count[common_plays]
#         drilled_wells = drilled_wells[common_plays]
#
#         ratio = drilled_wells / rig_count
#         ratio = ratio.fillna(0)
#         ratio = self.fill_zeros_with_average_from_play(ratio)
#         return VisualsBuilder.round_up_on_half(ratio, 2)
#
#     @staticmethod
#     def recalculate_drilled_wells(plays_ratios: pd.DataFrame, continuous_rig_count: pd.DataFrame) -> pd.DataFrame:
#         plays_ratios = plays_ratios.dropna(how='all')
#         plays_ratios.fillna(0, inplace=True)
#         plays_ratios = DrilledWellsRatios.extend_ratios(plays_ratios, continuous_rig_count)
#         drilled_wells = plays_ratios.astype(float) * continuous_rig_count.astype(float)
#         drilled_wells = drilled_wells.dropna(how='all')
#         drilled_wells.fillna(0, inplace=True)
#         drilled_wells = VisualsBuilder.round_up_on_half(drilled_wells, 0)
#         return drilled_wells.astype(int)
#
#     @staticmethod
#     def extend_ratios(plays_ratios: pd.DataFrame, continuous_rig_count: pd.DataFrame) -> pd.DataFrame:
#         rig_count_end_date = continuous_rig_count.index.max()
#         play_ratios_extended_index = pd.date_range(start=plays_ratios.index.min(),
#                                           end=rig_count_end_date,
#                                           freq='MS')
#         play_ratios_extended = plays_ratios.reindex(play_ratios_extended_index).fillna(0)
#         play_ratios_extended = play_ratios_extended.apply(lambda col: col.replace(0, col[col != 0].mean())).fillna(0)
#         play_ratios_extended.index.name = ModelMetadata.DT
#
#         return play_ratios_extended
#
#     def fill_zeros_with_average_from_play(self, play_ratios):
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
#
#     @staticmethod
#     def update_ratios(drilled_wells_history: pd.DataFrame, drilled_wells_forecast: pd.DataFrame,
#                       rig_count_history: pd.DataFrame, rig_count_forecast: pd.DataFrame) -> Tuple[
#         pd.DataFrame, go.Figure]:
#         manager = DrilledWellsRatios(
#             drilled_wells_history=drilled_wells_history,
#             drilled_wells_forecast=drilled_wells_forecast,
#             rig_count_history=rig_count_history,
#             rig_count_forecast=rig_count_forecast
#         )
#
#         ratio_fig = manager.make_chart()
#         ratios_data = manager.play_ratios
#
#         return ratios_data, ratio_fig
