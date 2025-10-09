# Detailed Installation Guide

## Prerequisites

- Odoo 15 Community Edition
- PostgreSQL 10+ (12+ recommended)
- Ubuntu/Debian Linux
- Root or sudo access
- At least 4GB RAM (8GB+ recommended)

## Pre-Installation Checklist

- [ ] Backup your database
- [ ] Backup Odoo configuration
- [ ] Check available disk space (need ~2GB for indexes)
- [ ] Note current performance metrics (for comparison)
- [ ] Schedule during low-traffic period

## Installation Steps

### 1. Backup Everything

```bash
# Backup database
sudo su - postgres
pg_dump patro > /tmp/patro_backup_$(date +%Y%m%d).sql
exit

# Backup Odoo config
sudo cp /home/ragab/odoo/odoo15/conf/patro.conf /home/ragab/odoo/odoo15/conf/patro.conf.backup

# Backup PostgreSQL config
sudo cp /etc/postgresql/*/main/postgresql.conf /etc/postgresql/*/main/postgresql.conf.backup
```

### 2. Verify Server Resources

```bash
# Check RAM
free -h
# Should have at least 4GB total, 8GB recommended

# Check disk space
df -h
# Should have at least 10GB free in /var/lib/postgresql

# Check CPU cores
nproc
# Adjust workers in config based on cores: (cores * 2) + 1
```

### 3. Stop Odoo (Optional but Recommended)

```bash
sudo systemctl stop odoo
# OR if running manually:
# Press Ctrl+C in Odoo terminal
```

### 4. The New Config is Already Updated

The configuration file has already been updated:
- `/home/ragab/odoo/odoo15/conf/patro.conf`

Review the changes:
```bash
cat /home/ragab/odoo/odoo15/conf/patro.conf
```

### 5. Install Performance Module

```bash
cd /home/ragab/odoo/odoo15

# Install the module
./odoo-bin -c conf/patro.conf -d patro -i performance_optimization --stop-after-init
```

Expected output:
```
...
INFO patro odoo.modules.loading: Modules loaded.
INFO patro odoo.modules.registry: module performance_optimization: ...
...
```

### 6. Run Database Optimization

```bash
cd /home/ragab/odoo/odoo15/patro/performance_optimization/scripts

# Make script executable (if not already)
chmod +x optimize_database.sh

# Run optimization
./optimize_database.sh
```

This will take 5-15 minutes depending on your database size.

Expected output:
```
========================================
Odoo Database Optimization Script
========================================

Step 1: Creating Database Indexes...
✓ Indexes created

Step 2: Analyzing Tables...
✓ Tables analyzed

Step 3: Vacuuming Important Tables...
✓ Tables vacuumed

Step 4: Checking Database Statistics...
✓ Database statistics displayed

========================================
Optimization Complete!
========================================
```

### 7. Configure PostgreSQL

#### Option A: Create Separate Config File (Recommended)

```bash
# Create conf.d directory if it doesn't exist
sudo mkdir -p /etc/postgresql/*/main/conf.d

# Copy tuning config
sudo cp /home/ragab/odoo/odoo15/patro/performance_optimization/scripts/postgresql_tuning.conf \
        /etc/postgresql/*/main/conf.d/odoo_performance.conf

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### Option B: Append to Main Config

```bash
# Append tuning to main config
sudo bash -c 'cat /home/ragab/odoo/odoo15/patro/performance_optimization/scripts/postgresql_tuning.conf >> /etc/postgresql/*/main/postgresql.conf'

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### Verify PostgreSQL is Running

```bash
sudo systemctl status postgresql
# Should show "active (running)"
```

### 8. Start Odoo with New Configuration

```bash
# Start Odoo service
sudo systemctl start odoo

# Check it's running
sudo systemctl status odoo

# Monitor logs for any issues
sudo tail -f /var/log/odoo/odoo.log
```

### 9. Configure POS Performance Settings

1. Login to Odoo
2. Go to **Point of Sale → Configuration → Point of Sale**
3. Open each POS configuration
4. Navigate to **Performance Settings** tab
5. Configure:
   ```
   ✓ Limit Products to Load
   Product Load Limit: 1000
   ✓ Load Only Available Products
   
   Optional (if you have specific categories):
   Product Categories to Load: [Select specific categories]
   ```
6. Click **Save**

### 10. Test Performance

#### Test POS Session Opening

