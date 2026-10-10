import datetime
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clockenstein.formatting import default_time_locale, format_time


class TimeFormattingTests(unittest.TestCase):
    def test_locale_time_format_removes_seconds_and_its_separator(self):
        with patch("clockenstein.formatting.locale.nl_langinfo", return_value="%I:%M:%S %p"):
            self.assertEqual(format_time(datetime.time(13, 5, 42)), "01:05 PM")

    def test_locale_time_format_removes_alternative_seconds(self):
        with patch("clockenstein.formatting.locale.nl_langinfo", return_value="%H.%M.%OS"):
            self.assertEqual(format_time(datetime.time(13, 5, 42)), "13.05")

    def test_locale_time_format_expands_composite_directives(self):
        with patch("clockenstein.formatting.locale.nl_langinfo", return_value="%r"):
            self.assertEqual(format_time(datetime.time(13, 5, 42)), "01:05 PM")

    def test_forced_clock_formats_omit_seconds(self):
        value = datetime.time(13, 5, 42)
        self.assertEqual(format_time(value, "12-hour"), "1:05 PM")
        self.assertEqual(format_time(value, "24-hour"), "13:05")


class TimeLocaleTests(unittest.TestCase):
    def test_lc_all_overrides_lc_time(self):
        env = {"LC_ALL": "fr_FR.UTF-8", "LC_TIME": "de_DE.UTF-8", "LANG": "it_IT.UTF-8"}
        with patch.dict(os.environ, env, clear=True):
            self.assertEqual(default_time_locale(), "fr_FR")

    def test_lc_time_overrides_lang(self):
        env = {"LC_TIME": "de_DE.UTF-8", "LANG": "it_IT.UTF-8", "LANGUAGE": "en_US"}
        with patch.dict(os.environ, env, clear=True):
            self.assertEqual(default_time_locale(), "de_DE")

    def test_lang_overrides_language(self):
        env = {"LANG": "it_IT.UTF-8", "LANGUAGE": "en_US"}
        with patch.dict(os.environ, env, clear=True):
            self.assertEqual(default_time_locale(), "it_IT")

    def test_c_locale(self):
        with patch.dict(os.environ, {"LANG": "C.UTF-8"}, clear=True):
            self.assertEqual(default_time_locale(), "en_US_POSIX")


if __name__ == "__main__":
    unittest.main()
