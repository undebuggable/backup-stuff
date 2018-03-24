Configurable utility for automated backup of local and remote directories and files
=================

Introduction
------------------

This utility allows configurable automated backups of local and remote directories and files. The configuration is loaded from an INI file. Example backup command using the `backup.example.ini` configuration file:

`python backup.py backup.example.ini`

Supported configuration features
--------------
- backup local directory or file (`source`)
- backup and compress local directory or file (`source_compress`)
- backup remote directory or file (`remote_source`)
- backup and compress remote directory or file (`remote_source_compress`)
- rename the backup archive (`mappings`)
