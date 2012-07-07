def respond(app, req, template, env):
    """Run template engine and generate response"""
    build_url = req.router.build
    def url_for(view, **values):
        return build_url(view, values, append_unknown=False)
    env["url_for"] = url_for
    env["static"] = app.get_static_resource
    env["admin_addr"] = app.admin_addr
    template = app.template_env.get_template(template)
    body = template.render(env)
    return app.Response(body, content_type="text/html; charset=UTF-8")


def index(app, req):
    return respond(app, req, "index.html", {})
