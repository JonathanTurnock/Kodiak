import importlib

from bootstrap import env

importlib.import_module(env.get_property("datasource.driver"))
