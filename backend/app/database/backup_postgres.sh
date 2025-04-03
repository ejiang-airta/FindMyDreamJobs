#!/bin/bash

# Customize these as needed
DB_NAME="job_db"
DB_USER="job_user"
BACKUP_DIR="/Users/e_jiang/Projects/Job_App/dev_tracking/db_backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILENAME="${BACKUP_DIR}/${DB_NAME}_backup_${TIMESTAMP}.sql"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Create the backup using pg_dump
pg_dump -U "$DB_USER" -F p -d "$DB_NAME" > "$FILENAME"

# Optional: Keep only last 10 backups
ls -1t "$BACKUP_DIR"/*.sql | tail -n +11 | xargs rm -f

echo "✅ Backup completed: $FILENAME"