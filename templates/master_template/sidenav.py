import dash_bootstrap_components as dbc
from dash import html, page_registry
from ea_dash import EADrawerItem, EADrawerCollapsibleItem
from pages.utilities.pages_utilities import PagesOrder, PagesNames


def make_sidenav():
    pages = make_pages_list()

    content = [
        make_intro_pages(pages),
        make_advanced_pages(pages),
    ]
    return html.Div(content, className="sidenav")


def make_pages_list():
    pages = []
    for page in page_registry.values():
        pages.append(
            dbc.NavLink(
                EADrawerItem(
                    label=page["name"],
                    disabled=page.get("disabled", False),
                ),
                href=page["relative_path"],
                active="exact",
                disabled=page.get("disabled", False),
            )
        )
    return pages


def get_intro_pages():
    dash_pages = [
        PagesNames.HOME,
        PagesNames.SIMPLE_PAGE,
    ]
    return dash_pages


def make_intro_pages(pages):
    dashboard_pages_names = get_intro_pages()
    pages = [page for page in pages if page.children.label in dashboard_pages_names]
    item = EADrawerCollapsibleItem(
        pages,
        label="Intro pages",
        className="sidenav__models",

    )
    return item


def make_advanced_pages(pages):
    intro_pages = get_intro_pages()
    pages = [page for page in pages if page.children.label not in intro_pages]
    item = EADrawerCollapsibleItem(
        pages,
        label="Advanced pages",
        className="sidenav__models",
    )
    return item
