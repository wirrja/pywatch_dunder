#!/usr/bin/env python
import unittest
from pywatch_dunder.pd_config import YAMLReader, YAMLParser, UnknownFileFormat


class TestYAMLReader(unittest.TestCase):
    def setUp(self):
        self.func = YAMLReader()

    def test_config_not_found(self):
        with self.assertRaises(FileNotFoundError):
            YAMLReader(storeyml="blabla.yml").read()

    def test_config_not_yaml(self):
        with self.assertRaises(UnknownFileFormat):
            YAMLReader(storeyml="incorrect.yml").read()

    def test_config_is_ok(self):
        self.assertEqual(
            YAMLReader(storeyml="test.yml").read(),
            {
                "home": {
                    "file": [".inputrc", ".bashrc", ".bash_history"],
                    "folder": ["/home/wirr/"],
                }
            },
        )


class TestYAMLParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_config_not_found(self):
        with self.assertRaises(FileNotFoundError):
            YAMLParser(storeyml="blabla.yml`").read()

    def test_config_not_yaml(self):
        with self.assertRaises(UnknownFileFormat):
            YAMLParser(storeyml="incorrect.yml").read()

    def test_config_is_ok(self):
        self.assertEqual(
            YAMLParser(storeyml="test.yml").read(),
            {
                "home": {
                    "file": [".inputrc", ".bashrc", ".bash_history"],
                    "folder": ["/home/wirr/"],
                }
            },
        )

    def test_parse_storeyml(self):
        test_folder_results = [
            "/etc/postgresql/10/main/pg_ident.conf",
            "/etc/postgresql/10/main/pg_hba.conf",
            "etc/postgresql/10/main/postgresql.conf",
            "/etc/postgresql/10/main/start.conf",
            "/etc/postgresql/10/main/pg_ctl.conf",
            "/etc/postgresql/10/main/environment",
        ]
        for n in YAMLParser._all_configs("/etc/postgresq/10/main/"):
            for y in test_folder_results:
                self.assertEqual(n, y)


if __name__ == "__main__":
    unittest.main()
