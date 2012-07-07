"""Map URLs to views"""

from werkzeug.routing import Map, Rule


url_map = Map([
    Rule("/", endpoint="index"),
    Rule("/login/", endpoint="login"),
    Rule("/logout/", endpoint="logout"),
    Rule("/newbug/", endpoint="new_bug"),
    Rule("/bug/<int:bugid>/", endpoint="view_bug"),
    Rule("/bugs/", endpoint="list_bugs"),
    Rule("/addcomment/<string:kind>/<int:bugid>/", endpoint="add_comment"),
], redirect_defaults=False)
