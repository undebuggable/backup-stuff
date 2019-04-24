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

UI_ = "Try again"
UI_ = "The directory already exists"
UI_ = "The backup destination directory already exists:"
UI_ = "Please specify one config file"
UI_ = "Config file doesn't exist"
UI_ = "Please specify in configuration file one directory to make backup to"
UI_ = "Please specify in configuration file at least one local or remote directory or file to backup"
UI_ = "Directory doesn't exist"
UI_ = "Directory exists\t"
UI_ = "Directory or file doesn't exist"
UI_ = "Directory or file exists"
UI_ = "Incorrect rename mapping key"
