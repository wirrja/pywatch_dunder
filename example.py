#!/usr/bin/env python
import os
import shutil
from pwdr import YAMLReader, BACKUP_DIR

def backup(path):
    os.makedirs(
        os.path.join(os.path.join(BACKUP_DIR + os.path.dirname(path))), exist_ok=True
    )
    shutil.copy2(
        path, os.path.join(BACKUP_DIR + os.path.abspath(path)), follow_symlinks=True
    )


if __name__ == "__main__":
    parser = YAMLReader().parse_yml()
    for path in parser:
        backup(path)
