from dash import html, dcc
import dash_bootstrap_components as dbc
from ea_dash_elements.components.table_card import make_table_card
from ea_dash_elements.components.chart_card import make_chart_card
from templates.pages.proper_ea_design.enums import SelectionEnums
from dash_iconify import DashIconify
import dash_mantine_components as dmc


class ProperDesignLayout:
    def __init__(self, prefix):
        self.prefix = prefix

    def make_layout(self):
        content = [
            self.make_storage(),
            self.make_title(),
            self.make_table_div(),
            self.make_controls(),
            self.make_figure(),
        ]

        # this makes the whole page taking max 50% of the screen space and be centered
        return dbc.Container(content, fluid=True, id=f'{self.prefix}master-container')

    def make_storage(self):
        return dcc.Store(id=f'{self.prefix}storage')

    @staticmethod
    def make_title():
        content = dbc.Row(dbc.Col(html.H1('This is how to properly build a page')), justify="center")
        return content

    def make_table_div(self):
        table_card = make_table_card(
            prefix=self.prefix,
            id_name='top-card',
            title='This table is editable and will affect the chart',
            editable=True,
            source='Energy Aspects'
        )
        content = dbc.Row(dbc.Col(table_card, width=12), justify="center")

        return content

    def make_figure(self):
        chart_card = make_chart_card(
            prefix=self.prefix,
            id_name='bottom-card',
            title='This chart will update if the table is edited',
            source='Energy Aspects'
        )

        content = dbc.Row(dbc.Col(chart_card, width=12), justify="center")
        return content

    def make_controls(self):
        dropdown = dmc.Select(
            id=f"{self.prefix}operation-dropdown",
            data=[SelectionEnums.UNCHANGED, SelectionEnums.MULTIPLY],
            value=SelectionEnums.UNCHANGED,
            clearable=False,
            className="dropdown",
            rightSection=DashIconify(
                icon="radix-icons:triangle-down"),
            searchable=True,
        )

        content = dbc.Row([dbc.Col(dropdown, width=3)], justify='start')

        return content
