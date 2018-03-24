* [TASK] unbackup utility reverting the backup based on the `ini` file
* [TASK] remote backup - check for `rsync` on remote destination, in case not present fallback to `scp`
* [IMPROVEMENT] external memory backup - do chmod 777 before (?)
* [✓|IMPROVEMENT] log the timestamps between tasks
* [REFACTOR] console strings stored in config variables
* [TASK] after successful backup prepare comprehensive report
  * [TASK] sizes of created archives (e.g. `du -sh`)
  * [TASK] checksums of created archives (md5 and sha256)
* [TASK] prepare Python `requirements.txt` for the application

