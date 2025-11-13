import warnings
from pathlib import Path
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, ClientsideFunction
from flask import (Flask,
                   jsonify,
                   redirect,
                   session,
                   url_for)

import os
from urllib.parse import urlencode
from auth import requires_auth, authorise_authenticate_dashviews
from authlib.integrations.flask_client import OAuth
from werkzeug.exceptions import HTTPException
import logging
from templates.master_template.master_template import make_master_template
from templates.master_template.sidenav import make_sidenav

warnings.filterwarnings("ignore")

# This is necessary when deploying code to Google App Engine.
# App engine will work off a /workspace source, so we need to figure out
# the path relative to a changing starting environment
for p in Path('.').rglob('*'):
    if str(p).endswith('pages'):
        pages_folder = str(p)
        break

server = Flask(__name__)

dash_app = Dash(
    __name__,
    server=server,
    use_pages=True,
    title='Demo app',
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    pages_folder=pages_folder,
    routes_pathname_prefix='/app/',
    prevent_initial_callbacks='initial_duplicate'
)


def get_secret_key():
    secret_key = os.getenv('SERVER_SECRET_KEY', None)
    if secret_key is None:
        logging.log(logging.WARNING, 'There is no SERVER_SECRET_KEY set in the environment variables, you can run local but do not deploy this without a real key in Doppler')
        secret_key = 'NotSoSecretKeyNowIsIt?'
    return secret_key


server.secret_key = get_secret_key()

dash_app.layout = make_master_template()

##############################################################################################
############ authentication and security boilerplate, will be used for deployment ############
##############################################################################################

#
# # Add a clientside callback to identify users
# dash_app.clientside_callback(
#     ClientsideFunction(
#         namespace='clientside',
#         function_name='identifyUser'
#     ),
#     output=Output('segment-tracking', 'children', allow_duplicate=True),
#     inputs=[Input('user-info-store', 'data')]
# )
#
# # Add a clientside callback to track page views
# dash_app.clientside_callback(
#     ClientsideFunction(
#         namespace='clientside',
#         function_name='trackPageView'
#     ),
#     output=Output('segment-tracking', 'children', allow_duplicate=True),
#     inputs=[Input('url', 'pathname')]
# )
#
# #  Set up authorization in the Dash app
# authorise_authenticate_dashviews(dash_app)
#
# oauth = OAuth(server)
# CLOUD_AUTH0_CALLBACK_URL = os.environ.get('CLOUD_AUTH0_CALLBACK_URL')
# AUTH0_CALLBACK_URL = CLOUD_AUTH0_CALLBACK_URL if CLOUD_AUTH0_CALLBACK_URL else os.environ.get(
#     'AUTH0_CALLBACK_URL')
# AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
# AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
# AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
# AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
# AUTH0_AUDIENCE = os.environ.get('AUTH0_AUDIENCE')
# auth0 = oauth.register(
#     'auth0',
#     client_id=AUTH0_CLIENT_ID,
#     client_secret=AUTH0_CLIENT_SECRET,
#     api_base_url=AUTH0_BASE_URL,
#     access_token_url=AUTH0_BASE_URL + '/oauth/token',
#     authorize_url=AUTH0_BASE_URL + '/authorize',
#     server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
#     client_kwargs={
#         'scope': 'openid profile email',
#     },
# )
#
#
# @server.errorhandler(Exception)
# def handle_auth_error(ex):
#     response = jsonify(message=str(ex))
#     response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
#     return response
#
#
# @server.route('/callback')
# def callback_handling():
#     session.permanent = False
#     auth0.authorize_access_token()
#     resp = auth0.get('userinfo')
#     userinfo = resp.json()
#     session['jwt_payload'] = userinfo
#     try:
#         session['profile'] = {
#             'user_id': userinfo['sub'],
#             'sf_contact_id': userinfo['https://energyaspects.com/sf_contact_id'],
#             'sf_account_id': userinfo['https://energyaspects.com/sf_account_id'],
#             'activated': userinfo['https://energyaspects.com/activated'],
#             'name': userinfo['name'],
#             'first_name': userinfo.get('given_name'),
#             'last_name': userinfo.get('family_name'),
#             'nickname': userinfo.get('nickname'),
#             'picture': userinfo.get('picture'),
#             'updated_at': userinfo['updated_at'],
#             'entitlements': userinfo['https://energyaspects.com/entitlements'],
#             'ad_groups': userinfo['https://energyaspects.com/claims/groups'],
#             'roles': userinfo['https://energyaspects.com/roles']
#         }
#     except KeyError:
#         user_id = userinfo['sub']
#         print(f'profile data for {user_id} is not complete')
#         redirect('/logout')
#     print('redirecting now to homepage')
#     return redirect('/app/')
#
#
# @server.route('/login')
# def login():
#     return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)
#
#
# @server.route('/logged-out')
# def goodbye():
#     return redirect('/login')
#
#
# @server.route('/logout')
# def logout():
#     session.clear()
#     params = {
#         'returnTo': url_for('goodbye', _external=True),
#         'client_id': AUTH0_CLIENT_ID
#     }
#     return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
#
#
# @server.route('/')
# @requires_auth
# def root():
#     return redirect('/app/')
#
#
# @server.route('/404')
# def not_found():
#     return "You are not licensed to access this application " \
#            "- please contact sales@energyaspects.com or your Account Manager!"

@callback(
    Output('layoutEA', 'leftDrawerContent'),
    Output('layoutEA', 'firstName'),
    Output('layoutEA', 'lastName'),
    Input('user-info-store', 'data'),
)
def drawer(user_info):
    # in the real world you would get that from Session which you get with authentication
    name = 'John'
    surname = 'Smith'
    drawer = make_sidenav()
    return drawer, name, surname



if __name__ == '__main__':
    dash_app.run_server(debug=True,
                        port=8000,
                        dev_tools_hot_reload=True,  # this controls reloading the app when source is edited
                        use_reloader=False,
                        # if False 30s timeouts on requests will be removed. Useful when using breakpoints to code,
                        )
