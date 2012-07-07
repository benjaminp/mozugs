def get_script_name(environ):
    """Returns the equivalent of the HTTP request's SCRIPT_NAME environment
    variable. If Apache mod_rewrite has been used, returns what would have been
    the script name prior to any rewriting.
    """
    # If Apache's mod_rewrite had a whack at the URL, Apache set either
    # SCRIPT_URL or REDIRECT_URL to the full resource URL before applying any
    # rewrites.
    script_url = environ.get('SCRIPT_URL', '')
    if not script_url:
        script_url = environ.get('REDIRECT_URL', '')
    if script_url:
        name = script_url[:-len(environ.get('PATH_INFO', ''))]
        if not name.endswith("/"):
            name += "/"
        return name
    return "/"
