#!/usr/bin/env python
"""Management utilities"""

import os

from _setuppaths import root

from werkzeug import script, security

from mozugs import models
from mozugs.app import BugTrackerApp


static = {"/static" : os.path.join(root, "static")}
config_dir = os.path.join(root, "config")
config_files = [os.path.join(config_dir, fn) for fn in os.listdir(config_dir)
                if fn.endswith(".ini")]


def _create_app():
    app = BugTrackerApp(root, [os.path.join(config_dir, "test.ini"),
                               os.path.join(config_dir, "local.ini")])
    models.ModelBase.metadata.create_all(app.engine)
    return app


def _init_shell():
    return {"app" : _create_app()}


action_run = script.make_runserver(_create_app, port=1111, use_reloader=True,
                                   extra_files=config_files,
                                   static_files=static)
action_shell = script.make_shell(_init_shell)


def action_gensalt():
    print(security.gen_salt(8))


if __name__ == "__main__":
    script.run(globals())
