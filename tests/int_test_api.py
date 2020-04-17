import json
import logging
from unittest import TestCase

import requests

LOGGING_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
logging.basicConfig(format=LOGGING_FORMAT, level=logging.ERROR)

gql_url = "http://localhost:5000/api/graphql"
headers = {
    'Content-Type': 'application/json'
}

get_jobs = lambda: send_query('''\
query {
    getJobs {
        uuid
        name
        url
    }
}''')

add_job = lambda name, url: send_query('''\
mutation {
    addJob(name: "%s", url: "%s") {
        uuid
        name
        url
    }
}''' % (name, url))

remove_job = lambda uuid: send_query('''\
mutation {
    removeJob(uuid: "%s")
}''' % (uuid,))


def send_query(query: str, variables: dict = None):
    payload = {
        "query": query,
        "variables": {} if variables is None else variables
    }
    logging.info(f"#### GraphQL Query ####\n{query}")
    response = requests.request("POST", gql_url, headers=headers, data=json.dumps(payload))
    resp_bdy = json.loads(response.text)

    logging.info(f"#### GraphQL Response ####\n{json.dumps(resp_bdy['data'], indent=4, sort_keys=False)}")

    if "errors" in resp_bdy.keys():
        logging.error(f"#### GraphQL Error ####\n{json.dumps(resp_bdy['errors'], indent=4, sort_keys=False)}")

    if response.status_code != 200:
        raise Exception(f"Invalid Status Code, expected 200, received {response.status_code}")

    return resp_bdy["data"]


def job_is_present(uuid):
    r = get_jobs()
    matching_jobs = [job for job in r["getJobs"] if job["uuid"] == uuid]
    return len(matching_jobs) == 1


def job_is_not_present(uuid):
    r = get_jobs()
    matching_jobs = [job for job in r["getJobs"] if job["uuid"] == uuid]
    return len(matching_jobs) == 0


class AddJobTests(TestCase):
    """
    Tests adding Jobs via the Graphql API
    """

    def setUp(self) -> None:
        self.r = add_job("AEP Hello World", "git@bitbucket.org:fxqlabs/aep-hello-world.git")

    def test_add_job(self):
        self.assertEqual(self.r["addJob"]["name"], "AEP Hello World")
        self.assertEqual(self.r["addJob"]["url"], "git@bitbucket.org:fxqlabs/aep-hello-world.git")

    def test_job_is_in_jobs_list(self):
        self.assertTrue(job_is_present(self.r["addJob"]["uuid"]))


class GetJobsTests(TestCase):
    """
    Tests getting Jobs via the Graphql API
    """

    def test_get_jobs_matches_schema(self):
        self.r = get_jobs()
        self.assertIsInstance(self.r["getJobs"][0]["uuid"], str)
        self.assertIsInstance(self.r["getJobs"][0]["name"], str)
        self.assertIsInstance(self.r["getJobs"][0]["url"], str)


class RemoveJobsTests(TestCase):
    """
    Tests Removing Jobs via the Graphql API
    """

    def setUp(self) -> None:
        self.add_job_r = add_job("AEP Hello World", "git@bitbucket.org:fxqlabs/aep-hello-world.git")
        self.added_job_uuid = self.add_job_r["addJob"]["uuid"]
        self.assertTrue(job_is_present(self.added_job_uuid))

    def test_remove_job_returns_true_on_success(self):
        r = remove_job(self.added_job_uuid)
        self.assertTrue(r["removeJob"])

    def test_remove_job_is_not_in_jobs_list(self):
        remove_job(self.added_job_uuid)
        self.assertTrue(job_is_not_present(self.added_job_uuid))
