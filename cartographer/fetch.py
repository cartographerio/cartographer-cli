import requests
import json

cert = None  # 'charles-ssl-proxying-certificate.pem'


# URLs ------------------------------------------


def create_url(scheme, host, path, query={}):
    filtered_query = {}
    for (key, val) in query.items():
        if isinstance(val, str):
            filtered_query[key] = val
        elif isinstance(val, bool):
            if val == True:
                filtered_query[key] = "true"
            else:
                filtered_query[key] = "false"
        elif val:
            filtered_query[key] = str(val)
    query_args = ["{}={}".format(key, val) for (key, val) in filtered_query.items()]
    query_string = "&".join(query_args)
    url = "{}://{}{}?{}".format(scheme, host, path, query_string)
    # print(url)
    return url


# Headers ---------------------------------------


def create_headers(token=None):
    headers = {}
    if token is not None:
        headers["Authorization"] = "Bearer {}".format(token)
    return headers


# Responses -------------------------------------


def format_json(data):
    return json.dumps(data, sort_keys=False)


# Requests -------------------------------------


def handle_http_errors(response):
    # Adapted from `raise_for_status()` in the `requests` library:
    if 400 <= response.status_code < 600:
        status = response.status_code

        if isinstance(response.reason, bytes):
            try:
                reason = response.reason.decode("utf-8")
            except UnicodeDecodeError:
                reason = response.reason.decode("iso-8859-1")
        else:
            reason = response.reason

        msg = "Server returned {} {}".format(status, reason)

        raise requests.HTTPError(msg, response=response)


def get(url, auth, headers):
    response = requests.get(url, headers=headers, auth=auth, verify=cert)
    handle_http_errors(response)
    return response


def post(url, auth, headers, payload):
    response = requests.post(
        url, headers=headers, auth=auth, verify=cert, data=json.dumps(payload)
    )
    handle_http_errors(response)
    return response


def put(url, auth, headers, payload):
    response = requests.put(
        url, headers=headers, auth=auth, verify=cert, data=json.dumps(payload)
    )
    handle_http_errors(response)
    return response


def basic_auth(email, password):
    return requests.auth.HTTPBasicAuth(email, password)
