import plotly.graph_objects as go
from templates.pages.proper_ea_design.enums import SelectionEnums
from ea_dash_elements.utilities.visual_settings import VisualSettings


def make_chart(operation: SelectionEnums, df):
    if operation == SelectionEnums.MULTIPLY:
        df = df * 1000

    fig = go.Figure()
    chart_settings = VisualSettings()
    colors_iterator = chart_settings.make_color_iterator()

    for col in df.columns:
        # this cycles over the theme colours
        color = next(colors_iterator)

        fig.add_trace(go.Scatter(
            name=col,
            x=df[col].index,
            y=df[col],
            line=dict(color=color),
        ))

    # this applies the standard EA chart layout
    fig.update_layout(chart_settings.make_base_layout_dict())

    # this adds my personal layout preferences
    fig.update_layout(
        yaxis=dict(tickformat=",.0f"),
    )
    return fig
