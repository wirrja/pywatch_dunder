#!/usr/bin/env python
from pwdr import YAMLReader, BACKUP_DIR, PWDRBackup
backup_folder = '/home/wirr/code/python/pywatch_dunder/backup/'

if __name__ == "__main__":
    parser = YAMLReader().parse_yml()
    for path in parser:
        pwdr = PWDRBackup(path, backup_folder=backup_folder)
        pwdr.backup()
