# Scripts Directory

## Available Scripts

### 1. `optimize_database.sh`

**Purpose**: Creates database indexes and optimizes PostgreSQL for Odoo performance

**Usage**:
```bash
cd /home/ragab/odoo/odoo15/patro/performance_optimization/scripts
./optimize_database.sh
```

**What it does**:
- Creates 30+ database indexes on critical tables
- Runs ANALYZE on important tables (updates query planner statistics)
- Runs VACUUM on important tables (reclaims storage, reduces bloat)
- Shows database statistics and index usage

**When to run**:
- After initial module installation (required)
- When database feels slow
- After bulk data operations
- Monthly as maintenance

**Time required**: 5-15 minutes (depends on database size)

**Requirements**:
- PostgreSQL must be running
- Database user/password configured in script
- Sufficient disk space for indexes (~2GB)

---

### 2. `postgresql_tuning.conf`

**Purpose**: PostgreSQL configuration tuning for Odoo 15 with large catalogs

**Usage**:
```bash
# Option 1: Create separate config (recommended)
sudo cp postgresql_tuning.conf /etc/postgresql/*/main/conf.d/odoo_performance.conf
sudo systemctl restart postgresql

# Option 2: Append to main config
sudo bash -c 'cat postgresql_tuning.conf >> /etc/postgresql/*/main/postgresql.conf'
sudo systemctl restart postgresql
```

**What it does**:
- Increases shared buffers (PostgreSQL memory)
- Optimizes checkpoint settings
- Configures autovacuum for better maintenance
- Tunes query planner for better execution plans

**When to apply**:
- After initial module installation (recommended)
- When experiencing slow queries
- As part of production optimization

**Requirements**:
- Root or sudo access
- 8GB+ RAM recommended
- SSD storage recommended

---

## Configuration Files

### Database Settings in `optimize_database.sh`

Edit these variables if your setup is different:

```bash
DB_NAME="patro"          # Your database name
DB_USER="odoo"           # PostgreSQL user
PGPASSWORD="1"           # PostgreSQL password
```

### PostgreSQL Settings Explained

Key settings in `postgresql_tuning.conf`:

| Setting | Value | Purpose |
|---------|-------|---------|
| `shared_buffers` | 2GB | PostgreSQL memory cache |
| `effective_cache_size` | 6GB | Tells planner available OS cache |
| `work_mem` | 10MB | Memory per query operation |
| `maintenance_work_mem` | 512MB | Memory for VACUUM, CREATE INDEX |
| `random_page_cost` | 1.1 | Cost estimate for SSD |
| `max_connections` | 150 | Max database connections |

**Adjust based on your server**:
- `shared_buffers`: 25% of RAM
- `effective_cache_size`: 50-75% of RAM
- `work_mem`: (RAM × 0.25) / max_connections / 2

---

## Troubleshooting Scripts

### Script won't run: "Permission denied"

```bash
chmod +x optimize_database.sh
```

### Script fails: "Database connection failed"

Check PostgreSQL is running:
```bash
sudo systemctl status postgresql
```

Check database exists:
```bash
sudo -u postgres psql -l | grep patro
```

### Script fails: "FATAL: password authentication failed"

Edit script and update:
```bash
DB_USER="odoo"      # Your PostgreSQL user
PGPASSWORD="1"      # Your PostgreSQL password
```

### PostgreSQL won't start after config changes

Check PostgreSQL logs:
```bash
sudo tail -100 /var/log/postgresql/postgresql-*-main.log
```

Check config syntax:
```bash
sudo -u postgres /usr/lib/postgresql/*/bin/postgres -D /etc/postgresql/*/main -C config_file
```

Restore backup if needed:
```bash
sudo cp /etc/postgresql/*/main/postgresql.conf.backup \
        /etc/postgresql/*/main/postgresql.conf
sudo systemctl restart postgresql
```

---

## Best Practices

### When to Run Database Optimization

**Automatically** (already configured):
- Daily ANALYZE at 2:00 AM
- Weekly full optimization at 3:00 AM Sunday

**Manually run when**:
- After installing module (first time)
- After bulk import/delete operations
- Database feels slow
- Monthly maintenance

### Monitoring

Check if indexes are being used:
```bash
sudo -u postgres psql -d patro -c "
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC
LIMIT 20;"
```

Check slow queries:
```bash
sudo tail -f /var/log/postgresql/postgresql-*-main.log | grep -E "duration: [0-9]{4,}"
```

### Backup Before Running

Always backup before major operations:
```bash
# Backup database
sudo -u postgres pg_dump patro > /tmp/patro_backup_$(date +%Y%m%d).sql

# Backup PostgreSQL config
sudo cp /etc/postgresql/*/main/postgresql.conf \
        /etc/postgresql/*/main/postgresql.conf.backup
```

---

## Script Output Examples

### Successful Database Optimization

```
========================================
Odoo Database Optimization Script
========================================

Step 1: Creating Database Indexes...
  ✓ Created index product_product_barcode_idx on product_product(barcode)
  ✓ Created index stock_quant_prod_loc_idx on stock_quant(product_id, location_id)
  ... (30+ indexes)
✓ Indexes created

Step 2: Analyzing Tables...
  ✓ ANALYZE product_product
  ✓ ANALYZE stock_quant
  ... (8 tables)
✓ Tables analyzed

Step 3: Vacuuming Important Tables...
  ✓ VACUUM product_product
  ✓ VACUUM stock_quant
  ... (7 tables)
✓ Tables vacuumed

Step 4: Checking Database Statistics...
 schema | table              | size
--------+--------------------+----------
 public | product_product    | 284 MB
 public | stock_quant        | 156 MB
 public | stock_move         | 124 MB
 ...

========================================
Optimization Complete!
========================================
```

### After PostgreSQL Tuning

Check settings were applied:
```bash
sudo -u postgres psql -d patro -c "SHOW shared_buffers;"
# Should show: 2GB

sudo -u postgres psql -d patro -c "SHOW effective_cache_size;"
# Should show: 6GB
```

---

## Need Help?

See the main documentation:
- [README.md](../README.md) - Full documentation
- [QUICKSTART.md](../QUICKSTART.md) - 5-minute setup
- [INSTALLATION.md](../INSTALLATION.md) - Detailed installation

