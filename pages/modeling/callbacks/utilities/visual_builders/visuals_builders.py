import pandas as pd
from dash.dash_table.Format import Format, Group
from dateutil.relativedelta import relativedelta
from helper_functions_ea import ShoojuTools
from argentina_prod.configs.enums import ModelMetadata, ShoojuFields
from typing import Union, List, Dict, Tuple, Optional, Any
import plotly.graph_objects as go
# from argentina_prod.utilities.locations_mapping import LocationsMapping

from ea_dash_elements.utilities.visual_settings import VisualSettings
from pages.utilities import ChartTitles
from datetime import datetime, timezone


class DataTypes:
    AREA_LEVEL = 'area_level'


class VisualsBuilder:

    def __init__(self, history: Union[pd.Series, pd.DataFrame, None], forecast: pd.DataFrame = None):
        self.history = history
        if forecast is not None and not self.history.empty:
            forecast = forecast.loc[forecast.index > max(history.index)]
        self.forecast = forecast

    @staticmethod
    def process_data(df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        if df is not None:
            if data_type == DataTypes.AREA_LEVEL:
                df = df[[ModelMetadata.AREA, ShoojuFields.VAL]].pivot_table(index=df.index,
                                                                               columns=ModelMetadata.AREA,
                                                                               values=ShoojuFields.VAL)
        return df

    def make_table_elements(self) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]]]:
        df = self.forecast.copy()
        df = df.round()
        df = df.reset_index()
        df[ShoojuFields.DT] = df[ShoojuFields.DT].dt.strftime('%Y-%m')

        columns = self._make_columns(df)
        data = self._make_data(df)
        return columns, data

    @staticmethod
    def make_total_table(df: pd.DataFrame) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        total_df = df.copy().sum(axis=1).to_frame("Total")

        columns = VisualsBuilder._make_columns(total_df)
        data = VisualsBuilder._make_data(total_df)

        return columns, data

    @staticmethod
    def update_play_level_data_from_totals(new_total_data, old_total_data, play_level_data):
        result = play_level_data.copy()
        play_columns = play_level_data.columns.tolist()

        new_totals = pd.Series(new_total_data['Total'])
        old_totals = pd.Series(old_total_data['Total'])

        delta = new_totals - old_totals
        rows_to_update = delta.abs() >= 1e-6

        if not rows_to_update.any():
            return result

        for idx in rows_to_update.index[rows_to_update]:
            timestamp = result.index[idx]
            row_values = result.loc[timestamp, play_columns].astype(float)
            row_sum = row_values.sum()

            if row_sum == 0:
                continue

            new_total = new_totals.loc[idx]
            scaling_factor = new_total / row_sum
            scaled_values = row_values * scaling_factor
            rounded = scaled_values.round()

            discrepancy = int(round(new_total - rounded.sum()))
            if discrepancy != 0:
                largest_play = row_values.idxmax()
                rounded[largest_play] += discrepancy

            result.loc[timestamp, play_columns] = rounded.astype(int)

        return result

    @staticmethod
    def _make_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
        return df.to_dict('records')

    @staticmethod
    def _make_columns(df: pd.DataFrame) -> List[Dict[str, str]]:
        columns = []
        for i in df.columns:
            column_def = {"name": i, "id": i}

            if pd.api.types.is_numeric_dtype(df[i]):
                column_def.update({
                    "type": "numeric",
                    "format": Format(group=Group.yes),
                    "on_change": {"action": "coerce", "failure": "reject"}
                })

            columns.append(column_def)

        return columns

    def make_continuous_df(self) -> pd.DataFrame:
        df = pd.concat([self.history, self.forecast], axis=0)
        df = df[~df.index.duplicated(keep='first')]
        if self.forecast is not None and not self.forecast.empty:
            target_index = min(self.forecast.index)
        else:
            target_index = max(self.history.index)

        sorted_names = df.loc[target_index, :].sort_values(ascending=False).index
        return df[sorted_names]

    def make_chart(self, stacked: bool, title: ChartTitles) -> go.Figure:

        fig = go.Figure()
        colors = VisualSettings().make_rgba_color_iterator(opacity=VisualSettings.STACKED_CHARTS_OPACITY)

        df = self.make_continuous_df()
        for play in df.columns:
            color = next(colors)

            params = dict(
                name=play,
                x=df[play].index,
                y=df[play],
                mode='lines',
                line=dict(color=color),
            )
            if stacked:
                params.update(
                    stackgroup='one'
                )

            fig.add_trace(go.Scatter(**params))

        all_totals = df.sum(axis=1)
        fig = self.add_total(fig, all_totals)

        base_layout = VisualSettings().make_base_layout_dict()
        base_layout["hovermode"] = "x unified"
        fig.update_layout(base_layout)
        tickformat = ",.0f"

        fig.update_layout(
            yaxis=dict(tickformat=tickformat),
            showlegend=True,
            title=title
        )
        return fig

    @staticmethod
    def add_total(fig, total):
        fig.add_trace(
            go.Scatter(
                x=total.index,
                y=total,
                name='Total',
                mode='lines',
                marker_color='red',
                line_color='red',
                line_width=2
            )
        )
        return fig

    @staticmethod
    def add_snapshot(fig, snapshot_series: pd.Series):
        fig.add_trace(
            go.Scatter(
                x=snapshot_series.index,
                y=snapshot_series,
                name='Current Snapshot',
                mode='lines',
                marker_color='blue',
                line_color='blue',
                line_width=2,
            )
        )
        return fig

    @staticmethod
    def add_ea_library_current_snapshot_comparison(fig, previous_psm_series: pd.Series):
        fig.add_trace(
            go.Scatter(
                x=previous_psm_series.index,
                y=previous_psm_series,
                name='Current Snapshot',
                mode='lines',
                marker_color='blue',
                line_color='blue',
                line_width=2,
            )
        )
        return fig

    @staticmethod
    def _add_first_forecast_line(fig: go.Figure, first_forecast_date: pd.Timestamp) -> go.Figure:
        fig.add_vline(x=first_forecast_date, line_width=2,
                      line_dash="dash", line_color=VisualSettings.FIRST_FORECAST_LINE_COLOR)
        fig.add_annotation(
            x=first_forecast_date,
            y=1,
            text='First forecast month',
            showarrow=False,
            font=dict(color=VisualSettings.FIRST_FORECAST_LINE_COLOR, size=12),
            xanchor="left",
            yanchor="bottom",
            textangle=-30,
            yref='paper'
        )
        return fig

    @staticmethod
    def _add_nowcasting_line(fig: go.Figure, nowcasting_date: pd.Timestamp) -> go.Figure:
        fig.add_vline(x=nowcasting_date, line_width=2,
                      line_dash="dash", line_color=VisualSettings.EA_RED)
        fig.add_annotation(
            x=nowcasting_date,
            y=0.7,
            text='Nowcasting start',
            showarrow=False,
            font=dict(color="purple", size=12),
            xanchor="left",
            yanchor="bottom",
            textangle=-30,
            yref='paper'
        )
        return fig

    def _add_zoom(self, fig: go.Figure, xaxis_range: Optional[List[pd.Timestamp]] = None) -> go.Figure:
        if xaxis_range is None:
            if self.forecast is not None:
                max_range = max(self.forecast.index)
                min_range = min(self.forecast.index) - relativedelta(months=12)
            else:
                max_range = max(self.history.index)
                min_range = min(self.history.index) - relativedelta(months=12)
            xaxis_range = [min_range, max_range]

        fig.update_xaxes(rangeslider_visible=True)
        fig.update_xaxes(tickmode="auto", showticklabels=True)
        fig.update_yaxes(tickmode="auto", showticklabels=True)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(xaxis_range=xaxis_range)
        return fig

    @staticmethod
    def visualise_data(history_df: pd.DataFrame,
                       forecast_df: pd.DataFrame,
                       title: ChartTitles,
                       stacked: bool = True,
                       ) -> Tuple[List[Dict[str, str]], List[Dict[str, Any]], go.Figure]:
        visuals_builder = VisualsBuilder(history=history_df, forecast=forecast_df)
        columns, data = visuals_builder.make_table_elements()
        fig = visuals_builder.make_chart(stacked=stacked, title=title)

        return columns, data, fig

    @staticmethod
    def process_and_visualise_data(history_df: pd.DataFrame,
                                   forecast_df: pd.DataFrame,
                                   title: ChartTitles,
                                   history_data_type: str = DataTypes.AREA_LEVEL,
                                   stacked: bool = True) -> Tuple[
        pd.DataFrame, pd.DataFrame, List[Dict[str, str]], List[Dict[str, Any]], go.Figure]:
        if not history_df.empty:
            history_df = VisualsBuilder.process_data(df=history_df, data_type=history_data_type)
        if not forecast_df.empty:
            forecast_df = VisualsBuilder.process_data(df=forecast_df, data_type=DataTypes.AREA_LEVEL)

        columns, data, fig = VisualsBuilder.visualise_data(
            history_df=history_df,
            forecast_df=forecast_df,
            stacked=stacked,
            title=title
        )

        return history_df, forecast_df, columns, data, fig

    @staticmethod
    def create_empty_figure(title: str,
                            y_label: str = "Count") -> go.Figure:
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title=y_label,
            template="plotly_white"
        )
        return fig

    @staticmethod
    def round_up_on_half(df: Union[pd.DataFrame, pd.Series], decimals=0):
        """ This function is necessary, as other round functions use banker's rounding, which would round 0.5 down to 0"""
        factor = 10 ** decimals
        return (df * factor + 0.5).floordiv(1).div(factor)

    @staticmethod
    def add_secondary_axis_line(fig, series, name='Secondary Series', line_color='black',
                                line_width=2, dash=None, show_axis=False, tickformat=None, hover_template=None):
        if hover_template:
            hover_template = hover_template.replace('<name>', name)
        fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series,
                name=name,
                mode='lines',
                line=dict(
                    color=line_color,
                    width=line_width,
                    dash=dash
                ),
                yaxis="y2",
                hovertemplate=hover_template
            )
        )

        layout_updates = {
            "yaxis2": {
                "title": None,
                "showticklabels": show_axis,
                "side": "right",
                "overlaying": "y",
                "showgrid": False,
                "zeroline": False
            }
        }

        if tickformat and show_axis:
            layout_updates["yaxis2"]["tickformat"] = tickformat

        fig.update_layout(layout_updates)

        return fig
