# from argentina_prod.configs.enums import ModelMetadata, TypeCurveMetadata
# from argentina_prod.models.type_curves.type_curve import TypeCurve
# from plotly import graph_objects as go
# import pandas as pd
# from typing import List
#
#
# def populate_existing_table(available_type_curves, selected_plays, selected_vintages):
#     table_data = []
#     for play in selected_plays:
#         for vintage in selected_vintages:
#             mask = (
#                     (available_type_curves[ModelMetadata.EA_PLAY] == play) &
#                     (available_type_curves[ModelMetadata.VINTAGE] == vintage)
#             )
#             type_curves = available_type_curves[mask]
#
#             if not type_curves.empty:
#                 for _, type_curve_characteristics in type_curves.iterrows():
#                     row = {
#                         "select": False,
#                         ModelMetadata.ENERGY_PRODUCT: type_curve_characteristics[ModelMetadata.ENERGY_PRODUCT],
#                         ModelMetadata.EA_PLAY: type_curve_characteristics[ModelMetadata.EA_PLAY],
#                         ModelMetadata.VINTAGE: type_curve_characteristics[ModelMetadata.VINTAGE],
#                         TypeCurveMetadata.QI: round(float(type_curve_characteristics[TypeCurveMetadata.QI]), 4),
#                         TypeCurveMetadata.B: round(float(type_curve_characteristics[TypeCurveMetadata.B]), 4),
#                         TypeCurveMetadata.DI: round(float(type_curve_characteristics[TypeCurveMetadata.DI]), 4),
#                         TypeCurveMetadata.TYPE_CURVE_TYPE: f"Existing {type_curve_characteristics[TypeCurveMetadata.TYPE_CURVE_TYPE]}",
#                         TypeCurveMetadata.LATERAL_LENGTH: type_curve_characteristics[TypeCurveMetadata.LATERAL_LENGTH],
#                         TypeCurveMetadata.FIRST_COMPLETION_STAGES: type_curve_characteristics[TypeCurveMetadata.FIRST_COMPLETION_STAGES],
#                         TypeCurveMetadata.FIRST_COMPLETION_PROPPANT_MASS: type_curve_characteristics[TypeCurveMetadata.FIRST_COMPLETION_PROPPANT_MASS],
#                         TypeCurveMetadata.FIRST_COMPLETION_FLUID_VOLUME: type_curve_characteristics[TypeCurveMetadata.FIRST_COMPLETION_FLUID_VOLUME],
#                         TypeCurveMetadata.FIRST_90_DAYS_PRODUCTION: type_curve_characteristics[TypeCurveMetadata.FIRST_90_DAYS_PRODUCTION],
#                         TypeCurveMetadata.FIRST_180_DAYS_PRODUCTION: type_curve_characteristics[TypeCurveMetadata.FIRST_180_DAYS_PRODUCTION],
#                         TypeCurveMetadata.FIRST_365_DAYS_PRODUCTION: type_curve_characteristics[TypeCurveMetadata.FIRST_365_DAYS_PRODUCTION],
#                         TypeCurveMetadata.EUR: type_curve_characteristics[TypeCurveMetadata.EUR]
#                     }
#                     table_data.append(row)
#
#     return table_data
#
# def populate_graph(table_data, existing_figure=None):
#     if existing_figure is None:
#         fig = go.Figure()
#     else:
#         fig = existing_figure
#
#     for row in table_data:
#         type_curve = TypeCurve.from_characteristics(
#             vintage=row[ModelMetadata.VINTAGE],
#             energy_product=row[ModelMetadata.ENERGY_PRODUCT],
#             ea_play=row[ModelMetadata.EA_PLAY],
#             qi=float(row[TypeCurveMetadata.QI]),
#             b=float(row[TypeCurveMetadata.B]),
#             di=float(row[TypeCurveMetadata.DI])
#         )
#
#         curve_name = f"{row[ModelMetadata.EA_PLAY]} - {row[ModelMetadata.VINTAGE]} - {row[TypeCurveMetadata.TYPE_CURVE_TYPE]}"
#         fig.add_trace(go.Scatter(
#             x=list(range(len(type_curve.time_series))),
#             y=type_curve.time_series,
#             name=curve_name,
#             line=dict(dash=None if existing_figure is None else 'dash',
#                       width=3)
#         ))
#
#     fig.update_layout(
#         title="Type Curves Comparison",
#         xaxis_title="Months",
#         yaxis_title="Production",
#         template="plotly_white",
#         showlegend=True,
#         legend=dict(
#             yanchor="top",
#             y=0.99,
#             xanchor="right",
#             x=1
#         )
#     )
#
#     fig.update_layout(
#         xaxis=dict(
#             range=[0, 60],
#             rangeslider=dict(visible=True),
#             tickmode="auto",
#             showticklabels=True
#         ),
#         yaxis=dict(
#             tickmode="auto",
#             showticklabels=True,
#             fixedrange=False
#         )
#     )
#
#     return fig
#
# def update_table_data_from_selected_table_data(selected_table_data, existing_table_data):
#     new_parameter_data = existing_table_data.copy()
#     for row in selected_table_data:
#         play = row[ModelMetadata.EA_PLAY]
#         vintage = row[ModelMetadata.VINTAGE]
#         type_curve_type = f"Existing {TypeCurveMetadata.OVERRIDE}"
#
#         for i, existing_row in enumerate(new_parameter_data):
#             if (existing_row[ModelMetadata.EA_PLAY] == play and
#                     existing_row[ModelMetadata.VINTAGE] == vintage):
#                 new_parameter_data[i] = {
#                     **row,
#                     'select': False,
#                     TypeCurveMetadata.TYPE_CURVE_TYPE: type_curve_type
#                 }
#                 break
#
#     return new_parameter_data
#
# def update_available_type_curves_from_table_data(updated_table_data, existing_available_type_curves):
#     new_available_type_curves = existing_available_type_curves.copy()
#     for row in updated_table_data:
#         replacement_row = row.copy()
#         replacement_row[TypeCurveMetadata.TYPE_CURVE_TYPE] = TypeCurveMetadata.OVERRIDE
#         eia_basin = existing_available_type_curves[
#             existing_available_type_curves[ModelMetadata.EA_PLAY] == replacement_row[ModelMetadata.EA_PLAY]][
#             ModelMetadata.EIA_BASIN][0]
#         replacement_row[ModelMetadata.EIA_BASIN] = eia_basin
#
#         mask = (
#                 (new_available_type_curves[ModelMetadata.EA_PLAY] == row[ModelMetadata.EA_PLAY]) &
#                 (new_available_type_curves[ModelMetadata.VINTAGE] == row[ModelMetadata.VINTAGE]) &
#                 (new_available_type_curves[TypeCurveMetadata.TYPE_CURVE_TYPE] == TypeCurveMetadata.OVERRIDE)
#         )
#         if len(new_available_type_curves[mask]) == 1:
#             shared_columns = set(replacement_row.keys()).intersection(set(new_available_type_curves.columns))
#             for column in shared_columns:
#                 new_available_type_curves.loc[mask, column] = replacement_row[column]
#         elif len(new_available_type_curves[mask]) == 0:
#             new_row = {col: replacement_row[col]
#                                        for col in new_available_type_curves.columns
#                                        if col in replacement_row}
#             new_row = pd.DataFrame([new_row])
#             new_row[ModelMetadata.DT] = pd.Timestamp(year=replacement_row[ModelMetadata.VINTAGE], month=1, day=1)
#             new_row = new_row.set_index(ModelMetadata.DT)
#             new_row[ModelMetadata.EIA_BASIN] = eia_basin
#
#             if len(new_available_type_curves.columns) != len(new_row.columns):
#                 raise ValueError(f"New available type curves has {new_available_type_curves.columns} columns and new row has {new_row.columns} columns")
#             new_available_type_curves = pd.concat([new_available_type_curves, new_row])
#         else:
#             raise ValueError("Multiple overrides for the same play and vintage in available type curves df")
#
#
#     return new_available_type_curves
#
#
# def update_type_curve_metrics_from_parameter_table_data(parameter_table_data):
#     updated_parameter_table_data = parameter_table_data.copy()
#     for i, type_curve in enumerate(parameter_table_data):
#         time_series = TypeCurve.make_type_curve_time_series(qi=type_curve[TypeCurveMetadata.QI], b=type_curve[TypeCurveMetadata.B], di=type_curve[TypeCurveMetadata.DI])
#         calculated_metrics = TypeCurve.calculate_metrics(time_series)
#
#         updated_parameter_table_data[i][TypeCurveMetadata.FIRST_90_DAYS_PRODUCTION] = calculated_metrics[TypeCurveMetadata.FIRST_90_DAYS_PRODUCTION]
#         updated_parameter_table_data[i][TypeCurveMetadata.FIRST_180_DAYS_PRODUCTION] = calculated_metrics[
#             TypeCurveMetadata.FIRST_180_DAYS_PRODUCTION]
#         updated_parameter_table_data[i][TypeCurveMetadata.FIRST_365_DAYS_PRODUCTION] = calculated_metrics[
#             TypeCurveMetadata.FIRST_365_DAYS_PRODUCTION]
#         updated_parameter_table_data[i][TypeCurveMetadata.EUR] = calculated_metrics[
#             TypeCurveMetadata.EUR]
#
#     return updated_parameter_table_data
#
#
# def create_new_available_type_curves_from_selected_table_data(selected_parameter_data, existing_available_type_curves):
#     new_available_type_curves = existing_available_type_curves.copy()
#     if not selected_parameter_data:
#         return new_available_type_curves
#
#     new_rows = []
#
#     for row in selected_parameter_data:
#         new_row = row.copy()
#
#         new_row[TypeCurveMetadata.TYPE_CURVE_TYPE] = TypeCurveMetadata.OVERRIDE
#         new_row[ModelMetadata.EIA_BASIN] = existing_available_type_curves[existing_available_type_curves[ModelMetadata.EA_PLAY]==new_row[ModelMetadata.EA_PLAY]][ModelMetadata.EIA_BASIN][0]
#
#         shared_columns = set(new_row.keys()).intersection(set(new_available_type_curves.columns))
#         filtered_row = {col: new_row[col] for col in shared_columns}
#
#         filtered_row[ModelMetadata.DT] = pd.Timestamp(year=new_row[ModelMetadata.VINTAGE], month=1, day=1)
#
#         new_rows.append(filtered_row)
#
#     if new_rows:
#         new_rows_df = pd.DataFrame(new_rows)
#         new_rows_df.set_index(ModelMetadata.DT, inplace=True)
#
#         new_available_type_curves = pd.concat([new_available_type_curves, new_rows_df])
#
#     return new_available_type_curves
#
#
# def get_vintages_in_forecasting_period(completions_forecast) -> List[int]:
#     forecast_index = completions_forecast.index
#     forecast_index_years = forecast_index.year
#
#     sorted_years = sorted(set(forecast_index_years))
#
#     return sorted_years