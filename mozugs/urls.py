"""Map URLs to views"""

from werkzeug.routing import Map, Rule


url_map = Map([
    Rule("/", endpoint="index"),
    Rule("/login", endpoint="login")
], redirect_defaults=False)
