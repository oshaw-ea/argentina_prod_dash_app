import dash_bootstrap_components as dbc
from ea_dash_elements.utilities.enums import AggregationType
from dash_iconify import DashIconify
import dash_mantine_components as dmc
from dash import html


def make_filter_row(prefix: str,
                    id_name: str,
                    ):
    aggregation_options = [{'label': 'Total', 'value': 1}]
    aggregation_options.extend([{'label': f'{str(i - 1)} series', 'value': i} for i in range(2, 7)])
    for i in [11, 16, 21]:
        aggregation_options.extend(
            [
                {'label': f'{str(i - 1)} series', 'value': i}
            ]
        )

    content = dbc.Row([
        dbc.Col(dbc.Button('Filter', id=f'{prefix}{id_name}-filters-button', className='mx-2',
                           color='dark', style={'width': '100%'})),
        dbc.Col(
            dmc.Select(
                id=f"{prefix}{id_name}-aggregation-dropdown",
                data=[AggregationType.AGGREGATED, AggregationType.DETAILED],
                value=AggregationType.AGGREGATED,
                clearable=False,
                className="dropdown",
                rightSection=DashIconify(
                    icon="radix-icons:triangle-down"),
                searchable=True,

            )
        ),

        dbc.Col(
            html.Div(id=f'{prefix}{id_name}-aggregation-number-container', children=[
                dmc.Select(
                    id=f"{prefix}{id_name}-aggregation-number",
                    data=aggregation_options,
                    value=6,
                    clearable=False,
                    className="dropdown",
                    rightSection=DashIconify(
                        icon="radix-icons:triangle-down"),
                    searchable=True,

                ),
            ]),
        )
    ], justify='start', align='center')
    return content
