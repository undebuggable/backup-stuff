* [TASK] unbackup utility reverting the backup based on the `ini` file
* [TASK] remote backup - check for `rsync` on remote destination, in case not present fallback to `scp`
* [IMPROVEMENT] external memory backup - do chmod 777 before (?)
* [REFACTOR] console strings stored in config variables
* [TASK] after successful backup prepare comprehensive report
  * [TASK] sizes of created archives (e.g. `du -sh`)
  * [TASK] checksums of created archives (md5 and sha256)
* [TASK] prepare Python `requirements.txt` for the application
* [TASK] create unit tests
* [TASK] create Makefile redirecting stdout and stdin into logs, linting the source code, etc
* [TASK] `chunk/split/fat32` configuration option - splitting the output archive into smaller chunks allowing to copy the entire backup onto e.g. `fat32` formatted USB drive
* [REFACTOR] parse the command line arguments for the `backup.py` outside of the package
* [TASK] Prompt for ssh key password and add the keys to the keyring (`ssh-add`) of remote sources before starting the backup
