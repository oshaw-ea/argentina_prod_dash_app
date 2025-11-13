from dateutil.relativedelta import relativedelta
from argentina_prod.configs.scenarios import ScenarioTypes
from argentina_prod.pipeline.global_pipeline import GlobalPipeline

from pages.modeling.callbacks.utilities.visual_builders.visuals_builders import DataTypes, VisualsBuilder
import pandas as pd
from typing import Union
from ea_dash_elements.utilities.visual_settings import VisualSettings
from dash.dash_table.Format import Format, Group
import plotly.graph_objects as go
from argentina_prod.configs.enums import ShoojuFields, ModelMetadata
from helper_functions_ea import Unit, EnergyProduct
from typing import List, Dict

from argentina_prod.models.unconventional_production.unconventional_production_model import UnconventionalProductionModel, \
    UnconventionalProductionModelData

#
# class ProductionVisualiser(VisualsBuilder):
#
#     def __init__(self,
#                  unconventional_existing_df: pd.DataFrame,
#                  unconventional_future_df: pd.DataFrame,
#                  continuous_conventional_df: pd.DataFrame,
#                  eia_df: Union[pd.DataFrame, None],
#                  eia_basin: UsBasins,
#                  pipeline: GlobalPipeline
#                  ):
#
#         energy_product = unconventional_existing_df[ModelMetadata.ENERGY_PRODUCT].unique()
#         self._previous_psm_series = None
#         self.pipeline = pipeline
#         if len(energy_product) > 1:
#             raise ValueError(f"Multiple energy products found in unconventional existing dataframe: {energy_product}")
#         self.energy_product = energy_product[0]
#         self.last_psm_history_date = self.get_last_psm_history_date()
#
#         self.unconventional_existing_df = VisualsBuilder.process_data(df=unconventional_existing_df,
#                                                                       data_type=DataTypes.PLAY_LEVEL).round(0)
#         self.unconventional_future_df = VisualsBuilder.process_data(df=unconventional_future_df,
#                                                                     data_type=DataTypes.PLAY_LEVEL).round(0)
#         self.continuous_conventional_df = VisualsBuilder.process_data(df=continuous_conventional_df,
#                                                                       data_type=DataTypes.PLAY_LEVEL).round(0)
#         self.eia_df = eia_df
#         if self.eia_df is not None:
#             self.eia_df = self.eia_df.round(0)
#         self.eia_basin = eia_basin
#
#     @property
#     def previous_psm_series(self):
#         if self._previous_psm_series is None:
#             basins_filter = get_basins_filter(self.eia_basin)
#             previous_psm_pipeline = GlobalPipeline(
#                 scenario_type=ScenarioTypes.EA_LIBRARY,
#                 asof_datetime=VisualsBuilder.get_last_snapshot_datetime(),
#                 basins_filter=basins_filter,
#                 energy_product_filter=[self.energy_product],
#                 start_date=self.continuous_conventional_df.index.min(),
#                 end_date=self.continuous_conventional_df.index.max()
#             )
#             existing_wells_previous_psm = previous_psm_pipeline.existing_wells_unconventional_production.groupby(level=0)[ModelMetadata.VAL].sum()
#             future_wells_previous_psm = previous_psm_pipeline.future_wells_unconventional_production.groupby(level=0)[ModelMetadata.VAL].sum()
#             conventional_continuous_previous_psm = previous_psm_pipeline.conventional_continuous.groupby(level=0)[ModelMetadata.VAL].sum()
#
#             all_indexes = existing_wells_previous_psm.index.union(future_wells_previous_psm.index).union(
#                 conventional_continuous_previous_psm.index)
#
#             existing_wells_previous_psm = existing_wells_previous_psm.reindex(all_indexes, fill_value=0)
#             future_wells_previous_psm = future_wells_previous_psm.reindex(all_indexes, fill_value=0)
#             conventional_continuous_previous_psm = conventional_continuous_previous_psm.reindex(all_indexes,
#                                                                                                 fill_value=0)
#             previous_psm_series = existing_wells_previous_psm + future_wells_previous_psm + conventional_continuous_previous_psm
#
#             self._previous_psm_series = previous_psm_series
#         return self._previous_psm_series
#
#     @staticmethod
#     def _add_last_psm_history_line(fig: go.Figure, last_psm_history_date: pd.Timestamp) -> go.Figure:
#         fig.add_vline(x=last_psm_history_date, line_width=2,
#                       line_dash="dash", line_color=VisualSettings.FIRST_FORECAST_LINE_COLOR)
#         fig.add_annotation(
#             x=last_psm_history_date,
#             y=1,
#             text='Last PSM history',
#             showarrow=False,
#             font=dict(color=VisualSettings.FIRST_FORECAST_LINE_COLOR, size=12),
#             xanchor="left",
#             yanchor="bottom",
#             textangle=-30,
#             yref='paper'
#         )
#
#         return fig
#
#     def get_last_psm_history_date(self):
#         if self.energy_product == EnergyProduct().CRUDE_OIL:
#             eia_padd_production = self.pipeline.eia_steo_padd_production
#             eia_psm_last_history_date = eia_padd_production.index.max()
#             return eia_psm_last_history_date
#         return None
#
#     def get_modified_plays_completions(self, previous_df, new_df) -> List[UsPlay]:
#         modified_columns = []
#         for col in new_df.columns:
#             if not previous_df[col].equals(new_df[col]):
#                 modified_columns.append(col)
#         return modified_columns
#
#     @staticmethod
#     def _process_df_for_unconventional_model(df):
#         return df.melt(var_name=ModelMetadata.EA_PLAY, value_name=ShoojuFields.VAL, ignore_index=False)
#
#     @staticmethod
#     def update_adjustment_series(unconventional_existing_df, new_production_table):
#         adjustment_series_name = ProductionVisualiser.get_adjustment_column(new_production_table)
#         new_adjustment_series = new_production_table[adjustment_series_name]
#
#         unconventional_adjustments = unconventional_existing_df[
#             unconventional_existing_df[ModelMetadata.EA_PLAY] == adjustment_series_name]
#         unconventional_adjustments.loc[:, ModelMetadata.VAL] = new_adjustment_series.loc[
#             unconventional_adjustments.index]
#
#         unconventional_existing_df = unconventional_existing_df.loc[
#             unconventional_existing_df[ModelMetadata.EA_PLAY] != adjustment_series_name]
#         result = pd.concat([unconventional_existing_df, unconventional_adjustments], axis=0)
#         return result
#
#     def recalculate_future_wells_production(self, type_curves: pd.DataFrame, completions_history, completions_forecasts,
#                                             plays_to_recalculate: List[UsPlay] = None):
#
#         future_unconventional = self.unconventional_future_df
#
#         completions = VisualsBuilder(history=completions_history, forecast=completions_forecasts)
#         continuous_completions = completions.make_continuous_df()
#         continuous_completions = continuous_completions.loc[
#             continuous_completions.index >= min(future_unconventional.index)]
#
#         if plays_to_recalculate is not None:
#             continuous_completions = continuous_completions[plays_to_recalculate]
#
#         data = UnconventionalProductionModelData(
#             completions=self._process_df_for_unconventional_model(continuous_completions),
#             type_curves=type_curves
#         )
#         model = UnconventionalProductionModel(data=data)
#         result = model.run()
#         play_level_result = \
#             result.reset_index().groupby([ModelMetadata.DT, ModelMetadata.EA_PLAY, ModelMetadata.ENERGY_PRODUCT])[
#                 ModelMetadata.VAL].sum().reset_index().set_index('dt')
#         pivoted_play_level_production = play_level_result.pivot_table(index=play_level_result.index,
#                                                                       columns=play_level_result.ea_play,
#                                                                       values=ModelMetadata.VAL)
#
#         combined_index = self.unconventional_future_df.index.union(pivoted_play_level_production.index)
#         self.unconventional_future_df = self.unconventional_future_df.reindex(combined_index)
#         for col in pivoted_play_level_production:
#             self.unconventional_future_df[col] = pivoted_play_level_production[col]
#         return self.unconventional_future_df
#
#     def process_and_visualise_data(self):
#         fig = self.make_chart()
#         columns, data,total_columns, total_data = self.make_table_elements()
#         return fig, columns, data,  total_columns, total_data
#
#     def make_table_elements(self):
#         existing_indices = self.unconventional_existing_df.index
#         future_indices = self.unconventional_future_df.index
#         combined_indices = existing_indices.union(future_indices).sort_values()
#         df = pd.DataFrame(index=combined_indices)
#         df = pd.concat([df, self.unconventional_existing_df], axis=1)
#         df = pd.concat([df, self.unconventional_future_df], axis=1)
#         df = df.groupby(level=0, axis=1).sum()
#
#         df['conventional'] = self.continuous_conventional_df.sum(axis=1)
#
#         adjustment_column = self.get_adjustment_column(df)
#         df = pd.concat(
#             [df[adjustment_column], df['conventional'], df.drop(columns=[adjustment_column, 'conventional'])], axis=1)
#
#         total_columns, total_data = VisualsBuilder.make_total_table(df)
#         df.index = df.index.strftime('%Y-%m')
#         df = df.reset_index(names=[ShoojuFields.DT])
#         columns = self._make_columns(df)
#         data = self._make_data(df)
#
#         return columns, data, total_columns, total_data
#
#     @staticmethod
#     def get_adjustment_column(df):
#         adjustment_column = [c for c in df.columns if 'eia_adjustment_series' in c]
#         if len(adjustment_column) != 1:
#             raise ValueError(f"Expected exactly one adjustment column but found {len(adjustment_column)}")
#         return adjustment_column[0]
#
#     @staticmethod
#     def _make_columns(df: pd.DataFrame) -> List[Dict[str, str]]:
#         adjustment_column = ProductionVisualiser.get_adjustment_column(df)
#         cols = []
#
#         for col in df.columns:
#             if col == adjustment_column:
#                 editable = True
#             else:
#                 editable = False
#
#             column_def = {"name": col, "id": col, "editable": editable}
#
#             if pd.api.types.is_numeric_dtype(df[col]):
#                 column_def.update({
#                     "type": "numeric",
#                     "format": Format(group=Group.yes),
#                     "on_change": {"action": "coerce", "failure": "reject"}
#                 })
#
#             cols.append(column_def)
#
#         return cols
#
#     def make_chart(self):
#         fig = go.Figure()
#         colors = VisualSettings().make_rgba_color_iterator(opacity=VisualSettings.STACKED_CHARTS_OPACITY)
#
#         total_df = []
#
#         adjustment_series_name = [c for c in self.unconventional_existing_df if 'adjustment_series' in c]
#         if len(adjustment_series_name) > 0:
#             adjustment_series_name = adjustment_series_name[0]
#             adjustment_series = self.unconventional_existing_df[adjustment_series_name]
#
#             total_df.append(adjustment_series)
#
#             fig.add_trace(
#                 go.Scatter(x=adjustment_series.index,
#                            y=adjustment_series,
#                            name=adjustment_series_name,
#                            mode='lines',
#                            stackgroup='production',
#                            marker_color='black',
#                            line_color='black')
#             )
#
#         color = next(colors)
#         conventional = self.continuous_conventional_df.sum(axis=1)
#         total_df.append(conventional)
#         fig.add_trace(
#             go.Scatter(x=conventional.index,
#                        y=conventional,
#                        name=f'Conventional',
#                        mode='lines',
#                        stackgroup='production',
#                        marker_color=color,
#                        line_color=color)
#         )
#
#         for ea_play in self.unconventional_existing_df.columns:
#             if 'adjustment_series' in ea_play:
#                 continue
#
#             existing = self.unconventional_existing_df[ea_play]
#             total_df.append(existing)
#
#             color = next(colors)
#
#             if ea_play in self.unconventional_future_df.columns:
#                 future = self.unconventional_future_df[ea_play]
#                 total_df.append(future)
#                 combined = existing.add(future, fill_value=0)
#             else:
#                 future = None
#                 combined = existing
#
#             fig.add_trace(
#                 go.Scatter(
#                     x=existing.index,
#                     y=existing,
#                     name=f"{ea_play} existing",
#                     mode="lines",
#                     stackgroup="production",
#                     line=dict(color=color),
#                     legendgroup=ea_play,
#                     hoverinfo="skip",
#                     showlegend=False
#                 )
#             )
#
#             if future is not None:
#                 fig.add_trace(
#                     go.Scatter(
#                         x=future.index,
#                         y=future,
#                         name=f"{ea_play} future",
#                         mode="lines",
#                         stackgroup="production",
#                         line=dict(color=color),
#                         legendgroup=ea_play,
#                         hoverinfo="skip",
#                         showlegend=False
#                     )
#                 )
#
#             fig.add_trace(
#                 go.Scatter(
#                     x=combined.index,
#                     y=combined,
#                     name=ea_play,
#                     mode="lines",
#                     line=dict(width=2, color=color),
#                     legendgroup=ea_play,
#                     showlegend=True,
#                 )
#             )
#
#         total = pd.concat(total_df, axis=1).fillna(0).sum(axis=1)
#         fig = self.add_total(fig, total)
#
#         eia_first_forecast = self.eia_df[ModelMetadata.FIRST_FORECAST_DATE][0]
#         eia_series = self.eia_df[ModelMetadata.VAL]
#
#         previous_psm_forecast = self.previous_psm_series
#         fig = self.add_ea_library_current_snapshot_comparison(fig, previous_psm_forecast)
#
#         if self.last_psm_history_date is not None:
#             fig = self._add_last_psm_history_line(fig=fig, last_psm_history_date=self.last_psm_history_date)
#
#
#         eia_history = eia_series.loc[eia_series.index < eia_first_forecast]
#         eia_forecast = eia_series.loc[eia_series.index >= eia_first_forecast]
#
#         fig.add_trace(
#             go.Scatter(x=eia_history.index,
#                        y=eia_history,
#                        name=f'EIA history',
#                        mode='lines',
#                        legendgroup='eia',
#                        marker_color='black',
#                        line_color='black',
#                        line_width=2
#                        )
#         )
#         fig.add_trace(
#             go.Scatter(x=eia_forecast.index,
#                        y=eia_forecast,
#                        name=f'EIA forecast',
#                        mode='lines',
#                        legendgroup='eia',
#                        marker_color='black',
#                        line_color='black',
#                        line_width=2,
#                        line_dash='dot'
#                        )
#         )
#
#         ea_first_forecast = min(self.unconventional_future_df.index)
#
#         fig = self._add_first_forecast_line(fig, ea_first_forecast)
#         fig.update_layout(VisualSettings().make_base_layout_dict())
#         tickformat = ",.0f"
#
#         e = EnergyProduct()
#
#         if self.energy_product == e.CRUDE_OIL:
#             unit = Unit().BBL_D
#             product_indicator = 'Crude oil'
#         elif self.energy_product == e.NATURAL_GAS:
#             unit = Unit().MCF_D
#             product_indicator = 'Natural gas'
#
#         title = f"{product_indicator} production for {self.eia_basin} in {unit}"
#         fig.update_layout(
#             yaxis=dict(tickformat=tickformat),
#             showlegend=True,
#             title=title,
#             legend=dict(
#                 tracegroupgap=0,
#                 itemsizing='constant',
#                 font=dict(size=12)
#             ),
#             hoverlabel=dict(
#                 namelength=-1,
#                 font=dict(size=12),
#                 bordercolor='black',
#             ),
#         )
#         return fig
#
#     def get_storage_format_future_wells_prod(self):
#         df = self.unconventional_future_df.melt(var_name=ModelMetadata.EA_PLAY, value_name=ShoojuFields.VAL,
#                                                 ignore_index=False)
#         df[ModelMetadata.ENERGY_PRODUCT] = self.energy_product
#         df[ModelMetadata.EIA_BASIN] = self.eia_basin
#         return df
#
#     @staticmethod
#     def make_adjustment_df(existing_unconventional, future_unconventional, continuous_conventional, total_eia) -> pd.DataFrame:
#         existing_unconventional = existing_unconventional.groupby(level=0)[ModelMetadata.VAL].sum()
#         future_unconventional = future_unconventional.groupby(level=0)[ModelMetadata.VAL].sum()
#         continuous_conventional = continuous_conventional.groupby(level=0)[ModelMetadata.VAL].sum()
#         total_eia = total_eia[ModelMetadata.VAL]
#
#         df = pd.DataFrame.from_dict({
#             'conventional': continuous_conventional,
#             'existing_unconventional': existing_unconventional,
#             'future_unconventional': future_unconventional,
#             'eia': total_eia,
#         })
#         df = df.loc[df.index <= max(total_eia.index)]
#         df = df.fillna(0)
#         df['difference'] = df['eia'] - df['existing_unconventional']- df['future_unconventional'] - df['conventional']
#
#         adjustment_series = df['difference']
#         recent_mean = adjustment_series.iloc[-1:].mean()
#
#         adjustment_series = adjustment_series.reindex(existing_unconventional.index, fill_value=None)
#         adjustment_series = adjustment_series.fillna(recent_mean)
#         adjustment_series.rename(ModelMetadata.EIA_ADJUSTMENT_SERIES, inplace=True)
#
#         adjustment_df = adjustment_series.to_frame(name=ModelMetadata.VAL)
#         adjustment_df[ModelMetadata.FIRST_FORECAST_DATE] = max(total_eia.index) + relativedelta(months=1)
#
#         return adjustment_df
