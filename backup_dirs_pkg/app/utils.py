import subprocess
import os
from optparse import OptionParser

def createDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
        return True
    else:
        print("The directory already exists\t{}".format(path))
        return False

def exec_shell(command):
    print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
    return stdout if len(stdout) > 0 else stderr

def exec_shell_checksum(destination_path):
    file_checksum = open(r"{}.{}".format(destination_path, "sha256"), "w")
    subprocess.Popen(
        "sha256sum {}".format(destination_path),
        stdout=file_checksum,
        shell=True
    )
    file_checksum.close()

def splitext(path):
    for ext in [CONFIG.SUFFIX_TARGZ, CONFIG.SUFFIX_TARBZ2]:
        if path.endswith(ext):
            return path[: -len(ext)], path[-len(ext) :]
    return os.path.splitext(path)

def parse_options():
    is_valid = True
    config_filepath = ""
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) != 1:
        print("[✘] No config file specified")
        is_valid=False
    if len(args) == 1:
        config_filepath = args[0]
    return {
        "is_valid": is_valid,
        "config_filepath": config_filepath
    }