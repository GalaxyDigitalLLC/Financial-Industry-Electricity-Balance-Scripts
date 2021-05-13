import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers  # noqa: E402


class TestHelpers(unittest.TestCase):
    def test_to_gw_from_kw(self):
        kw = 1_000_000
        expect = 1
        self.assertEqual(expect, helpers.kw_to_gw(kw))

    def test_to_tw_from_kw(self):
        kw = 1_000_000_000
        expect = 1
        self.assertEqual(expect, helpers.kw_to_tw(kw))


if __name__ == '__main__':
    unittest.main()
