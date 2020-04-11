from unittest import TestCase

from kodiak.utils.version import is_later_version


class TestVersionUtils(TestCase):
    def test_is_later_version_returns_true_when_is_later(self):
        self.assertTrue(is_later_version("1.1.1", "1.0.0"))

    def test_is_later_version_returns_false_when_is_not_later(self):
        self.assertFalse(is_later_version("1.0.0", "1.1.1"))
