# Choreo Configuration Service DB - Secret References Extraction

## Overview
Extracts key vault secret references from the Choreo Configuration Service database by querying configuration values scoped to specific organizations.

## Script
- `extract_config_svc_db_secret_refs.py` - Extracts secret references from configuration_values table

## SQL Query

```sql
SELECT DISTINCT cv.value_ref 
FROM configuration_values cv
INNER JOIN configuration_keys ck ON cv.key_id = ck.id
INNER JOIN configuration_groups cg ON ck.group_id = cg.id
INNER JOIN configuration_scopes cs ON cg.id = cs.group_id
WHERE cs.organization_uuid = 'f5aad5f4-4cac-40df-b0ed-e0c3ca8ae985'
  AND cv.value_ref != '' 
  AND cv.value_ref IS NOT NULL;
```

## Output
- `key_vault_secrets.csv` - List of unique secret UUIDs extracted from the database

## Latest Execution History

**2026/02/02**
- No duplicate value_ref entries found
- Extracted **1,491 secrets** into key_vault_secrets.csv
- Active secrets: **1,491** (when compared with AWS Key Vault - 100% match rate)

## Key Tables
- `configuration_values` - Stores configuration values with secret references
- `configuration_keys` - Configuration key definitions
- `configuration_groups` - Groups of related configurations
- `configuration_scopes` - Organization-level scoping of configurations

## Notes
- Perfect match rate indicates this DB is a primary source for active secrets
- All secrets extracted from this DB are actively used in AWS Key Vault
