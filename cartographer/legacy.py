import requests
import json
import functools
import semver

cert = None  # 'charles-ssl-proxying-certificate.pem'

# URLs ------------------------------------------


def create_url(scheme, host, path, query={}):
    filtered_query = {}
    for (key, val) in query.items():
        if val:
            filtered_query[key] = val
    query_args = ["{}={}".format(key, val)
                  for (key, val) in filtered_query.items()]
    query_string = "&".join(query_args)
    return "{}://{}{}?{}".format(scheme, host, path, query_string)

# Headers ---------------------------------------


def create_headers(workspace='*', token=None):
    headers = {'Workspace': workspace}
    if token is not None:
        headers['Authorization'] = "Bearer {}".format(token)
    return headers

# Responses -------------------------------------


def format_json(data):
    return json.dumps(data, sort_keys=False, indent=2)

# Requests -------------------------------------


def handle_http_errors(response):
    # Adapted from `raise_for_status()` in the `requests` library:
    if 400 <= response.status_code < 600:
        status = response.status_code

        if isinstance(response.reason, bytes):
            try:
                reason = response.reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = response.reason.decode('iso-8859-1')
        else:
            reason = response.reason

        msg = "Server returned {} {}".format(status, reason)

        raise requests.HTTPError(msg, response=response)


def get(url, auth, headers):
    response = requests.get(url, headers=headers, auth=auth, verify=cert)
    handle_http_errors(response)
    return response


def post(url, auth, headers, payload):
    response = requests.post(url, headers=headers,
                             auth=auth, verify=cert, data=json.dumps(payload))
    handle_http_errors(response)
    return response


def put(url, auth, headers, payload):
    response = requests.put(url, headers=headers, auth=auth,
                            verify=cert, data=json.dumps(payload))
    handle_http_errors(response)
    return response


def basic_auth(email, password):
    return requests.auth.HTTPBasicAuth(email, password)

# Options ---------------------------------------


with_scheme = click.option('--scheme', envvar='CARTOGRAPHER_SCHEME',
                           default='https', help='The URL scheme to use')
with_host = click.option('--host', envvar='CARTOGRAPHER_HOST',
                         default='api.cartographer.io', help='The server hostname')
with_legacy_urls = click.option('--legacy-urls/--no-legacy-urls', envvar='CARTOGRAPHER_HOST',
                                default=False, help='Use legcy URLs? (for older server versions)')
with_workspace = click.option('--workspace', envvar='CARTOGRAPHER_WORKSPACE',
                              default='*', help='The workspace to scope the query to')
with_email = click.option('--email', envvar='CARTOGRAPHER_EMAIL',
                          prompt=True, help='The email to use to authenticate')
with_password = click.option('--password', envvar='CARTOGRAPHER_PASSWORD',
                             prompt=True, hide_input=True, help='The password to use to authenticate')
with_optional_email = click.option('--email', envvar='CARTOGRAPHER_EMAIL',
                                   default=None, help='The email to use to authenticate (optional)')
with_optional_password = click.option('--password', envvar='CARTOGRAPHER_PASSWORD',
                                      default=None, hide_input=True, help='The password to use to authenticate (optional)')


def with_required_param(name):
    return click.option('--{}'.format(name), prompt=True)


def with_optional_param(name):
    return click.option('--{}'.format(name), default=None)

# Commands --------------------------------------

# Login


@click.command()
@with_scheme
@with_host
@with_email
@with_password
@click_config_file.configuration_option()
def login(scheme, host, email, password):
    click.echo(format_json(fetch_credentials(scheme, host, email, password)))

# Survey module


@click.group()
def workspace():
    pass


@click.command('search')
@with_scheme
@with_host
@with_email
@with_password
@click_config_file.configuration_option()
def workspace_search(scheme, host, email, password):
    url = create_url(scheme, host, '/v1/workspace', {})
    auth = basic_auth(email, password)
    headers = create_headers('*')
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


workspace.add_command(workspace_search)


@click.command('read')
@with_scheme
@with_host
@with_email
@with_password
@with_required_param('id')
@click_config_file.configuration_option()
def workspace_read(scheme, host, email, password, id):
    url = create_url(scheme, host, '/v1/workspace/{}'.format(id))
    auth = basic_auth(email, password)
    headers = create_headers('*')
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


workspace.add_command(workspace_read)


# Survey module


@click.group()
def module():
    pass


@click.command('search')
@with_scheme
@with_host
@with_workspace
@with_email
@with_password
@click_config_file.configuration_option()
def module_search(scheme, host, workspace, email, password):
    url = create_url(scheme, host, '/v1/survey/module', {})
    auth = basic_auth(email, password)
    headers = create_headers(workspace)
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


module.add_command(module_search)


@click.command('read')
@with_scheme
@with_host
@with_workspace
@with_email
@with_password
@with_required_param('module')
@click_config_file.configuration_option()
def module_read(scheme, host, workspace, email, password, module):
    url = create_url(scheme, host, '/v1/survey/module/{}'.format(module))
    auth = basic_auth(email, password)
    headers = create_headers(workspace)
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


