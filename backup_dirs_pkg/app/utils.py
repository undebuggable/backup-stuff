import subprocess

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
