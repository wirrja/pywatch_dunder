from datetime import datetime
import logging
import os
import shutil
import yaml
from yaml.scanner import ScannerError


YAML_CONF_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SETTINGS"
)
BACKUP_DIR = os.path.join(os.path.dirname(YAML_CONF_DIR), "backup")
LOGDIR = os.path.join(os.path.dirname(YAML_CONF_DIR), "logs")
LOGFILE = os.path.join(
    LOGDIR, "{}".format(datetime.strftime(datetime.now(), "%Y-%m-%d.log"))
)

logging.basicConfig(
    format="%(asctime)s %(message)s",
    filename=LOGFILE,
    filemode="a",
    datefmt="%H:%M:%S",
    level=logging.WARNING,
)


class BaseError(Exception):
    pass


class UnknownFileFormat(BaseError):
    def __init__(self, **kwargs):
        self.error = "Error! File format is not YAML"
        self.file = kwargs.get("file")

    def __str__(self):
        return "{}: {}".format(self.error, self.file)


class YAMLReader:
    def __init__(self, ymlfile="store.yml"):
        self._ymlfile = ymlfile

    def parse_yml(self):
        yml_config = self._yml_loader()
        for n in yml_config:
            paths = yml_config.get(n)
            try:
                for y in paths.get("file"):
                    if y == "ALL":
                        folder = paths.get("folder")[0]
                        for line in self._all_configs(folder):
                            yield line
                    else:
                        file = os.path.join(paths.get("folder")[0], y)
                        for line in self._one_config(file):
                            yield line

            except TypeError:
                print(
                    "Warning: Check {}! Some strings are empty.".format(self._ymlfile)
                )

    def _yml_loader(self):
        with open(os.path.join(YAML_CONF_DIR, self._ymlfile), "r") as y:
            try:
                config = yaml.load(y)
                return config

            except ScannerError:
                raise UnknownFileFormat(
                    file=os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), self._ymlfile
                    )
                )

    @staticmethod
    def _one_config(file):
        if os.path.exists(file):
            logging.info("SUCCESS {}".format(file))
            yield file
        else:
            logging.warning("FILE NOT FOUND {}".format(file))

    @staticmethod
    def _all_configs(folder):
        if os.path.exists(folder):
            for root, subdirs, files in os.walk(folder):
                for filename in files:
                    logging.info("SUCCESS {}{}".format(root, filename))
                    yield os.path.join(root, filename)
        else:
            logging.warning("FOLDER NOT FOUND {}".format(folder))


def _local_backup(path, backup_folder=BACKUP_DIR):
    """
    Copy file from path with all metadata and rights
    to backup_folder
    """
    os.makedirs(
        os.path.join(os.path.join(backup_folder + os.path.dirname(path))), exist_ok=True
    )
    shutil.copy2(
        path, os.path.join(backup_folder + os.path.abspath(path)), follow_symlinks=True
    )


class PWDRBackup:
    def __init__(self, path, backup_folder=BACKUP_DIR):
        self.folder = backup_folder
        self.path = path

    def backup(self):
        return _local_backup(self.path, self.folder)