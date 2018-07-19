#!/usr/bin/env python

import unittest
from pwdr import YAMLReader, PWDRBackup, UnknownFileFormat, YAML_CONF_DIR, BACKUP_DIR
import os.path


class TestYAMLReader(unittest.TestCase):
    def test_config_not_found(self):
        with self.assertRaises(FileNotFoundError):
            YAMLReader(ymlfile="blabla.yml")._yml_loader()

    def test_config_not_yaml(self):
        with self.assertRaises(UnknownFileFormat):
            YAMLReader(ymlfile="incorrect.yml")._yml_loader()

    def test_config_is_ok(self):
        real_result = str()
        # monkeypatching, need $HOME var in yml file
        test_result = os.path.join("./SETTINGS", "test.yml")
        for n in YAMLReader(ymlfile="test.yml").parse_yml():
            real_result = n

        self.assertEqual(real_result, test_result)

    def test_parse_ymlfile_one_config(self):
        test_result = os.path.join(YAML_CONF_DIR, "test.yml")
        real_result = str()
        for n in YAMLReader._one_config(test_result):
            real_result = n

        self.assertEqual(test_result, real_result)

    def test_parse_ymlfile_all_configs(self):
        test_folder_results = [
            os.path.join(YAML_CONF_DIR, "incorrect.yml"),
            os.path.join(YAML_CONF_DIR, "store.yml"),
            os.path.join(YAML_CONF_DIR, "test.yml"),
        ]
        real_folder_results = []

        for n in YAMLReader._all_configs(YAML_CONF_DIR):
            real_folder_results.append(n)
        self.assertEqual(test_folder_results, sorted(real_folder_results))

class TestPWDRBackup(unittest.TestCase):
    def test_backup(self):
        PWDRBackup(
            os.path.join(
                os.path.dirname(BACKUP_DIR), "pwdr/__init__.py"
            )).backup()

        test_state = os.path.isfile(os.path.join(BACKUP_DIR + os.path.dirname(BACKUP_DIR), 'pwdr/__init__.py'))
        self.assertTrue(test_state)

if __name__ == "__main__":
    unittest.main()
