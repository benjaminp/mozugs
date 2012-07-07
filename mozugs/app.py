"""Theory test main application"""

import codecs
import datetime
import os
import ConfigParser

from urlparse import urljoin

import jinja2

from werkzeug import BaseRequest, BaseResponse
from werkzeug.exceptions import HTTPException

from sqlalchemy import engine_from_config
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import exc as ormexc

from mozugs import models, urls, util, views


class GlobalState(object):
    """Global configuration and objects"""

    def __init__(self, root, config_path):
        """Initialize state.

        *root* is the base directory containing source code and
        templates. *config_path* is a sequence of configuration files to
        consider.
        """
        self.root = root
        config_dir = os.path.join(root, "config")
        config_path.insert(0, os.path.join(config_dir, "defaults.ini"))
        loader = jinja2.FileSystemLoader(os.path.join(root, "templates"))
        self.template_env = jinja2.Environment(loader=loader)
        config = ConfigParser.SafeConfigParser()
        config.read(config_path)
        root_vars = {"root" : root}
        db_config = {opt : config.get("db", opt, vars=root_vars)
                     for opt in config.options("db")}
        self.engine = engine_from_config(db_config, "")
        self.salt = config.get("app", "salt")
        session_days = config.getint("app", "session_length_days")
        self.session_length_delta = datetime.timedelta(days=session_days)
        self.have_recaptcha = config.getboolean("app", "enable_recaptcha")
        if self.have_recaptcha:
            self.recaptcha_public = config.get("recaptcha", "public_key")
            self.recaptcha_private = config.get("recaptcha", "private_key")
        self.can_send_email = config.getboolean("app", "enable_smtp")
        if self.can_send_email:
            self.mail_sender = config.get("smtp", "sender")
            self.smtp_host = config.get("smtp", "host")
            self.smtp_port = config.getint("smtp", "port")
            self.smtp_user = config.get("smtp", "user")
            self.smtp_password = config.get("smtp", "password")
        self.data_dir = config.get("app", "test_data", vars=root_vars)
        self.static_base = config.get("app", "static_base")
        self.admin_users = set(config.get("app", "admin_users").split())
        self.admin_addr = config.get("app", "admin_addr")

    def create_session(self):
        """Create a SQLAlchemy session."""
        return Session(self.engine, autoflush=False)


def active_auth_session(req):
    key = req.cookies.get("auth")
    if key is None or len(key) != 32:
        return None
    q = req.session.query(models.AuthSession).filter_by(key=key)
    try:
        return q.one()
    except ormexc.NoResultFound:
        return None


class BugTrackerApp(GlobalState):
    """WSGI application"""

    class Request(BaseRequest):
        parameter_storage_class = dict
    Response = BaseResponse


    def __call__(self, env, start_response):
        """Run the WSGI application"""
        req = self.Request(env)
        req.router = urls.url_map.bind_to_environ(env)
        # When running with FastCGI, this prevents the script name from getting
        # into the URL.
        req.router.script_name = util.get_script_name(env)
        req.session = self.create_session()
        auth = active_auth_session(req)
        req.user = None if auth is None else auth.user
        try:
            end, values = req.router.match()
            view = getattr(views, end)
            resp = view(self, req, **values)
        except HTTPException, e:
            resp = e.get_response(env)
        # Cleanup the database session.
        resp.call_on_close(req.session.close)
        return resp(env, start_response)

    def get_static_resource(self, what):
        """Get the URL of a static resource"""
        sb = self.static_base
        if sb is not None:
            return urljoin(sb, what)
        # On test server.
        return u"/static/" + what
