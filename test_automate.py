import io
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import requests

import automate


class MoveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.src = os.path.join(self.tmp.name, "src")
        self.dst = os.path.join(self.tmp.name, "dst")
        os.makedirs(self.src)
        os.makedirs(self.dst)
        for n in ["a.jpg", "B.JPG", "notes.txt"]:
            open(os.path.join(self.src, n), "w").close()
        open(os.path.join(self.dst, "a.jpg"), "w").close()  # clash

    def tearDown(self):
        self.tmp.cleanup()

    def test_dry_run_moves_nothing(self):
        moved = automate.move_jpgs(self.src, self.dst, dry_run=True)
        self.assertEqual(len(moved), 2)
        self.assertTrue(os.path.exists(os.path.join(self.src, "a.jpg")))

    def test_move_with_clash(self):
        automate.move_jpgs(self.src, self.dst)
        self.assertEqual(sorted(os.listdir(self.dst)), ["B.JPG", "a.jpg", "a_1.jpg"])
        self.assertEqual(os.listdir(self.src), ["notes.txt"])

    def test_missing_source(self):
        with self.assertRaises(FileNotFoundError):
            automate.move_jpgs("/nope/none", self.dst)


class EmailTests(unittest.TestCase):
    def test_extract_dedupe(self):
        text = "a@x.com, b.c@y.org; A@X.com and bad@ and d+e@z.co.uk"
        self.assertEqual(automate.extract_emails(text), ["a@x.com", "b.c@y.org", "d+e@z.co.uk"])


class TitleTests(unittest.TestCase):
    @patch("automate.requests.get")
    def test_title(self, get):
        get.return_value = MagicMock(text="<html><TITLE>\n Hello  Page </TITLE></html>")
        self.assertEqual(automate.fetch_title("http://t"), "Hello Page")
        get.assert_called_with("http://t", timeout=10)

    @patch("automate.requests.get")
    def test_no_title(self, get):
        get.return_value = MagicMock(text="<html></html>")
        with self.assertRaises(ValueError):
            automate.fetch_title("http://t")

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("automate.requests.get", side_effect=requests.Timeout())
    def test_network_error_handled(self, get, out):
        self.assertEqual(automate.main(["title", "--out", os.devnull]), 1)
        self.assertIn("Network error", out.getvalue())


if __name__ == "__main__":
    unittest.main()
