import argparse

parser = argparse.ArgumentParser(prog="cartographer")


def read_args():
    return vars(parser.parse_args())


# Global options ================================

parser.add_argument(
    "-p", "--profile", help="The configuration profile to use", default="default"
)

parser.add_argument(
    "-U",
    "--email",
    "--username",
    help="The username or email address to use to authenticate with",
)

parser.add_argument("-P", "--password", help="The password to use to authenticate")

parsers = parser.add_subparsers(dest="command")


# Workspaces ====================================

workspace_parsers = parsers.add_parser(
    "workspace", help="Commands related to workspaces"
).add_subparsers(dest="subcommand")

# Workspace search ------------------------------

workspace_search = workspace_parsers.add_parser(
    "search", help="Search the workspaces on the API server"
)

# Workspace read --------------------------------

workspace_read = workspace_parsers.add_parser(
    "read", help="Read data on a specific workspace"
)

workspace_read.add_argument(
    "workspace", help="The ID or subdomain of the workspace to read"
)


# Modules =======================================

module_parsers = parsers.add_parser(
    "module", help="Commands related to module data"
).add_subparsers(dest="subcommand")

# Module search ---------------------------------

module_search = module_parsers.add_parser(
    "search", help="Search modules in a particular workspace/module"
)

module_search.add_argument(
    "-w", "--workspace", help="Workspace ID or subdomain", default=None
)

# Module read -----------------------------------

module_read = module_parsers.add_parser("read", help="Read data on a specific module")

module_read.add_argument("id", help="The ID of the module to read")


# Surveys =======================================

survey_parsers = parsers.add_parser(
    "survey", help="Commands related to survey data"
).add_subparsers(dest="subcommand")

# Survey search ---------------------------------

survey_search = survey_parsers.add_parser(
    "search", help="Search surveys in a particular workspace/module"
)

survey_search.add_argument("module", help="The module to search")

survey_search.add_argument(
    "-w", "--workspace", help="Workspace ID or subdomain", default=None
)

survey_search.add_argument("-q", "--query", help="Search string")

survey_search.add_argument("-o", "--order", help="Result order")

survey_search.add_argument("--skip", type=int, help="Skip the first N results")

survey_search.add_argument(
    "--limit", type=int, help="Fetch the first N results (after skip count)"
)

survey_search.add_argument(
    "--format", default=None, help='Set to "legacy" to receive old-style survey JSON'
)

# Survey summaries ---------------------------------

survey_summaries = survey_parsers.add_parser(
    "summaries", help="Search surveys in a particular workspace/module"
)

survey_summaries.add_argument("module", help="The module to search")

survey_summaries.add_argument(
    "-w", "--workspace", help="Workspace ID or subdomain", default=None
)

survey_summaries.add_argument("-q", "--query", help="Search string")

survey_summaries.add_argument("-o", "--order", help="Result order")

survey_summaries.add_argument("--skip", type=int, help="Skip the first N results")

survey_summaries.add_argument(
    "--limit", type=int, help="Fetch the first N results (after skip count)"
)

survey_summaries.add_argument(
    "--format", default=None, help='Set to "legacy" to receive old-style survey JSON'
)

# Survey read -----------------------------------

survey_read = survey_parsers.add_parser("read", help="Read data on a specific survey")

survey_read.add_argument("module", help="The survey module")

survey_read.add_argument("id", help="The ID of the survey to read")

survey_read.add_argument(
    "--format", default=None, help='Set to "legacy" to receive old-style survey JSON'
)

# Users =========================================

user_parsers = parsers.add_parser(
    "user", help="Commands related to user data"
).add_subparsers(dest="subcommand")

# User search -----------------------------------

user_search = user_parsers.add_parser(
    "search", help="Search users in a particular workspace/module"
)

user_search.add_argument(
    "-w", "--workspace", help="Workspace ID or subdomain", default=None
)

user_search.add_argument("-q", "--query", help="Search string")

user_search.add_argument("-r", "--role", help="Search for users with a particular role")

user_search.add_argument("-o", "--order", help="Result order")

user_search.add_argument("--skip", type=int, help="Skip the first N results")

user_search.add_argument(
    "--limit", type=int, help="Fetch the first N results (after skip count)"
)

# User read -------------------------------------

user_read = user_parsers.add_parser("read", help="Read data on a specific user")

user_read.add_argument(
    "-w",
    "--workspace",
    help='Workspace name, or "*" to search all workspaces',
    default="*",
)

user_read.add_argument("id", help="The ID of the user to read")


# Map layers ======================================

layer_parsers = parsers.add_parser(
    "layer", help="Commands related to map layer metadata"
).add_subparsers(dest="subcommand")

# Map layer search --------------------------------

layer_search = layer_parsers.add_parser(
    "search", help="Search users in a particular workspace/module"
)

layer_search.add_argument(
    "-w", "--workspace", help="Workspace ID or subdomain", default=None
)

# Map layer read ---------------------------------

layer_read = layer_parsers.add_parser("reset", help="Reset maps layer(s)")

layer_read.add_argument("layer", help="The layer ID")

layer_read.add_argument(
    "-w", "--workspace", help="Workspace ID or subdomain", default=None
)

# Features ======================================

feature_parsers = parsers.add_parser(
    "feature", help="Commands related to feature data"
).add_subparsers(dest="subcommand")

# Feature search --------------------------------

feature_search = feature_parsers.add_parser(
    "search", help="Search users in a particular workspace/module"
)

feature_search.add_argument("layer", help="The layer to search")

feature_search.add_argument(
    "-w", "--workspace", help="Workspace ID or subdomain", default=None
)

feature_search.add_argument(
    "-s", "--simplify", help="Simplify geometry", action="store_true"
)


# Feature reset ---------------------------------

feature_reset = feature_parsers.add_parser(
    "reset", help="Reset (recalculate) feature data"
)

feature_reset.add_argument("-l", "--layer", help="The layer to reset", default=None)


# Attachments ===================================

attachment_parsers = parsers.add_parser(
    "attachment", help="Commands related to attachmented files"
).add_subparsers(dest="subcommand")

# attachment search ---------------------------------

attachment_search = attachment_parsers.add_parser(
    "search", help="Search attachments in a particular survey"
)

attachment_search.add_argument("module", help="The survey module")

attachment_search.add_argument("survey", help="The survey")

attachment_search.add_argument("-f", "--folder", help="Optional folder to search")


# Version =======================================


version = parsers.add_parser("version", help="Get server version")
