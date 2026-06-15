#!/usr/bin/env bash
# backup.sh — backs up the SQLite database to a timestamped file
set -euo pipefail

DB_PATH="${DB_PATH:-/tmp/interview.db}"
BACKUP_DIR="${BACKUP_DIR:-/tmp/backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/interview_${TIMESTAMP}.db"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }

log "Starting backup of '${DB_PATH}'"

if [[ ! -f "${DB_PATH}" ]]; then
  log "ERROR: Database file '${DB_PATH}' does not exist"
  exit 1
fi

mkdir -p "${BACKUP_DIR}"

sqlite3 "${DB_PATH}" ".backup '${BACKUP_FILE}'" || {
  log "ERROR: Backup failed"
  exit 1
}

# Verify backup is not empty
if [[ ! -s "${BACKUP_FILE}" ]]; then
  log "ERROR: Backup file is empty — something went wrong"
  rm -f "${BACKUP_FILE}"
  exit 1
fi

log "Backup successful: ${BACKUP_FILE} ($(du -h "${BACKUP_FILE}" | cut -f1))"

# Retain only the last 7 backups
find "${BACKUP_DIR}" -name "interview_*.db" -type f | sort | head -n -7 | xargs -r rm -f
log "Old backups pruned. Remaining: $(find "${BACKUP_DIR}" -name "interview_*.db" | wc -l)"