1. Go to **Point of Sale → Dashboard**
2. Click **New Session**
3. Measure time to open
4. Expected: 3-5 seconds (was 30-60 seconds)

#### Test Stock Reports

1. Go to **Inventory → Reporting → Stock Reports**
2. Run a stock report for all products
3. Measure time to generate
4. Expected: 10-15 seconds (was 60-120 seconds)

#### Test Product Search

1. In POS, search for a product by barcode
2. Expected: Instant (<0.3 seconds, was 2-5 seconds)

### 11. Configure Automatic Maintenance (Already Done)

The module automatically sets up:
- Daily database ANALYZE at 2:00 AM
- Weekly full optimization at 3:00 AM Sunday

Verify cron jobs are active:
```python
# In Odoo interface:
# Settings → Technical → Automation → Scheduled Actions
# Search for "Database"
# Should see:
# - "Database: Daily Optimization (ANALYZE)" - Active
# - "Database: Weekly Optimization (Full)" - Active
```

## Post-Installation Verification

### Check Indexes Were Created

```bash
sudo su - postgres
psql -d patro -c "SELECT indexname FROM pg_indexes WHERE tablename = 'stock_quant';"
# Should see: stock_quant_prod_loc_idx, stock_quant_loc_prod_idx, etc.
exit
```

### Check Module is Installed

```bash
# In Odoo:
# Apps → Remove "Apps" filter → Search "Performance Optimization"
# Should show as "Installed"
```

### Monitor Performance

```bash
# Watch Odoo logs
sudo tail -f /var/log/odoo/odoo.log | grep -E "stock|product|pos"

# Watch PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*-main.log | grep duration
```

## Rollback (If Needed)

If something goes wrong:

### Rollback Odoo Config

```bash
sudo cp /home/ragab/odoo/odoo15/conf/patro.conf.backup \
        /home/ragab/odoo/odoo15/conf/patro.conf
sudo systemctl restart odoo
```

### Rollback PostgreSQL Config

```bash
sudo cp /etc/postgresql/*/main/postgresql.conf.backup \
        /etc/postgresql/*/main/postgresql.conf
sudo systemctl restart postgresql
```

### Uninstall Module

```bash
cd /home/ragab/odoo/odoo15
./odoo-bin -c conf/patro.conf -d patro -u performance_optimization --stop-after-init
# Then in Odoo interface: Apps → Performance Optimization → Uninstall
```

### Restore Database

```bash
sudo su - postgres
dropdb patro
createdb patro -O odoo
psql patro < /tmp/patro_backup_YYYYMMDD.sql
exit
```

## Common Installation Issues

### Issue: "Permission denied" when running script

**Solution:**
```bash
chmod +x /home/ragab/odoo/odoo15/patro/performance_optimization/scripts/optimize_database.sh
```

### Issue: "Database connection failed"

**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
sudo su - postgres
psql -l | grep patro
exit
```

### Issue: "Module not found"

**Solution:**
```bash
# Check module is in addons path
ls -la /home/ragab/odoo/odoo15/patro/performance_optimization/

# Check addons_path in config
grep addons_path /home/ragab/odoo/odoo15/conf/patro.conf
```

### Issue: "Out of memory" during optimization

**Solution:**
```bash
# Run optimization in smaller chunks
# Comment out VACUUM steps in script
# Run ANALYZE only first, then VACUUM later
```

### Issue: "Odoo won't start after config changes"

**Solution:**
```bash
# Check config syntax
/home/ragab/odoo/odoo15/odoo-bin -c /home/ragab/odoo/odoo15/conf/patro.conf --test-enable

# Check logs
sudo tail -100 /var/log/odoo/odoo.log

# Restore backup if needed
sudo cp /home/ragab/odoo/odoo15/conf/patro.conf.backup \
        /home/ragab/odoo/odoo15/conf/patro.conf
```

## Next Steps

After successful installation:

1. ✅ Monitor performance for 24-48 hours
2. ✅ Check automatic maintenance runs correctly
3. ✅ Document your specific performance gains
4. ✅ Train users on new POS search functionality
5. ✅ Review and adjust settings based on usage patterns

## Support

For issues or questions:
- Check logs: `/var/log/odoo/odoo.log` and `/var/log/postgresql/*.log`
- Review README.md for detailed troubleshooting
- Check QUICKSTART.md for common solutions

