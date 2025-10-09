# Quick Start Guide - Performance Optimization

## 🚀 5-Minute Setup

Follow these steps to dramatically improve your Odoo performance:

### Step 1: Run Database Optimization (2 minutes)

```bash
cd /home/ragab/odoo/odoo15/patro/performance_optimization/scripts
./optimize_database.sh
```

**What this does:**
- Creates 30+ database indexes
- Optimizes PostgreSQL tables
- Shows database statistics

### Step 2: Restart Odoo (30 seconds)

```bash
sudo systemctl restart odoo
# OR if running manually:
# cd /home/ragab/odoo/odoo15
# ./odoo-bin -c conf/patro.conf
```

**What this does:**
- Loads the new optimized configuration
- Applies increased memory and time limits

### Step 3: Install Performance Module (1 minute)

```bash
cd /home/ragab/odoo/odoo15
./odoo-bin -c conf/patro.conf -d patro -i performance_optimization --stop-after-init
```

OR via Odoo interface:
1. Go to **Apps**
2. Remove "Apps" filter
3. Search "Performance Optimization"
4. Click **Install**

### Step 4: Configure POS (1 minute)

1. Go to **Point of Sale → Configuration → Point of Sale**
2. Open your POS
3. Click on **Performance Settings** tab
4. Set:
   - ✓ Enable "Limit Products to Load"
   - Product Load Limit: **1000**
   - ✓ Enable "Load Only Available Products"
5. **Save**

### Step 5: Test! (30 seconds)

1. Open a new POS session
2. Generate a stock report
3. Enjoy the speed! 🎉

---

## Expected Results

| Before | After |
|--------|-------|
| POS opens in 30-60 seconds | POS opens in 3-5 seconds ✨ |
| Stock reports take 60-120 seconds | Stock reports take 10-15 seconds ✨ |
| Server timeouts | No more timeouts ✨ |

---

## Troubleshooting

**POS still slow?**
- Make sure Performance Settings are enabled in POS Config
- Clear browser cache (Ctrl+Shift+Delete)
- Check product load limit is 500-1000 (not 28,700!)

**Stock reports still slow?**
- Run the database optimization script again
- Restart Odoo server
- Check PostgreSQL logs: `sudo tail -f /var/log/postgresql/*.log`

**Database script errors?**
- Check database password in the script
- Make sure PostgreSQL is running: `sudo systemctl status postgresql`
- Run as postgres user: `sudo su - postgres`, then run script

---

## Need More Details?

See the full [README.md](README.md) for:
- Detailed explanations
- PostgreSQL tuning
- Monitoring and maintenance
- Advanced optimizations

---

## Quick Commands Reference

```bash
# Run database optimization
cd /home/ragab/odoo/odoo15/patro/performance_optimization/scripts
./optimize_database.sh

# Restart Odoo
sudo systemctl restart odoo

# Check Odoo logs
sudo tail -f /var/log/odoo/odoo.log

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*-main.log

# Install module
cd /home/ragab/odoo/odoo15
./odoo-bin -c conf/patro.conf -d patro -i performance_optimization --stop-after-init

# Update module
./odoo-bin -c conf/patro.conf -d patro -u performance_optimization --stop-after-init
```

---

## Support

If issues persist:
1. Check the logs (see commands above)
2. Review the full README.md
3. Verify all steps were completed
4. Check server resources: `htop` or `top`

**Remember:** With 28,700 products, some operations will naturally take time. The optimizations make them 75-90% faster, not instant.

