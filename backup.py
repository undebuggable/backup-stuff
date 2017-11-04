import time, datetime, shutil
from backup_dirs_pkg.app import backup as backup_dirs
from backup_dirs_pkg.app import config_file
from backup_dirs_pkg.config import constants

def createDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
        return True
    else:
        print 'The directory already exists\t' + path
        return False

def backup():
    global backup_to_dir
    ts = time.time()
    backup_to_dir += '/' + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
    if createDir(backup_to_dir):
        backup_dirs.backupLocal()
        backup_dirs.backupRemote()
    else:
        print 'The backup destination directory already exists:\n' + backup_to_dir

if config_file.parseConfig() and config_file.verifyConfig():
    backup()
    shutil.copy(
        configFilePath,
        backup_to_dir
    )

else:
    print 'Try again'
