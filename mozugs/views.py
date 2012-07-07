from werkzeug import redirect

from mozugs import models


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


def new_bug(app, req):
    if req.method == "GET":
        return respond(app, req, "newbug.html", {})
    bug = models.Bug()
    bug.title = req.form[u"title"]
    bug.description = req.form[u"description"]
    req.session.add(bug)
    req.session.commit()
    return redirect(req.router.build("view_bug", {"bugid" : bug.id}))


def view_bug(app, req, bugid):
    bug = req.session.query(models.Bug).filter_by(id=bugid).one()
    return respond(app, req, "bug.html", {u"bug" : bug})
