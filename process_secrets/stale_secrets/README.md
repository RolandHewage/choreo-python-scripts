# Stale Secrets Detection

This directory contains scripts to detect and analyze stale secrets in AWS Key Vault that are not referenced in any Choreo database.

## Scripts

### 1. `detect_stale_secrets.py`
**Purpose**: Basic stale secret detection with summary statistics

**What it does**:
- Compares AWS Key Vault secrets against all DB folder secrets
- Identifies secrets present in AWS but not in any database
- Generates a simple list of stale secret UUIDs
- Provides active secret counts per database

**Output**: `stale_secrets.csv` - Simple list of stale secret UUIDs

**Usage**:
```bash
python3 detect_stale_secrets.py
```

### 2. `detect_stale_secrets_detailed.py`
**Purpose**: Detailed stale secret detection with full audit information

**What it does**:
- Uses `secrets_full_audit.csv` as the primary data source
- Identifies stale secrets with complete metadata
- Includes all versions of each secret (AWSCURRENT, AWSPREVIOUS)
- Provides comprehensive audit trail

**Output**: `stale_secrets_detailed.csv` with columns:
- SecretName (UUID)
- LastAccessedDate
- LastChangedDate
- Tags
- VersionId
- VersionStages
- VersionCreatedDate

**Usage**:
```bash
python3 detect_stale_secrets_detailed.py
```

### 3. `sort_stale_secrets.py`
**Purpose**: Sort stale secrets by different date criteria

**What it does**:
- Reads `stale_secrets_detailed.csv`
- Creates three sorted output files by different date fields
- Handles special cases like "Never" and "N/A"
- Sorts in descending order (most recent first)

**Outputs**:
- `stale_secrets_by_last_accessed.csv` - Sorted by LastAccessedDate
- `stale_secrets_by_last_changed.csv` - Sorted by LastChangedDate
- `stale_secrets_by_version_created.csv` - Sorted by VersionCreatedDate

**Usage**:
```bash
python3 sort_stale_secrets.py
```

## Workflow

1. **Run basic detection** (optional):
   ```bash
   python3 detect_stale_secrets.py
   ```

2. **Run detailed detection** (recommended):
   ```bash
   python3 detect_stale_secrets_detailed.py
   ```

3. **Sort results** by date criteria:
   ```bash
   python3 sort_stale_secrets.py
   ```

## Latest Execution Summary

Summary:
  AWS Key Vault secrets: 3720
  DB folder secrets: 22892
  Stale secrets: 354
  Active secrets: 3366

Active secrets by DB folder:
  choreo_app_db: 1219 active secrets
  choreo_cloud_manager_db: 0 active secrets
  choreo_configuration_service_db: 1491 active secrets
  choreo_rudder_db: 656 active secrets

Detailed Analysis:
  Total stale UUIDs: 354
  UUIDs with audit data: 354
  UUIDs without audit data: 0
  Total rows in output (including all versions): 368

## Key Insights

- **Multiple Versions**: Some secrets have multiple versions (AWSCURRENT + AWSPREVIOUS), resulting in more rows in detailed output than unique UUIDs
- **Zero Cloud Manager Matches**: No direct matches found in Cloud Manager DB, suggesting different secret naming or storage approach
- **High Active Rate**: 90.5% of AWS secrets are actively used across databases (3366 out of 3720)
- **Cleanup Candidates**: 354 stale secrets identified as potential deletion candidates

## Data Sources

- **AWS Key Vault**: `../aws_key_vault/secrets_full_audit.csv` and `key_vault_secrets.csv`
- **App DB**: `../choreo_app_db/key_vault_secrets.csv`
- **Cloud Manager DB**: `../choreo_cloud_manager_db/key_vault_secrets.csv`
- **Configuration Service DB**: `../choreo_configuration_service_db/key_vault_secrets.csv`
- **Rudder DB**: `../choreo_rudder_db/key_vault_secrets.csv`
