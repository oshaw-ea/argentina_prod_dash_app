from dash import callback, Output, Input
from templates.pages.proper_ea_design.chart_maker import make_chart
import pandas as pd
from templates.pages.proper_ea_design.enums import SelectionEnums
from templates.pages.proper_ea_design.dummy_data import make_dummy_data


def define_charts_callbacks(prefix):
    @callback(
        Output(f'{prefix}storage', 'data'),
        Input(f'{prefix}master-container', 'children'),
    )
    def load_data(trigger):
        df = make_dummy_data()
        return df.reset_index().to_dict('records')

    @callback(
        Output(f'{prefix}top-card-table', 'columns'),
        Output(f'{prefix}top-card-table', 'data'),
        Input(f'{prefix}storage', 'data'),
    )
    def load_data_in_table(data):
        df = pd.DataFrame(data)
        return [{'name': i, 'id': i} for i in df.columns], df.to_dict('records')

    @callback(
        Output(f'{prefix}bottom-card-graph', 'figure'),
        Input(f'{prefix}operation-dropdown', 'value'),
        Input(f'{prefix}top-card-table', 'data'),
    )
    def update_chart(operation: SelectionEnums, data):
        df = pd.DataFrame(data).set_index('index')
        # minimal logic in callback
        # we abstract the logic away, to keep this clean and readable
        return make_chart(operation, df)
