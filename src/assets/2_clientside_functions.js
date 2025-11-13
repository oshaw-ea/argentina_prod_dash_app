document.addEventListener('DOMContentLoaded', function() {
    window.dash_clientside = Object.assign({}, window.dash_clientside, {
        clientside: {
            trackPageView: function(pathname) {
                if (typeof analytics !== 'undefined' && analytics !== null) {
                    analytics.page(pathname);
                }
                return '';
            },
            identifyUser: function(userData) {
                if (typeof analytics !== 'undefined' && analytics !== null && userData) {
                    analytics.identify(userData.user_id, {
                        name: userData.name
                    });
                }
                return '';
            }
        }
    });
});