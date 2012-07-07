import datetime
import json
import urllib

from sqlalchemy import exc as saexc
from sqlalchemy.orm import exc as ormexc

from werkzeug import redirect
from werkzeug.exceptions import Forbidden

from mozugs import models, util


def respond(app, req, template, env):
    """Run template engine and generate response"""
    build_url = req.router.build
    def url_for(view, **values):
        return build_url(view, values, append_unknown=False)
    env["user"] = req.user
    env["url_for"] = url_for
    env["static"] = app.get_static_resource
    env["admin_addr"] = app.admin_addr
    template = app.template_env.get_template(template)
    body = template.render(env)
    return app.Response(body, content_type="text/html; charset=UTF-8")


def index(app, req):
    return respond(app, req, "index.html", {})


def login(app, req):
    assertion = req.form["assertion"]
    audience = "localhost:1111" # TODO: lose hardcoding
    data = dict(assertion=assertion, audience=audience)

    u = urllib.urlopen("https://browserid.org/verify", data=urllib.urlencode(data))
    resp = json.loads(u.read())

    response = app.Response('')
    if resp["status"] == "okay":
        try:
            user = req.session.query(models.User).filter_by(email=resp["email"]).one()
        except ormexc.NoResultFound:
            user = models.User(resp["email"])
            req.session.add(user)
        # Add session
        while True:
            key = util.make_key(app.salt)
            expires = datetime.datetime.utcnow() + app.session_length_delta
            auth = models.AuthSession(user, key, expires)
            req.session.add(auth)
            try:
                req.session.commit()
            except saexc.IntegrityError:
                # The key was not unique; try again.
                continue
            break
        response.set_cookie("auth", key, expires=expires)
    else:
        response.status = 403
    return response


def logout(app, req):
    if req.user is not None:
        req.session.query(models.AuthSession).filter_by(user=req.user).delete()
        req.session.commit()
    return redirect(req.router.build("index"))


def new_bug(app, req):
    if req.user is None:
        raise Forbidden
    if req.method == "GET":
        return respond(app, req, "newbug.html", {})
    bug = models.Bug()
    bug.reporter = req.user
    bug.title = req.form[u"title"]
    bug.description = req.form[u"description"]
    bug.severity = req.form[u"severity"]
    bug.keywords = req.form[u"keywords"]
    bug.product = req.form[u"product"]
    bug.version = req.form[u"version"]
    req.session.add(bug)
    req.session.commit()
    return redirect(req.router.build("view_bug", {"bugid" : bug.id}))


def view_bug(app, req, bugid):
    bug = req.session.query(models.Bug).filter_by(id=bugid).one()
    comments = req.session.query(models.Comment).filter_by(bug_id=bugid)
    comments_description = [c for c in comments if c.kind == "Description"]
    comments_cause = [c for c in comments if c.kind == "Cause"]
    comments_solution = [c for c in comments if c.kind == "Solution"]
    return respond(app, req, "bug.html", {u"bug" : bug,
                                          u"comments_description": comments_description,
                                          u"comments_cause": comments_cause,
                                          u"comments_solution": comments_solution})


def list_bugs(app, req):
    bugs = req.session.query(models.Bug)
    return respond(app, req, "list_bugs.html", {u"bugs": bugs})


def add_comment(app, req, kind, bugid):
    comment = models.Comment()
    comment.bug_id = bugid
    comment.kind = kind
    comment.user = req.user
    comment.message = req.form[u"message"]

    req.session.add(comment)
    req.session.commit()

    return redirect(req.router.build("view_bug", {"bugid": bugid}))
