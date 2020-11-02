import datetime
import mimetypes
import ntpath
import os.path
import shutil
import time

from backup_dirs_pkg.app import config_file
from backup_dirs_pkg.app import utils
from backup_dirs_pkg.config import config as CONFIG


def backup_local_compress(_fileOrDirectory, backup_to_dir):
    head, tail = ntpath.split(_fileOrDirectory)
    source_path = _fileOrDirectory.replace(
        os.path.dirname(_fileOrDirectory), ""
    )[1::]
    if _fileOrDirectory in config_file.mappings.keys():
        destination_path = os.path.join(
            backup_to_dir, config_file.mappings.get(_fileOrDirectory)
        )
    else:
        destination_path = os.path.join(backup_to_dir, tail)
    destination_path += (
        CONFIG.SUFFIX_TAR
        if _fileOrDirectory in config_file.backup_source
        else CONFIG.SUFFIX_TARGZ
    )
    currentCwd = os.getcwd()
    os.chdir(os.path.dirname(_fileOrDirectory))
    utils.exec_shell(
        [
            "tar",
            (
                "-cpf"
                if _fileOrDirectory in config_file.backup_source
                else "-czpf"
            ),
            destination_path,
            source_path,
        ]
    )
    utils.exec_shell_checksum(destination_path)
    os.chdir(currentCwd)

def backup_local_binary(_fileOrDirectory, backup_to_dir):
    head, tail = ntpath.split(_fileOrDirectory)
    # Only copy those backup targets which are already archives
    if _fileOrDirectory in config_file.mappings.keys():
        destination_path = os.path.join(
            backup_to_dir, config_file.mappings.get(_fileOrDirectory)
        )
    else:
        destination_path = os.path.join(backup_to_dir, tail)
    fileName, fileExtensionOriginal = utils.splitext(tail)
    fileName, fileExtensionRenamed = utils.splitext(destination_path)
    if fileExtensionOriginal != fileExtensionRenamed:
        destination_path += fileExtensionOriginal
    shutil.copy(_fileOrDirectory, destination_path)

def backup_local(backup_to_dir):
    for fileOrDirectory in (
        config_file.backup_source + config_file.backup_source_compress
    ):
        _fileOrDirectory = fileOrDirectory.rstrip("/")
        (mimeType, encoding) = mimetypes.guess_type(_fileOrDirectory)
        print("********************")
        print("[→] Processing\t{}".format(_fileOrDirectory))

        ts = time.time()
        print(
            "Timestamp\t{}".format(
                datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d-%H-%M-%S")
            )
        )

        if mimeType not in CONFIG.ARCHIVE_MIMETYPES:
            backup_local_compress(_fileOrDirectory, backup_to_dir)
        else:
            backup_local_binary(_fileOrDirectory, backup_to_dir)
        ts = time.time()
        print(
            "Timestamp\t{}".format(
                datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d-%H-%M-%S")
            )
        )


def backup_remote(backup_to_dir):
    for remoteSource in config_file.backup_remote + config_file.backup_remote_compress:

        ts = time.time()
        print(
            "Timestamp\t{}".format(
                datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d-%H-%M-%S")
            )
        )

        utils.exec_shell(["rsync", "-az", remoteSource, backup_to_dir])
        (head, tail) = ntpath.split(remoteSource)
        (mimeType, encoding) = mimetypes.guess_type(remoteSource)
        if mimeType not in CONFIG.ARCHIVE_MIMETYPES:
            source_path = os.path.join(backup_to_dir, tail)
            if remoteSource in config_file.mappings.keys():
                destination_path = os.path.join(
                    backup_to_dir, config_file.mappings.get(remoteSource)
                )
            else:
                destination_path = os.path.join(backup_to_dir, tail)
            destination_path += (
                CONFIG.SUFFIX_TAR
                if remoteSource in config_file.backup_remote
                else CONFIG.SUFFIX_TARGZ
            )
            currentCwd = os.getcwd()
            os.chdir(backup_to_dir)
            utils.exec_shell(
                [
                    "tar",
                    ("-cpf" if remoteSource in config_file.backup_remote else "-czpf"),
                    destination_path,
                    tail,
                ]
            )
            os.chdir(currentCwd)
            utils.exec_shell(["rm", "-rf", source_path])
        else:
            if remoteSource in config_file.mappings.keys():
                source_path = os.path.join(backup_to_dir, tail)
                destination_path = os.path.join(
                    backup_to_dir, config_file.mappings.get(remoteSource)
                )
                fileName, fileExtensionOriginal = utils.splitext(tail)
                fileName, fileExtensionRenamed = utils.splitext(destination_path)
                if fileExtensionOriginal != fileExtensionRenamed:
                    destination_path += fileExtensionOriginal
                print(source_path)
                print(destination_path)
                os.rename(source_path, destination_path)

        ts = time.time()
        print(
            "Timestamp\t{}".format(
                datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d-%H-%M-%S")
            )
        )

def run():
    options_parse = utils.parse_options()
    if options_parse["is_valid"] and config_file.config_open(options_parse["config_filepath"]) and config_file.config_load() and config_file.config_validate():
        ts = time.time()
        backup_to_dir = os.path.join(
            config_file.backup_to_basedir,
            datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d-%H-%M-%S"),
        )
        if utils.createDir(backup_to_dir):
            shutil.copy(options_parse["config_filepath"], backup_to_dir)
            backup_local(backup_to_dir)
            backup_remote(backup_to_dir)
        else:
            print(
                "The backup destination directory already exists:\n{}".format(backup_to_dir)
            )
    else:
        print("Try again")

run()