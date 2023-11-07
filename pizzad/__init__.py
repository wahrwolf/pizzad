from importlib.util import find_spec
KNOWN_DEPENDENCIES = ["flask", "click"]


def get_missing_dependencies():
    missing_dependencies = [dep for dep in KNOWN_DEPENDENCIES if not find_spec(dep)]
    return missing_dependencies
