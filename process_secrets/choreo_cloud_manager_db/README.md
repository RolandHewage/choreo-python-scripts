# Choreo Cloud Manager DB - Secret References Extraction

## Overview
Extracts key vault secret references from the Choreo Cloud Manager database by aggregating reference tokens from multiple credential tables.

## Script
- `extract_cloud_manager_db_secret_refs.py` - Extracts secret references from credential tables

## SQL Query

```sql
SELECT 
    'common_credentials' as source_table,
    reference_token as secret_name,
    organization_id,
    name as credential_name,
    type,
    createdAt as created_at
FROM common_credentials
WHERE reference_token IS NOT NULL AND organization_id = '11307'
UNION ALL
SELECT 
    'git_credentials' as source_table,
    reference_token as secret_name,
    organization_id,
    name as credential_name,
    type,
    createdAt as created_at
FROM git_credentials
WHERE reference_token IS NOT NULL AND organization_id = '11307'
UNION ALL
SELECT 
    'docker_credentials' as source_table,
    reference_token as secret_name,
    organization_id,
    name as credential_name,
    type,
    createdAt as created_at
FROM docker_credentials
WHERE reference_token IS NOT NULL AND organization_id = '11307'
UNION ALL
SELECT 
    'user_apps_credentials' as source_table,
    reference_token as secret_name,
    NULL as organization_id,
    name as credential_name,
    type,
    createdAt as created_at
FROM user_apps_credentials
WHERE reference_token IS NOT NULL
UNION ALL
SELECT 
    'third_party_registry_credentials' as source_table,
    reference_token as secret_name,
    organization_id,
    name as credential_name,
    type,
    createdAt as created_at
FROM third_party_registry_credentials
WHERE reference_token IS NOT NULL AND organization_id = '11307'
ORDER BY source_table, created_at DESC;
```

## Output
- `key_vault_secrets.csv` - List of unique reference tokens extracted from the database

## Latest Execution History

**2026/02/02**
- No duplicate secret_name values found
- Extracted **19,488 secrets** into key_vault_secrets.csv
- Active secrets: **0** (when compared with AWS Key Vault - no UUID format matches)

## Key Tables
- `common_credentials` - General credentials storage
- `git_credentials` - Git repository credentials
- `docker_credentials` - Docker registry credentials
- `user_apps_credentials` - User application credentials
- `third_party_registry_credentials` - Third-party registry credentials

## Notes
- Reference tokens in this DB use a different naming format than AWS Key Vault UUIDs
- Zero matches suggest different secret management approach or naming convention
