"""Map URLs to views"""

from werkzeug.routing import Map, Rule


url_map = Map([
    Rule("/", endpoint="index"),
    Rule("/newbug/", endpoint="new_bug"),
    Rule("/bug/<int:bugid>/", endpoint="view_bug"),
], redirect_defaults=False)
