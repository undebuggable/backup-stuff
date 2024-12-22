import configparser as ConfigParser
import codecs
import os.path

from ..config import config as CONFIG

def config_load():
    global backup_source
    global backup_source_compress
    global backup_remote
    global backup_remote_compress
    global mappings
    global backup_to_basedir
    backup_source = []
    backup_source_compress = []
    backup_remote = []
    backup_remote_compress = []
    mappings = {}
    backup_to_basedir = ""
    if (
        config.has_option(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_SOURCE)
        and len(config.get(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_SOURCE).strip()) > 0
    ):
        backup_source = (
            config.get(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_SOURCE)
            .strip()
            .split("\n")
        )

    if (
        config.has_option(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_SOURCE_COMPRESS)
        and len(
            config.get(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_SOURCE_COMPRESS).strip()
        )
        > 0
    ):
        backup_source_compress = (
            config.get(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_SOURCE_COMPRESS)
            .strip()
            .split("\n")
        )

    if (
        config.has_option(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_REMOTE)
        and len(config.get(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_REMOTE).strip()) > 0
    ):
        backup_remote = (
            config.get(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_REMOTE)
            .strip()
            .split("\n")
        )

    # [NOTE] When using mappings to avoid name collisions, rename the local resources.
    # Remote resources are fetched first with original name and then renamed.
    if (
        config.has_option(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_REMOTE_COMPRESS)
        and len(
            config.get(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_REMOTE_COMPRESS).strip()
        )
        > 0
    ):
        backup_remote_compress = (
            config.get(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_REMOTE_COMPRESS)
            .strip()
            .split("\n")
        )

    if (
        config.has_option(CONFIG.CONFIG_RENAME, CONFIG.CONFIG_MAPPINGS)
        and len(config.get(CONFIG.CONFIG_RENAME, CONFIG.CONFIG_MAPPINGS).strip()) > 0
    ):
        mappings = (
            config.get(CONFIG.CONFIG_RENAME, CONFIG.CONFIG_MAPPINGS).strip().split("\n")
        )
        mappings = dict(zip(mappings[0::2], mappings[1::2]))

    if (
        config.has_option(CONFIG.CONFIG_BACKUP_TO, CONFIG.CONFIG_DIRECTORY)
        and len(config.get(CONFIG.CONFIG_BACKUP_TO, CONFIG.CONFIG_DIRECTORY).strip())
        > 0
    ):
        backup_to_basedir = config.get(
            CONFIG.CONFIG_BACKUP_TO, CONFIG.CONFIG_DIRECTORY
        ).strip()
    return True

def config_validate():
    is_valid = True
    directoriesOrFiles = backup_source + backup_source_compress
    if len(directoriesOrFiles + backup_remote + backup_remote_compress) < 1:
        print(CONFIG.UI_NO_TARGETS)
        is_valid = False

    if not os.path.isdir(backup_to_basedir):
        print(CONFIG.UI_NO_DIR.format(backup_to_basedir))
        is_valid = False
    else:
        print(CONFIG.UI_DIR_OK.format(backup_to_basedir))

    for dof in directoriesOrFiles:
        if not os.path.exists(dof):
            print(CONFIG.UI_NO_DIR_FILE.format(dof))
            is_valid = False
        else:
            print(CONFIG.UI_DIR_FILE_OK.format(dof))

    for mappingKey in mappings.keys():
        if mappingKey not in (
            directoriesOrFiles + backup_remote + backup_remote_compress
        ):
            print(CONFIG.UI_FAIL_MAPPING.format(mappingKey))
            is_valid = False
    return is_valid

def config_open(config_filepath):
    global config
    if not os.path.isfile(config_filepath):
        print(CONFIG.UI_NO_FILE.format(config_filepath))
        return False
    config = ConfigParser.ConfigParser()
    # Don't convert keys to lowercase
    config.optionxform = lambda option: option
    config.read_file(codecs.open(config_filepath, "r", "utf8"))
    return True

