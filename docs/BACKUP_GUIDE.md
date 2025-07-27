# CareView Backup & Restore Guide

## 🏥 For Care Home IT Staff

This guide covers how to backup and restore the CareView database during deployment.

---

## 📋 Quick Reference

**Create Backup**: `./backup.bat`  
**Restore Backup**: `psql -h localhost -U admin -d postgres -f backups/careview_backup_YYYYMMDD_HHMMSS.sql`

---

## 🔄 Creating Backups

### Automatic Backup
```bash
# Make script executable (first time only)
chmod +x backup.sh

# Run backup./backup.sh
```

### Manual Backup
```bash
# If backup.sh doesn't work, use direct command:
pg_dump -h localhost -U admin -d careview --clean --create > manual_backup.sql
```

---

## 📁 Backup Files

**Location**: `backups/` directory  
**Format**: `careview_backup_YYYYMMDD_HHMMSS.sql`  
**Retention**: Automatically keeps last 7 days  

**Example files**:
- `careview_backup_20250119_140530.sql` (Jan 19, 2025 at 2:05:30 PM)
- `careview_backup_20250120_090000.sql` (Jan 20, 2025 at 9:00:00 AM)

---

## 🔧 Restoring Data

### ⚠️ Important Notes
- **Stop the API first**: `Ctrl+C` in the terminal running CareView
- **Backup current data** before restoring
- **Database will be recreated** (all current data lost)

### Restore Steps

1. **Stop CareView API**
   ```bash
   # Press Ctrl+C in terminal running: uvicorn main:app --reload
   ```

2. **Choose backup file**
   ```bash
   # List available backups
   ls -la backups/
   
   # Example output:
   # careview_backup_20250119_140530.sql
   # careview_backup_20250120_090000.sql
   ```

3. **Restore database**
   ```bash
   # Replace FILENAME with actual backup file
   psql -h localhost -U admin -d postgres -f backups/FILENAME.sql
   
   # Example:
   psql -h localhost -U admin -d postgres -f backups/careview_backup_20250119_140530.sql
   ```

4. **Restart CareView API**
   ```bash
   uvicorn main:app --reload
   ```

5. **Test system**
   - Open browser: http://localhost:8000/health
   - Try logging in with demo accounts

---

## 🚨 Emergency Procedures

### If Backup Script Fails
```bash
# Direct backup command
export PGPASSWORD="MySecurePass123"
pg_dump -h localhost -U admin -d careview > emergency_backup.sql
unset PGPASSWORD
```

### If Restore Fails
```bash
# 1. Check if database exists
psql -h localhost -U admin -l

# 2. Drop and recreate database if needed
psql -h localhost -U admin -d postgres -c "DROP DATABASE IF EXISTS careview;"
psql -h localhost -U admin -d postgres -c "CREATE DATABASE careview;"

# 3. Try restore again
psql -h localhost -U admin -d careview -f backups/FILENAME.sql
```

### If PostgreSQL Tools Missing
```bash
# Ubuntu/Debian
sudo apt-get install postgresql-client

# macOS with Homebrew
brew install postgresql

# Windows
# Download from: https://www.postgresql.org/download/windows/
```

---

## 📅 Recommended Schedule

**During Care Home Deployment**:
- **Daily backups** before staff start work
- **Before any major changes** (new users, bulk data entry)
- **End of each day** to capture all visits/schedules

**Commands**:
```bash
# Add to daily routine
./backup.sh
```

---

## ✅ Testing Your Backup

### Quick Test
```bash
# 1. Check backup file was created
ls -la backups/

# 2. Check file size (should be > 0 bytes)
du -h backups/careview_backup_*.sql

# 3. Check file contains data
head -20 backups/careview_backup_*.sql
# Should see SQL commands like "CREATE DATABASE", "CREATE TABLE", etc.
```

### Full Test (Optional)
```bash
# 1. Create test database
psql -h localhost -U admin -d postgres -c "CREATE DATABASE careview_test;"

# 2. Restore backup to test database
psql -h localhost -U admin -d careview_test -f backups/FILENAME.sql

# 3. Check tables exist
psql -h localhost -U admin -d careview_test -c "\dt"

# 4. Clean up test database
psql -h localhost -U admin -d postgres -c "DROP DATABASE careview_test;"
```

---


**If you need help**:
1. Check this guide first
2. Look for error messages in terminal
3. Contact system administrator 07715278067

**Common issues**:
- ❌ "pg_dump: command not found" → Install PostgreSQL client tools
- ❌ "permission denied" → Run `chmod +x backup.sh`
- ❌ "connection refused" → Check database is running
- ❌ "authentication failed" → Check credentials in .env file