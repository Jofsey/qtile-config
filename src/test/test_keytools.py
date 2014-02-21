from unittest import TestCase
from libqtile.command import lazy
from libqtile.config import Key
from src.keytools import expand_placeholders, MultiKey


class TestExpand_placeholders(TestCase):
    def test_expand_placeholders(self):
        key = Key(['mod4'], 'c', lazy.spawn('chromium'))
        key2 = MultiKey(['mod4'], MultiKey.left, lazy.spawn('chromium'))
        keys_before = [key, key2]
        print keys_before
        keys = expand_placeholders(keys_before)
        print keys
        if len(keys) != 3:
            self.fail("lenght != 3")
        self.assertEqual(keys[1].commands, keys_before[1].commands)
