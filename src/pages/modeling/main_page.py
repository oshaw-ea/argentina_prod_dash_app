from dash import register_page
from pages.utilities import PagesNames, PagesOrder, PagesPrefix
from templates.modeling.master_template import MasterTemplate
from pages.modeling.callbacks.modeling_callbacks import define_modeling_callbacks

register_page(
    __name__,
    path='/',
    title=PagesNames.MODELING,
    name=PagesNames.MODELING,
    order=PagesOrder.MODELING,
)

def layout():
    return MasterTemplate(PagesPrefix.MODELING).make_template()

define_modeling_callbacks(prefix=PagesPrefix.MODELING)


