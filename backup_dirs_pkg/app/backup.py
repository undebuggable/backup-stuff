import ConfigParser, os.path, codecs, time, datetime, subprocess, zipfile, mimetypes, shutil, ntpath
from ..config import constants

def exec_shell(command):
  print command
  p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  (stdout, stderr) = p.communicate()
  print stdout
  print stderr
  return stdout if len(stdout) > 0 else stderr

#http://stackoverflow.com/questions/16976192/whats-the-way-to-extract-file-extension-from-file-name-in-python
def splitext(path):
    for ext in [constants.SUFFIX_TARGZ, constants.SUFFIX_TARBZ2]:
        if path.endswith(ext):
            return path[:-len(ext)], path[-len(ext):]
    return os.path.splitext(path)

def backupLocal():
    for fileOrDirectory in backup_source + backup_source_compress:
        (mimeType, encoding) = mimetypes.guess_type(fileOrDirectory)
        print 'Processing\t' + fileOrDirectory
        head, tail = ntpath.split(fileOrDirectory)
        if mimeType not in constants.ARCHIVE_MIMETYPES:
            source_path = fileOrDirectory.replace(os.path.dirname(fileOrDirectory), '')[1::]
            if fileOrDirectory in mappings.keys():
                destination_path = os.path.join(
                    backup_to_dir, mappings.get(fileOrDirectory)
                )
            else:
                destination_path = os.path.join(backup_to_dir, tail)
            destination_path += (constants.SUFFIX_TAR if fileOrDirectory in backup_source else constants.SUFFIX_TARGZ)
            currentCwd = os.getcwd()
            os.chdir(os.path.dirname(fileOrDirectory))
            exec_shell([
                'tar',
                ('-cpf' if fileOrDirectory in backup_source else '-czpf'),
                destination_path,
                source_path
            ])
            os.chdir(currentCwd)
        else:
            if fileOrDirectory in mappings.keys():
                destination_path = os.path.join(
                    backup_to_dir, mappings.get(fileOrDirectory)
                )
            else:
                destination_path = os.path.join(backup_to_dir, tail)
            fileName, fileExtensionOriginal = splitext(tail)
            fileName, fileExtensionRenamed = splitext(destination_path)
            if fileExtensionOriginal != fileExtensionRenamed:
                destination_path += fileExtensionOriginal
            shutil.copy(
                fileOrDirectory,
                destination_path
            )

def backupRemote():
    for remoteSource in (backup_remote + backup_remote_compress):
        exec_shell([
            'rsync',
            '-az',
            remoteSource,
            backup_to_dir
        ])
        (head, tail) = ntpath.split(remoteSource)
        (mimeType, encoding) = mimetypes.guess_type(remoteSource)
        if mimeType not in constants.ARCHIVE_MIMETYPES:
            source_path = os.path.join(backup_to_dir, tail)
            if remoteSource in mappings.keys():
                destination_path = os.path.join(
                    backup_to_dir, mappings.get(remoteSource)
                )
            else:
                destination_path = os.path.join(backup_to_dir, tail)
            destination_path += (constants.SUFFIX_TAR if remoteSource in backup_remote else constants.SUFFIX_TARGZ)
            currentCwd = os.getcwd()
            os.chdir(backup_to_dir)
            exec_shell([
                'tar',
                ('-cpf' if remoteSource in backup_remote else '-czpf'),
                destination_path,
                tail
            ])
            os.chdir(currentCwd)
            exec_shell([
                'rm',
                '-rf',
                source_path
            ])
        else:
            if remoteSource in mappings.keys():
                source_path = os.path.join(
                    backup_to_dir, tail
                )
                destination_path = os.path.join(
                    backup_to_dir, mappings.get(remoteSource)
                )
                fileName, fileExtensionOriginal = splitext(tail)
                fileName, fileExtensionRenamed = splitext(destination_path)
                if fileExtensionOriginal != fileExtensionRenamed:
                    destination_path += fileExtensionOriginal
                print source_path
                print destination_path
                os.rename(source_path, destination_path)
