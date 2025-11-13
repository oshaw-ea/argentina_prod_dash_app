from functools import wraps
from flask import session
from werkzeug.utils import redirect
from datetime import datetime, timezone
from pandas import to_datetime

dt_now = datetime.now()
dt_now = dt_now.replace(tzinfo=timezone.utc)


def requires_auth(f):
    """Checks Flask session for "profile" establishing a valid Auth0 login"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


def requires_entitlement(f, expected_entitlements):
    """Extends requires_auth(), checks a list of expected entitlements against a user's own entitlements"""
    @wraps(f)
    def decorated(*args, **kwargs):
        user_entitlements = session.get('profile').get('entitlements')
        filtered_entitlements = list(filter(lambda d: d['id'] in expected_entitlements, user_entitlements))
        if len(filtered_entitlements) == 0:
            return redirect('/404')
        if len(filtered_entitlements) >= 1:
            for x in filtered_entitlements:
                if x['active']:
                    break
            else:
                return redirect('/404')
        return f(*args, **kwargs)
    return decorated


def requires_ad_group(ad_group):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            profile = session.get('profile')
            if ad_group not in profile['ad_groups']:
                return redirect('/404')
            return f(*args, **kwargs)
        return wrapper
    return decorator


def authorise_authenticate_dashviews(dash_app):
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = \
                requires_auth(dash_app.server.view_functions[view_func])


