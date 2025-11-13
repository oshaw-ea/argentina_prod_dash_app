from datetime import datetime
from plotly import graph_objects as go
from ea_dash_elements.utilities.visual_settings import VisualSettings


def add_vertical_line(fig: go.Figure, timestamp: datetime, label: str = "First forecast month"):

    fig.add_vline(x=timestamp, line_width=2,
                  line_dash="dash", line_color="#85888a")
    fig.add_annotation(
        x=timestamp,
        y=0.8,
        text=label,
        showarrow=False,
        font=dict(color=VisualSettings.FIRST_FORECAST_LINE_COLOR, size=12),
        xanchor="left",
        yanchor="bottom",
        textangle=-30,
        yref='paper'
    )
