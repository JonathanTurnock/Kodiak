from unittest import TestCase
from unittest.mock import patch

from kodiak.utils.id import new_string_id


class TestIdUtils(TestCase):

    @patch("kodiak.utils.id.uuid")
    def test_new_string_id(self, mock_uuid_module):
        mock_uuid_module.uuid4.return_value = "8f398fbe-c0b5-49e9-914d-ddb1ee856356"
        expected_uuid = "8f398fbec0b549e9914dddb1ee856356"
        id = new_string_id()
        self.assertEqual(id, expected_uuid)