module.add_command(module_read)

# survey


@click.group()
def survey():
    pass


@click.command('search')
@with_scheme
@with_host
@with_legacy_urls
@with_workspace
@with_email
@with_password
@with_required_param('module')
@with_optional_param('order')
@with_optional_param('skip')
@with_optional_param('limit')
@with_optional_param('q')
@click_config_file.configuration_option()
def survey_search(scheme, host, legacy_urls, workspace, email, password, module, order, skip, limit, q):
    if legacy_urls:
        url = create_url(scheme, host, '/v1/survey', {
            "type": module,
            "order": order,
            "skip": skip,
            "limit": limit,
            "q": q
        })
    else:
        url = create_url(scheme, host, '/v1/survey/{}'.format(module), {
            "order": order,
            "skip": skip,
            "limit": limit,
            "q": q
        })
    auth = basic_auth(email, password)
    headers = create_headers(workspace)
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


survey.add_command(survey_search)


@click.command('read')
@with_scheme
@with_host
@with_legacy_urls
@with_workspace
@with_email
@with_password
@with_optional_param('format')
@with_required_param('module')
@with_required_param('id')
@click_config_file.configuration_option()
def survey_read(scheme, host, legacy_urls, workspace, email, password, format, module, id):
    if legacy_urls:
        url = create_url(scheme, host, '/v1/survey/{}'.format(id), {
            "format": format
        })
    else:
        url = create_url(scheme, host, '/v1/survey/{}/{}'.format(module, id), {
            "format": format
        })
    auth = basic_auth(email, password)
    headers = create_headers(workspace)
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


survey.add_command(survey_read)

# User


@click.group()
def user():
    pass


@click.command('search')
@with_scheme
@with_host
@with_workspace
@with_email
@with_password
@with_optional_param('role')
@with_optional_param('order')
@click_config_file.configuration_option()
def user_search(scheme, host, workspace, email, password, role, order):
    url = create_url(scheme, host, '/v1/user', {'role': role, 'order': order})
    auth = basic_auth(email, password)
    headers = create_headers(workspace)
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


user.add_command(user_search)

# Map layer


@click.group()
def layer():
    pass


@click.command('search')
@with_scheme
@with_host
@with_workspace
@with_optional_email
@with_optional_password
@click_config_file.configuration_option()
def layer_search(scheme, host, workspace, email, password):
    url = create_url(scheme, host, '/v1/map/layer', {})
    auth = basic_auth(email, password)
    headers = create_headers(workspace)
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


layer.add_command(layer_search)


@click.command('read')
@with_scheme
@with_host
@with_workspace
@with_optional_email
@with_optional_password
@with_required_param('layer')
@click_config_file.configuration_option()
def layer_read(scheme, host, workspace, email, password, layer):
    url = create_url(scheme, host, '/v1/map/layer/{}'.format(layer))
    auth = basic_auth(email, password)
    headers = create_headers(workspace)
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


layer.add_command(layer_read)

# Feature


@click.group()
def feature():
    pass


@click.command('search')
@with_scheme
@with_host
@with_workspace
@with_optional_email
@with_optional_password
@with_required_param('layer')
@click_config_file.configuration_option()
def feature_search(scheme, host, workspace, email, password, layer):
    url = create_url(scheme, host, '/v1/map/{}'.format(layer), {})
    auth = basic_auth(email, password)
    headers = create_headers(workspace)
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


feature.add_command(feature_search)


@click.command('reset')
@with_scheme
@with_host
@with_workspace
@with_email
@with_password
@with_optional_param('layer')
@click_config_file.configuration_option()
def feature_reset(scheme, host, workspace, email, password, layer):
    if layer:
        url = create_url(scheme, host, '/v1/map/{}/reset'.format(layer), {})
    else:
        url = create_url(scheme, host, '/v1/map/reset', {})
        auth = basic_auth(email, password)
    headers = create_headers(workspace)
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


feature.add_command(feature_reset)

# Upload


@click.group()
def upload():
    pass


@click.command('search')
@with_scheme
@with_host
@with_workspace
@with_email
@with_password
@with_required_param('survey')
@click_config_file.configuration_option()
def upload_search(scheme, host, workspace, email, password, survey):
    url = create_url(scheme, host, '/v1/upload', {'survey': survey})
    auth = basic_auth(email, password)
    headers = create_headers(workspace)
    response = get(url, auth, headers)
    click.echo(format_json(response.json()))


upload.add_command(upload_search)

# Version


@click.command('version')
@with_scheme
@with_host
@click_config_file.configuration_option()
def version(scheme, host):
    url = create_url(scheme, host, '/v1/version')
    headers = {}
    response = get(url, None, headers)
    click.echo(format_json(response.json()))

# Main ------------------------------------------


@click.group()
def main():
    pass


main.add_command(login)
main.add_command(workspace)
main.add_command(module)
main.add_command(survey)
main.add_command(layer)
main.add_command(feature)
main.add_command(user)
main.add_command(upload)
main.add_command(version)
