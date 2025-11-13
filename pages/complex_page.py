from dash import Output, Input, State, html, callback, register_page, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from pages.utilities.pages_utilities import PagesOrder, PagesNames
from ea_dash_elements.components.chart_card import make_chart_card
from ea_dash_elements.components.table_card import make_table_card
from ea_dash_elements.utilities.visual_settings import VisualSettings

# This is needed to add the page to navigation
# You can remove order if you don't care about page ordering in navbar
register_page(
    __name__,
    path='/complex_page',
    title=PagesNames.COMPLEX_PAGE,
    name=PagesNames.COMPLEX_PAGE,
    order=PagesOrder.COMPLEX_PAGE
)

prefix = 'complex-'


# the page needs to contain either a function called layout returning the layout or a layout object
def layout():
    # store data in local cache
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
    storage = dcc.Store(id='df-storage', storage_type='memory', data=df.to_dict(orient='records')),

    # create page elements
    slider = dcc.RangeSlider(df['year'].min(), df['year'].max(), step=None, value=[df['year'].min(), df['year'].max()],
                             marks={str(year): str(year) for year in df['year'].unique()}, id='year-slider')
    graph = make_chart_card(
        prefix=prefix,
        id_name='card-1',
        title='Complex page chart',
        source='Energy Aspects'
    )
    table = make_table_card(
        prefix=prefix,
        id_name='card-2',
        title='Complex page table',
        source='Energy Aspects'
    )

    # add elements to layout
    layout = dbc.Container([
        dbc.Row(dbc.Col(storage)),
        dbc.Row(dbc.Col(html.Div(children=[graph, slider]), width=12), justify="center"),
        dbc.Row(dbc.Col(html.Div(children=[table]), width=10), justify="center"),
    ], fluid=True
    )
    return layout


@callback(
    Output(f'{prefix}card-1-graph', 'figure'),
    Output(f'{prefix}card-2-table', 'columns'),
    Output(f'{prefix}card-2-table', 'data'),
    Input('year-slider', 'value'),
    State('df-storage', 'data'),
)
def update_figures(selected_years, df_json):
    # read cached data
    df = pd.DataFrame(df_json)
    filtered_df = df[(df.year >= selected_years[0]) & (df.year <= selected_years[1])]

    # make figure
    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)
    fig.update_layout(
        VisualSettings().make_base_layout_dict()
    )
    fig.update_layout(transition_duration=500)

    # make table
    columns = [{"name": i, "id": i} for i in filtered_df.columns]
    data = filtered_df.to_dict('records')

    return fig, columns, data
