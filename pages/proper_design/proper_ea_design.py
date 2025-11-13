from dash import register_page
from templates.pages.proper_ea_design.main_page import ProperDesignLayout
from pages.utilities.pages_utilities import PagesOrder, PagesNames
from pages.proper_design.callbacks.chart_table_callbacks import define_charts_callbacks

# This is needed to add the page to navigation
# You can remove order if you don't care about page ordering in navbar

register_page(
    __name__,
    path='/proper_design',
    title=PagesNames.PROPER_DESIGN,
    name=PagesNames.PROPER_DESIGN,
    order=PagesOrder.PROPER_DESIGN
)

prefix = 'proper-design-'


def layout():
    return ProperDesignLayout(prefix).make_layout()


define_charts_callbacks(prefix)
