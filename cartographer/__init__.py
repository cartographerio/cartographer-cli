import requests
import json
import functools
import semver
import sys

from cartographer.args import read_args
from cartographer.profile import read_profile
import cartographer.fetch as fetch


commands = {}


def register_command(command, subcommand=None):
    def wrapped(func):
        if subcommand is None:
            commands[command] = func
        else:
            if command not in commands:
                commands[command] = {}
            commands[command][subcommand] = func
        return func

    return wrapped


# Commands --------------------------------------


@register_command("workspace", "search")
def workspace_search(params):
    scheme = params["scheme"]
    host = params["host"]
    email = params["email"]
    password = params["password"]

    url = fetch.create_url(scheme, host, "/v1/workspace", {})
    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("workspace", "read")
def workspace_read(params):
    scheme = params["scheme"]
    host = params["host"]
    email = params["email"]
    password = params["password"]
    workspace = params["workspace"]

    url = fetch.create_url(scheme, host, "/v1/workspace/{}".format(workspace))
    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("module", "search")
def module_search(params):
    scheme = params["scheme"]
    host = params["host"]
    workspace = params["workspace"]
    email = params["email"]
    password = params["password"]

    url = fetch.create_url(scheme, host, "/v1/survey/module", {"workspace": workspace})

    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("module", "read")
def module_read(params):
    scheme = params["scheme"]
    host = params["host"]
    email = params["email"]
    password = params["password"]
    id = params["id"]

    url = fetch.create_url(scheme, host, "/v1/survey/module/{}".format(id))

    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("survey", "search")
def survey_search(params):
    scheme = params["scheme"]
    host = params["host"]
    email = params["email"]
    password = params["password"]
    workspace = params["workspace"]
    module = params["module"]
    order = params["order"]
    skip = params["skip"]
    limit = params["limit"]
    q = params["query"]
    format = params["format"]

    url = fetch.create_url(
        scheme,
        host,
        "/v1/survey/{}".format(module),
        {
            "workspace": workspace,
            "q": q,
            "order": order,
            "skip": skip,
            "limit": limit,
            "format": format,
        },
    )

    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("survey", "summaries")
def survey_search(params):
    scheme = params["scheme"]
    host = params["host"]
    email = params["email"]
    password = params["password"]
    workspace = params["workspace"]
    module = params["module"]
    order = params["order"]
    skip = params["skip"]
    limit = params["limit"]
    q = params["query"]
    format = params["format"]

    url = fetch.create_url(
        scheme,
        host,
        "/v1/survey/{}/summary".format(module),
        {
            "workspace": workspace,
            "q": q,
            "order": order,
            "skip": skip,
            "limit": limit,
            "format": format,
        },
    )

    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("survey", "read")
def survey_read(params):
    scheme = params["scheme"]
    host = params["host"]
    email = params["email"]
    password = params["password"]
    module = params["module"]
    id = params["id"]
    format = params["format"]

    url = fetch.create_url(
        scheme, host, "/v1/survey/{}/{}".format(module, id), {"format": format}
    )

    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("user", "search")
def user_search(params):
    scheme = params["scheme"]
    host = params["host"]
    workspace = params["workspace"]
    email = params["email"]
    password = params["password"]
    q = params["query"]
    role = params["role"]
    order = params["order"]
    skip = params["skip"]
    limit = params["limit"]

    url = fetch.create_url(
        scheme,
        host,
        "/v1/user",
        {
            "workspace": workspace,
            "q": q,
            "role": role,
            "order": order,
            "skip": skip,
            "limit": limit,
        },
    )
    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("user", "read")
def user_search(params):
    scheme = params["scheme"]
    host = params["host"]
    workspace = params["workspace"]
    email = params["email"]
    password = params["password"]
    id = params["id"]

    url = fetch.create_url(scheme, host, "/v1/user/{}".format(id))
    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers(workspace)
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("layer", "search")
def layer_search(params):
    scheme = params["scheme"]
    host = params["host"]
    workspace = params["workspace"]
    email = params["email"]
    password = params["password"]

    url = fetch.create_url(scheme, host, "/v1/map/layer", {"workspace": workspace})

    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("layer", "read")
def layer_read(params):
    scheme = params["scheme"]
    host = params["host"]
    workspace = params["workspace"]
    email = params["email"]
    password = params["password"]
    layer = params["layer"]

    url = fetch.create_url(
        scheme, host, "/v1/map/layer/{}".format(layer), {"workspace": workspace}
    )

    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("feature", "search")
def feature_search(params):
    scheme = params["scheme"]
    host = params["host"]
    workspace = params["workspace"]
    email = params["email"]
    password = params["password"]
    layer = params["layer"]
    simplify = params["simplify"]

    url = fetch.create_url(
        scheme,
        host,
        "/v1/map/{}".format(layer),
        {"workspace": workspace, "simplify": simplify},
    )

    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("feature", "reset")
def feature_reset(params):
    scheme = params["scheme"]
    host = params["host"]
    email = params["email"]
    password = params["password"]
    layer = params.get("layer", None)

    if layer:
        path = "/v1/map/{}/reset".format(layer)
    else:
        path = "/v1/map/reset"

    url = fetch.create_url(scheme, host, path, {})

    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("upload", "search")
def upload_search(params):
    scheme = params["scheme"]
    host = params["host"]
    email = params["email"]
    password = params["password"]
    module = params["module"]
    survey = params["survey"]
    subfolder = params["subfolder"]

    url = fetch.create_url(
        scheme,
        host,
        "/v1/upload",
        {"module": module, "survey": survey, "subfolder": subfolder},
    )

    auth = fetch.basic_auth(email, password)
    headers = fetch.create_headers()
    response = fetch.get(url, auth, headers)

    return response.json()


@register_command("version")
def version(params):
    scheme = params["scheme"]
    host = params["host"]

    url = fetch.create_url(scheme, host, "/v1/version")
    headers = {}
    response = fetch.get(url, None, headers)

    return response.json()


# Main ------------------------------------------


def main():
    args = read_args()
    profile = read_profile(args["profile"])
    params = {}

    for key in profile:
        params[key] = profile.get(key, None)

    for key in args:
        params[key] = args.get(key, None) or profile.get(key, None)

    cmd_name = params.get("command", None)
    sub_name = params.get("subcommand", None)

    if cmd_name in commands:
        cmd = commands[cmd_name]

        if callable(cmd):
            ans = cmd(params)
        elif sub_name in cmd:
            sub = cmd[sub_name]
            ans = sub(params)
        else:
            sys.stderr.write("Command not found: {} {}".format(cmd_name, sub_name))

        print(fetch.format_json(ans))
    else:
        sys.stderr.write("Command not found: {} {}".format(cmd_name, sub_name))

    return
