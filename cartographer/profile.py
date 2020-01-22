import os
import copy
import ConfigParser

profile_whitelist = {
    'scheme': 'string',
    'host': 'string',
    'email': 'string',
    'password': 'string',
    'legacy_urls': 'string',
    'legacy_json': 'boolean'
}

profile_defaults = {
    'scheme': 'https',
    'host': 'api.cartographer.io',
    'legacy_urls': 'no',
    'legacy_json': 'no'
}


def read_profile(profile_name=None):
    home_dir = os.getenv("HOME")

    config = ConfigParser.ConfigParser(profile_defaults)

    config.read([
        ".credentials",
        "{}/.cartographer/credentials".format(home_dir),
        "{}/.config/cartographer/credentials".format(home_dir)
    ])

    if profile_name is None:
        # HACK: If the user didn't ask for a profile,
        # inject an empty config section so we still get the [DEFAULT]s:
        profile_name = '__dummy_section__'
        config.add_section(profile_name)

    profile = {}

    for key in config.options(profile_name):
        type = profile_whitelist.get(key, None)
        if type == 'string':
            profile[key] = config.get(profile_name, key)
        elif type == 'boolean':
            profile[key] = config.getboolean(profile_name, key)
        else:
            sys.stderr.write('Skipping config key: {}'.format(key))

    return profile
