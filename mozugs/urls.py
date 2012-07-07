"""Map URLs to views"""

from werkzeug.routing import Map, Rule


url_map = Map([
    Rule("/", endpoint="index"),
    Rule("/login", endpoint="login"),
    Rule("/newbug/", endpoint="new_bug"),
    Rule("/bug/<int:bugid>/", endpoint="view_bug"),
    Rule("/bugs", endpoint="list_bugs")
], redirect_defaults=False)
