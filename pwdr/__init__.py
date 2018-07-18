import os
import yaml
from yaml.scanner import ScannerError


YAML_CONF_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(os.path.dirname(YAML_CONF_DIR), "backup")
BACKUP_TEMP_DIR = os.path.join(os.path.dirname(YAML_CONF_DIR), "temp")


class BasePDFileError(Exception):
    pass


class UnknownFileFormat(BasePDFileError):
    def __init__(self, **kwargs):
        self.error = "Error! File format is not YAML"
        self.file = kwargs.get("file")

    def __str__(self):
        return "{}: {}".format(self.error, self.file)


class YAMLReader:
    def __init__(self, storeyml="store.yml"):
        self._storeyml = storeyml

    def _storeyml_loader(self):
        with open(os.path.join(YAML_CONF_DIR, self._storeyml), "r") as y:
            try:
                config = yaml.load(y)
                return config

            except FileNotFoundError as nf:
                raise nf

            except ScannerError:
                raise UnknownFileFormat(
                    file=os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), self._storeyml
                    )
                )

    def read(self):
        return self._storeyml_loader()


class YAMLParser(YAMLReader):
    def parse_storeyml(self):
        yaml_config = self.read()
        for n in yaml_config:
            paths = yaml_config.get(n)

            try:
                for y in paths.get("file"):
                    if y == "ALL":
                        folder = paths.get("folder")[0]
                        for line in YAMLParser._all_configs(folder):
                            yield line
                    else:
                        file = os.path.join(paths.get("folder")[0], y)
                        for line in YAMLParser._one_config(file):
                            yield line

            except TypeError:
                print(
                    "Warning: Check {}! Some strings are empty.".format(self._storeyml)
                )

    @staticmethod
    def _one_config(file):
        yield file

    @staticmethod
    def _all_configs(folder):
        for root, subdirs, files in os.walk(folder):
            for filename in files:
                yield os.path.join(root, filename)
