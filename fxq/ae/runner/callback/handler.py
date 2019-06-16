import json
import logging
import os
from http import HTTPStatus

import requests

from fxq.ae.runner.constants import JSON_HEADERS, URI_LIST_HEADERS

try:
    run_callback_url = os.environ["RUN_CALLBACK_URL"]
except KeyError:
    run_callback_url = None

try:
    step_callback_url = os.environ["STEP_CALLBACK_URL"]
except KeyError:
    step_callback_url = None

try:
    cmd_callback_url = os.environ["CMD_CALLBACK_URL"]
except KeyError:
    cmd_callback_url = None

LOGGER = logging.getLogger(__name__)


def get_callback_url(ref_object):
    if ref_object.__class__.__name__ == "Run":
        return run_callback_url
    if ref_object.__class__.__name__ == "Step":
        return step_callback_url
    if ref_object.__class__.__name__ == "Command":
        return cmd_callback_url


def do_callback(ref_object):
    LOGGER.info("Performing Callback for %s" % ref_object.to_dict())
    callback_url = get_callback_url(ref_object)
    if callback_url and ref_object._links:
        r = requests.patch(
            ref_object._links["self"]["href"],
            data=json.dumps(ref_object.to_dict()),
            headers=JSON_HEADERS)
        if r.status_code != HTTPStatus.OK:
            LOGGER.error("Post Callback Failed with Status Code %s" % r.status_code)
            LOGGER.debug("%s - %s" % (r.status_code, r.text))
            raise Exception("Post Callback Failed with Status Code %s" % r.status_code)
    elif callback_url and ref_object._links is None:
        r = requests.post(
            "%s" % callback_url,
            data=json.dumps(ref_object.to_dict()),
            headers=JSON_HEADERS)
        if r.status_code == HTTPStatus.CREATED:
            ref_object._links = r.json()["_links"]
        else:
            LOGGER.error("Post Callback Failed with Status Code %s" % r.status_code)
            LOGGER.debug("%s - %s" % (r.status_code, r.text))
            raise Exception("Post Callback Failed with Status Code %s" % r.status_code)
        for link_name, link_value in ref_object._links.items():
            try:
                associated_object = getattr(ref_object, link_name)
                LOGGER.info(
                    "%s is being linked to %s" % (link_value["href"], associated_object._links["self"]["href"]))
                requests.put(link_value["href"], data=associated_object._links["self"]["href"],
                             headers=URI_LIST_HEADERS)
            except AttributeError:
                LOGGER.info("No associated object exists of type %s for type %s" % (
                    link_name, ref_object.__class__.__name__))
