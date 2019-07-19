import json
import logging
import threading
from http import HTTPStatus

import requests
from fxq.core.beans.factory.annotation import Autowired

from fxq.ae.agent.constants import JSON_HEADERS, URI_LIST_HEADERS
from fxq.ae.agent.service.consul import ConsulService

LOGGER = logging.getLogger(__name__)

consul_service: ConsulService = Autowired(type=ConsulService)
callback_host = None


def get_callback_host():
    global callback_host
    try:
        callback_host = f'{consul_service.get_callback_host()}'
        LOGGER.info(f'Configuring callback host as {callback_host}')
        t = threading.Timer(30.0, get_callback_host)
        t.start()
    except Exception as e:
        LOGGER.error(e)


get_callback_host()

def get_callback_url(ref_object):
    if ref_object.__class__.__name__ == "Run":
        return f'{callback_host}/api/data/runs'
    if ref_object.__class__.__name__ == "Step":
        return f'{callback_host}/api/data/steps'
    if ref_object.__class__.__name__ == "Command":
        return f'{callback_host}/api/data/commands'


def do_callback(ref_object):
    callback_url = get_callback_url(ref_object)
    if callback_url:
        LOGGER.info("Performing Callback for %s" % ref_object.to_dict())
    else:
        LOGGER.warning("No Callback URL could be determined")

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
