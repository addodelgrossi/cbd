# Issue #2: Memory Error - Wrong Repository

## Summary

Issue #2 "Ao executar na mina maquina tenho erro de memory" was filed in this repository (`cbd` - Charlie Brown Decoder), but it describes a problem with a different project.

## The Issue

The issue describes:
- SQLite database operations with Brazilian company data (CNPJ)
- Tables: `estabelecimentos`, `socios`
- Memory error during VACUUM operation: `Error: out of memory (7)`

## The Problem

This repository (`addodelgrossi/cbd`) is a **Python CAPTCHA decoder** for image processing. It contains no database code or CNPJ-related functionality.

## Correct Repository

The issue should be filed in: **[addodelgrossi/bcd](https://github.com/addodelgrossi/bcd)** (Brazil Companies Database)

This is a Go application that manages Brazilian company data in SQLite.

## Solution for the Memory Error

If you're experiencing this error in the `bcd` repository, here are solutions to fix the SQLite `out of memory (7)` error:

### Option 1: Configure SQLite Memory Limits (Recommended)

Add these PRAGMA statements before running VACUUM:

```go
// Increase memory limits
db.Exec("PRAGMA cache_size = -2000000") // 2GB cache (negative = KB)
db.Exec("PRAGMA temp_store = MEMORY")
db.Exec("PRAGMA mmap_size = 2147483648") // 2GB mmap

// Alternative: Use incremental vacuum instead of full VACUUM
db.Exec("PRAGMA auto_vacuum = INCREMENTAL")
```

### Option 2: Disable VACUUM or Make it Optional

```go
// Make VACUUM optional with a flag
if !skipVacuum {
    log.Info("vacuuming database - this may take a while...")
    if err := db.Exec("VACUUM"); err != nil {
        log.Warn("VACUUM failed, continuing anyway: %v", err)
        // Don't fail the entire operation
    }
}
```

### Option 3: Use Alternative Cleanup Methods

Instead of full VACUUM, use:

```go
// Analyze tables without vacuum
db.Exec("ANALYZE")

// Or use incremental vacuum
db.Exec("PRAGMA incremental_vacuum")
```

### Option 4: System-Level Solutions

- Increase available RAM
- Add swap space
- Close other applications
- Set `ulimit -v unlimited` (Linux)

## Recommendation

Please close this issue and reopen it in the correct repository: https://github.com/addodelgrossi/bcd/issues
