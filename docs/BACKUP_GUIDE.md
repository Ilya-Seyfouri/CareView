
## CareView Backup & Restore Instructions




# For Care Home IT Staff

This document explains how to back up and restore the CareView database using the backup.bat script.





# Quick Reference

Run backup: Double-click backup.bat or run it from the command line (cmd)




# Restore backup:

psql -h localhost -U admin -d postgres -f backups\careview_backup_YYYYMMDD_HHMMSS.sql





# How to Back Up

Run the backup.bat script. It will:

- Load database settings from the .env file if available

- Create a backups folder if one doesn’t exist

- Generate a timestamped SQL backup file in backups\

- The backup file will be named like:
# careview_backup_20250119_140530.sql

If pg_dump is missing, the script will notify you and stop.
You’ll need to install the PostgreSQL client tools to proceed.




# Backup File Details

- Location: backups\ folder
- Filename format: careview_backup_YYYYMMDD_HHMMSS.sql

Files include the entire CareView database with commands to drop and recreate tables




# How to Restore
Before restoring:

Stop the CareView API (Ctrl+C in the terminal where it's running)
Backup any current data, just in case




# Restore command:
psql -h localhost -U admin -d postgres -f backups\FILENAME.sql
Replace FILENAME.sql with the actual backup filename.




# Troubleshooting
If you get "pg_dump not found", install PostgreSQL client tools:
https://www.postgresql.org/download/windows/

If backup files look suspiciously small (<1KB), check the backup_error.log file in the same folder.

Ensure the .env file is correctly set up with your DB credentials, or the script will use default values.




# Notes
Your DB password is set temporarily during the backup to avoid prompts and cleared afterward.

The backup includes tables like users, clients, schedules, visit_logs, and audit_logs.



# Need Help?
Read this guide
Check for error messages on screen or in backup_error.log
Contact your system admin at 07715278067 if problems persist
