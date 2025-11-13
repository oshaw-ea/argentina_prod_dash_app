import dash_bootstrap_components as dbc
from dash import html, page_registry
from ea_dash import EADrawerItem, EADrawerCollapsibleItem
from pages.utilities import PagesNames, PagesOrder


def make_sidenav():
    client_version_box = html.Div('Client version',
                                  className="pr-2 align-items-center d-flex",
                                  style={
                                      'color': 'white',
                                      'border-style': 'solid',
                                      'border-color': '#ac0b3d',
                                      'padding': '5px',
                                      'background-color': '#ac0b3d',
                                      'height': '3em'
                                  },
                                  id='client-version-box',
                                  hidden=True
                                  )
    pages = make_pages_list()

    pages_containers = [
        # make_dashboard_container(pages),
        make_non_dashboard_container(pages),
    ]

    content = [
        # client_version_box,
    ]
    content.extend(pages_containers)

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


# def get_dashboard_pages():
#     dash_pages = [
#         PagesNames.PRODUCTION_DASHBOARD
#     ]
#     return dash_pages


def make_dashboard_container(pages):
#     dashboard_pages_names = get_dashboard_pages()
#     pages = [page for page in pages if page.children.label in dashboard_pages_names]
    item = EADrawerCollapsibleItem(
        pages,
        label="Dashboards",
        className="sidenav__models",

    )
    return item


def make_non_dashboard_container(pages):
    # dashboard_pages_names = get_dashboard_pages()
    # pages = [page for page in pages if page.children.label not in dashboard_pages_names]
    item = EADrawerCollapsibleItem(
        pages,
        label="Engine (BETA)",
        className="sidenav__models",
    )
    return item
