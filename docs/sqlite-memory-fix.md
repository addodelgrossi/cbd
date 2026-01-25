# SQLite Memory Error Fix Guide

## Error Description

```
Error: out of memory (7)
```

This error occurs during SQLite VACUUM operations on large databases, particularly when working with Brazilian company data (CNPJ database).

## Root Cause

The VACUUM operation in SQLite requires approximately 2x the database size in free memory and disk space. For large datasets (millions of records), this can exceed system memory limits.

## Solutions

### Solution 1: Configure SQLite PRAGMA Settings (Recommended)

Before running VACUUM, configure these SQLite settings:

```sql
-- Increase cache size (negative value = kilobytes)
-- This example sets 2GB cache
PRAGMA cache_size = -2000000;

-- Store temporary tables in memory instead of disk
PRAGMA temp_store = MEMORY;

-- Enable memory-mapped I/O (2GB in this example)
PRAGMA mmap_size = 2147483648;

-- Optionally, set page size (must be done before data is loaded)
PRAGMA page_size = 4096;
```

### Solution 2: Use Incremental VACUUM

Instead of a full VACUUM, use incremental vacuuming:

```sql
-- Set auto vacuum mode (do this BEFORE loading data)
PRAGMA auto_vacuum = INCREMENTAL;

-- After data is loaded, perform incremental vacuum
PRAGMA incremental_vacuum(1000); -- Free 1000 pages at a time
```

### Solution 3: Make VACUUM Optional

Add a command-line flag to skip VACUUM when memory is limited:

```bash
# Example command with --skip-vacuum flag
./your-program --skip-vacuum
```

### Solution 4: Optimize VACUUM Timing

```sql
-- Only vacuum when fragmentation is significant
SELECT 
    (page_count - freelist_count) as used_pages,
    freelist_count as free_pages,
    (freelist_count * 100.0 / page_count) as fragmentation_pct
FROM pragma_page_count(), pragma_freelist_count();

-- Only vacuum if fragmentation > 20%
```

### Solution 5: System-Level Configuration

**Increase swap space (Linux):**
```bash
# Create 4GB swap file
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

**Increase memory limits:**
```bash
# Remove virtual memory limit
ulimit -v unlimited

# Check current limits
ulimit -a
```

### Solution 6: VACUUM in Parts (Advanced)

For very large databases, split the vacuum operation:

```sql
-- Vacuum individual tables instead of entire database
VACUUM estabelecimentos;
VACUUM socios;
-- etc.
```

Note: Table-level VACUUM is not directly supported in SQLite, but you can:
1. Create a new database
2. Copy tables one at a time using INSERT INTO ... SELECT
3. Replace the old database

## Implementation Example (Go)

```go
package main

import (
    "database/sql"
    "flag"
    "log"
    _ "github.com/mattn/go-sqlite3"
)

func main() {
    skipVacuum := flag.Bool("skip-vacuum", false, "Skip VACUUM operation")
    flag.Parse()

    db, err := sql.Open("sqlite3", "database.db")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Configure SQLite for better memory handling
    configureSQLite(db)

    // ... load data, create indexes ...

    // Analyze tables
    log.Println("Analyzing tables for query optimization...")
    if _, err := db.Exec("ANALYZE"); err != nil {
        log.Printf("Warning: ANALYZE failed: %v", err)
    }

    // Optional vacuum
    if !*skipVacuum {
        log.Println("Vacuuming database - this may take a while...")
        if err := vacuumWithRetry(db); err != nil {
            log.Printf("Warning: VACUUM failed: %v (continuing anyway)", err)
            // Don't fail the entire operation
        }
    } else {
        log.Println("Skipping VACUUM (--skip-vacuum flag set)")
    }
}

func configureSQLite(db *sql.DB) {
    pragmas := []string{
        "PRAGMA journal_mode = WAL",
        "PRAGMA synchronous = NORMAL",
        "PRAGMA cache_size = -2000000",  // 2GB cache
        "PRAGMA temp_store = MEMORY",
        "PRAGMA mmap_size = 2147483648",  // 2GB mmap
    }

    for _, pragma := range pragmas {
        if _, err := db.Exec(pragma); err != nil {
            log.Printf("Warning: %s failed: %v", pragma, err)
        }
    }
}

func vacuumWithRetry(db *sql.DB) error {
    // Try full VACUUM first
    if _, err := db.Exec("VACUUM"); err != nil {
        log.Printf("Full VACUUM failed: %v, trying incremental...", err)
        
        // Try incremental vacuum as fallback
        if _, err := db.Exec("PRAGMA incremental_vacuum"); err != nil {
            return err
        }
    }
    return nil
}
```

## Prevention

To avoid this issue in the future:

1. **Set auto_vacuum mode** before loading data:
   ```sql
   PRAGMA auto_vacuum = INCREMENTAL;
   ```

2. **Monitor database size** and available memory

3. **Use WAL mode** for better concurrency:
   ```sql
   PRAGMA journal_mode = WAL;
   ```

4. **Regular maintenance** with incremental vacuum instead of full VACUUM

## Testing

Before running on production data:

```bash
# Check database size
ls -lh database.db

# Ensure 2x database size is available in RAM + swap
free -h

# Test with smaller dataset first
```

## References

- [SQLite PRAGMA Statements](https://www.sqlite.org/pragma.html)
- [SQLite VACUUM Documentation](https://www.sqlite.org/lang_vacuum.html)
- [SQLite Memory Management](https://www.sqlite.org/malloc.html)
