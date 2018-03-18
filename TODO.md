* [TASK] unbackup utility reverting the backup based on the `ini` file
* [TASK] remote backup - check if `rsync` is available on remote destination, when not fallback to `scp`
* [IMPROVEMENT] external memory backup - do chmod 777 before
* [✓|IMPROVEMENT] log the timestamps between tasks
* [IMPROVEMENT] console strings stored in config variables
* [TASK] after successful backup prepare comprehensive report
  * sizes of created archives (e.g. `du -sh`)
  * checksums of created archives (md5 and sha256)
* [TASK] prepare Python `requirements.txt` for the application
