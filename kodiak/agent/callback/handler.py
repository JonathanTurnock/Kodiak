import logging

LOGGER = logging.getLogger(__name__)


def do_callback(ref_object):
    LOGGER.info(f"Performing Callback for {ref_object.__class__.__name__} - {ref_object.to_dict()}")
