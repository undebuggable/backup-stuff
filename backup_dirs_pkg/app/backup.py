import datetime
import mimetypes
import ntpath
import os.path
import shutil
import subprocess
import time

from backup_dirs_pkg.app import config_file
from ..config import config as CONFIG


def exec_shell(command):
    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
    return stdout if len(stdout) > 0 else stderr


def splitext(path):
    for ext in [CONFIG.SUFFIX_TARGZ, CONFIG.SUFFIX_TARBZ2]:
        if path.endswith(ext):
            return path[: -len(ext)], path[-len(ext) :]
    return os.path.splitext(path)


def backupLocal(backup_to_dir):
    for fileOrDirectory in (
        config_file.backup_source + config_file.backup_source_compress
    ):
        _fileOrDirectory = fileOrDirectory.rstrip("/")
        (mimeType, encoding) = mimetypes.guess_type(_fileOrDirectory)
        print("********************")
        print("Processing\t{}".format(_fileOrDirectory))

        ts = time.time()
        print(
            "Timestamp\t{}".format(
                datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d-%H-%M-%S")
            )
        )

        head, tail = ntpath.split(_fileOrDirectory)
        if mimeType not in CONFIG.ARCHIVE_MIMETYPES:
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
            exec_shell(
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
            os.chdir(currentCwd)
        else:
            # Only copy those backup targets which are already archives
            if _fileOrDirectory in config_file.mappings.keys():
                destination_path = os.path.join(
                    backup_to_dir, config_file.mappings.get(_fileOrDirectory)
                )
            else:
                destination_path = os.path.join(backup_to_dir, tail)
            fileName, fileExtensionOriginal = splitext(tail)
            fileName, fileExtensionRenamed = splitext(destination_path)
            if fileExtensionOriginal != fileExtensionRenamed:
                destination_path += fileExtensionOriginal
            shutil.copy(_fileOrDirectory, destination_path)

        ts = time.time()
        print(
            "Timestamp\t{}".format(
                datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d-%H-%M-%S")
            )
        )


def backupRemote(backup_to_dir):
    for remoteSource in config_file.backup_remote + config_file.backup_remote_compress:

        ts = time.time()
        print(
            "Timestamp\t{}".format(
                datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d-%H-%M-%S")
            )
        )

        exec_shell(["rsync", "-az", remoteSource, backup_to_dir])
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
            exec_shell(
                [
                    "tar",
                    ("-cpf" if remoteSource in config_file.backup_remote else "-czpf"),
                    destination_path,
                    tail,
                ]
            )
            os.chdir(currentCwd)
            exec_shell(["rm", "-rf", source_path])
        else:
            if remoteSource in config_file.mappings.keys():
                source_path = os.path.join(backup_to_dir, tail)
                destination_path = os.path.join(
                    backup_to_dir, config_file.mappings.get(remoteSource)
                )
                fileName, fileExtensionOriginal = splitext(tail)
                fileName, fileExtensionRenamed = splitext(destination_path)
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
