from distutils.core import setup

setup(
    name="backup_dirs",
    version="0.0.0.0",
    author="Pawel Owczarek",
    packages=["backup_dirs_pkg", "backup_dirs_pkg.app", "backup_dirs_pkg.config", "backup_dirs_pkg.test"],
    description="Configurable utility for automated backup of local and remote directories and files.",
)
