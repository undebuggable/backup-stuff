import ConfigParser
import codecs
import os.path
from optparse import OptionParser

from ..config import config as CONFIG


def config_load():
    global config
    global config_filepath
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print("Please specify one config file")
        return False
    if len(args) == 1 and not os.path.isfile(args[0]):
        print("Config file doesn't exist")
        return False
    config_filepath = args[0]
    config = ConfigParser.ConfigParser()

    # Don't convert keys to lowercase
    config.optionxform = lambda option: option

    config.readfp(codecs.open(config_filepath, "r", "utf8"))
    return True


def config_validate():
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
        and len(config.get(CONFIG.CONFIG_BACKUP_FROM, constants.CONFIG_SOURCE).strip())
        > 0
    ):
        backup_source = (
            config.get(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_SOURCE)
            .strip()
            .split("\n")
        )

    if (
        config.has_option(constants.CONFIG_BACKUP_FROM, CONFIG.CONFIG_SOURCE_COMPRESS)
        and len(
            config.get(
                constants.CONFIG_BACKUP_FROM, CONFIG.CONFIG_SOURCE_COMPRESS
            ).strip()
        )
        > 0
    ):
        backup_source_compress = (
            config.get(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_SOURCE_COMPRESS)
            .strip()
            .split("\n")
        )

    if (
        config.has_option(CONFIG.CONFIG_BACKUP_FROM, constants.CONFIG_REMOTE)
        and len(config.get(constants.CONFIG_BACKUP_FROM, CONFIG.CONFIG_REMOTE).strip())
        > 0
    ):
        backup_remote = (
            config.get(constants.CONFIG_BACKUP_FROM, constants.CONFIG_REMOTE)
            .strip()
            .split("\n")
        )

    # WARNING!!! When using mappings to avoid name collisions, rename local resources.
    # Remote resources are fetched first with original name and then renamed
    if (
        config.has_option(CONFIG.CONFIG_BACKUP_FROM, CONFIG.CONFIG_REMOTE_COMPRESS)
        and len(
            config.get(
                constants.CONFIG_BACKUP_FROM, CONFIG.CONFIG_REMOTE_COMPRESS
            ).strip()
        )
        > 0
    ):
        backup_remote_compress = (
            config.get(CONFIG.CONFIG_BACKUP_FROM, constants.CONFIG_REMOTE_COMPRESS)
            .strip()
            .split("\n")
        )

    if (
        config.has_option(CONFIG.CONFIG_RENAME, CONFIG.CONFIG_MAPPINGS)
        and len(config.get(CONFIG.CONFIG_RENAME, CONFIG.CONFIG_MAPPINGS).strip()) > 0
    ):
        mappings = (
            config.get(constants.CONFIG_RENAME, CONFIG.CONFIG_MAPPINGS)
            .strip()
            .split("\n")
        )
        # http://stackoverflow.com/questions/4576115/python-list-to-dictionary
        mappings = dict(zip(mappings[0::2], mappings[1::2]))

    if (
        config.has_option(constants.CONFIG_BACKUP_TO, CONFIG.CONFIG_DIRECTORY)
        and len(config.get(CONFIG.CONFIG_BACKUP_TO, CONFIG.CONFIG_DIRECTORY).strip())
        > 0
    ):
        backup_to_basedir = config.get(
            constants.CONFIG_BACKUP_TO, CONFIG.CONFIG_DIRECTORY
        ).strip()

    if len(backup_to_basedir) < 1:
        print("Please specify in configuration file one directory to make backup to")
        return False

    directoriesOrFiles = backup_source + backup_source_compress
    if len(directoriesOrFiles + backup_remote + backup_remote_compress) < 1:
        print(
            "Please specify in configuration file at least one local or remote directory or file to backup"
        )
        return False

    if not os.path.isdir(backup_to_basedir):
        print("Directory doesn't exist\t{}".format(backup_to_basedir))
        return False
    else:
        print("Directory exists\t{}".format(backup_to_basedir))

    for dof in directoriesOrFiles:
        if not os.path.exists(dof):
            print("Directory or file doesn't exist\t{}".format(dof))
            return False
        else:
            print("Directory or file exists\t{}".format(dof))

    for mappingKey in mappings.keys():
        if mappingKey not in (
            directoriesOrFiles + backup_remote + backup_remote_compress
        ):
            print("Incorrect rename mapping key\t{}".format(mappingKey))
            return False

    return True
