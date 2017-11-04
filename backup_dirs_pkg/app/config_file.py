from optparse import OptionParser
import ConfigParser, os.path, codecs
from ..config import constants

def parseConfig():    
    global config
    global configFilePath
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print "Please specify one config file"
        return False
    if len(args) == 1 and not os.path.isfile(args[0]):
        print "Config file doesn't exist"
        return False
    configFilePath = args[0]
    config = ConfigParser.ConfigParser()

    #Don't convert keys to lowercase
    config.optionxform = lambda option: option

    config.readfp(codecs.open(configFilePath, 'r', 'utf8'))
    return True

def verifyConfig():
    global backup_to_dir
    global backup_source
    global backup_source_compress
    global backup_remote
    global backup_remote_compress
    global mappings
    backup_source = []
    backup_source_compress = []
    backup_remote = []
    backup_remote_compress = []
    mappings = {}
    backup_to_dir = ''

    if config.has_option(constants.CONFIG_BACKUP_FROM,constants.CONFIG_SOURCE) and len(config.get(constants.CONFIG_BACKUP_FROM,constants.CONFIG_SOURCE).strip()) > 0:
        backup_source = config.get(constants.CONFIG_BACKUP_FROM,constants.CONFIG_SOURCE).strip().split('\n')
    
    if config.has_option(constants.CONFIG_BACKUP_FROM,constants.CONFIG_SOURCE_COMPRESS) and len(config.get(constants.CONFIG_BACKUP_FROM,constants.CONFIG_SOURCE_COMPRESS).strip()) > 0:
        backup_source_compress = config.get(constants.CONFIG_BACKUP_FROM,constants.CONFIG_SOURCE_COMPRESS).strip().split('\n')

    if config.has_option(constants.CONFIG_BACKUP_FROM, constants.CONFIG_REMOTE) and len(config.get(constants.CONFIG_BACKUP_FROM, constants.CONFIG_REMOTE).strip()) > 0:
        backup_remote = config.get(constants.CONFIG_BACKUP_FROM, constants.CONFIG_REMOTE).strip().split('\n')
    
    #WARNING!!! When using mappings to avoid name collisions, rename local resources.
    #Remote resources are fetched first with original name and then renamed
    if config.has_option(constants.CONFIG_BACKUP_FROM, constants.CONFIG_REMOTE_COMPRESS) and len(config.get(constants.CONFIG_BACKUP_FROM, constants.CONFIG_REMOTE_COMPRESS).strip()) > 0:
        backup_remote_compress = config.get(constants.CONFIG_BACKUP_FROM, constants.CONFIG_REMOTE_COMPRESS).strip().split('\n')

    if config.has_option(constants.CONFIG_RENAME, constants.CONFIG_MAPPINGS) and len(config.get(constants.CONFIG_RENAME, constants.CONFIG_MAPPINGS).strip()) > 0:
        mappings = config.get(constants.CONFIG_RENAME, constants.CONFIG_MAPPINGS).strip().split('\n')
        #http://stackoverflow.com/questions/4576115/python-list-to-dictionary
        mappings = dict(zip(mappings[0::2], mappings[1::2]))

    if config.has_option(constants.CONFIG_BACKUP_TO,constants.CONFIG_DIRECTORY) and len(config.get(constants.CONFIG_BACKUP_TO,constants.CONFIG_DIRECTORY).strip()) > 0:
        backup_to_dir = config.get(constants.CONFIG_BACKUP_TO,constants.CONFIG_DIRECTORY).strip()

    if len(backup_to_dir) < 1:
        print ('Please specify in configuration file one directory to make backup to')
        return False

    directoriesOrFiles = backup_source + backup_source_compress
    if len(directoriesOrFiles + backup_remote + backup_remote_compress) < 1:
        print ('Please specify in configuration file at least one local or remote directory or file to backup')
        return False

    if not os.path.isdir(backup_to_dir):
        print ('Directory doesn\'t exist\t' + backup_to_dir)
        return False
    else:
        print ('Directory exists\t' + backup_to_dir)

    for dof in directoriesOrFiles:
        if not os.path.exists(dof):
            print 'Directory or file doesn\'t exist\t' + dof
            return False
        else:
            print 'Directory or file exists\t' + dof

    for mappingKey in mappings.keys():
        if mappingKey not in (directoriesOrFiles + backup_remote + backup_remote_compress):
            print 'Incorrect rename mapping key\t' + mappingKey
            return False
    return True
