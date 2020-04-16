import os

has_override = lambda variable: f"FXQ_{variable}" in os.environ
get_override = lambda variable: os.environ[f"FXQ_{variable}"]
