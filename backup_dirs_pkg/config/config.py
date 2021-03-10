# -*- coding: utf-8 -*-

CONFIG_BACKUP_TO = "backup_to"
CONFIG_BACKUP_FROM = "backup_from"
CONFIG_RENAME = "rename"
CONFIG_DIRECTORY = "dir"
CONFIG_SOURCE = "source"
CONFIG_SOURCE_COMPRESS = "source_compress"
CONFIG_REMOTE = "remote_source"
CONFIG_REMOTE_COMPRESS = "remote_source_compress"
CONFIG_MAPPINGS = "mappings"

BACKUP_TO_KEYS = [CONFIG_DIRECTORY]

BACKUP_FROM_KEYS = [CONFIG_SOURCE, CONFIG_SOURCE_COMPRESS]

ARCHIVE_MIMETYPES = [
    "application/x-tar",
    "application/zip",
    "application/gzip",
    "application/x-7z-compressed",
    "application/x-rar-compressed",
    "application/x-7z-compressed",
]

SUFFIX_TAR = ".tar"
SUFFIX_TARGZ = ".tar.gz"
SUFFIX_TARBZ2 = ".tar.bz2"

DATETIME_FORMATTING="%Y-%m-%d-%H-%M-%S"

UI_SPACER = "********************"
UI_PROCESSING = "[→] Processing\t{}"
UI_TIMESTAMP = "[i] Timestamp\t{}"
UI_DIR_EXISTS = "[✘] The directory already exists:\n{}"
UI_DIR_OK = "[✔] The backup target directory exists\t{}"
UI_DIR_FILE_OK = "[✔] Directory or file exists\t{}"
UI_CONFIGURATION_FAIL="[✘] Configuration error"
UI_NO_CONFIG = "[✘] No config file specified"
UI_NO_TARGETS = "[✘] Nothing to backup in config file"
UI_NO_DIR = "[✘] The directory doesn't exist\t{}"
UI_NO_FILE = "[✘] File doesn't exist\t{}"
UI_NO_DIR_FILE = "[✘] Directory or file doesn't exist\t{}"
UI_FAIL_MAPPING = "[✘] Incorrect rename mapping key\t{}"