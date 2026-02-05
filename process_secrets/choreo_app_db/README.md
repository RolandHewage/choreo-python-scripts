# Choreo App DB - Secret References Extraction

## Overview
Extracts key vault secret references from the Choreo App database by querying configuration values associated with components and organizations.

## Script
- `extract_app_db_secret_refs.py` - Extracts secret references from configuration_value table

## SQL Query

```sql
SELECT DISTINCT
    cd.organization_handle,
    cv.value_ref,
    PARSENAME(REPLACE(cv.value_ref, '/', '.'), 2) as secret_uuid,
    PARSENAME(REPLACE(cv.value_ref, '/', '.'), 3) as key_vault_name
FROM configuration_value cv
JOIN configuration_mount cm ON cv.config_mount_id = cm.id
JOIN component_data cd ON cm.component_data_uuid = cd.uuid
WHERE cd.organization_handle = 'universityofedinburgh'
  AND cv.value_ref IS NOT NULL
  AND cv.value_ref != ''
ORDER BY cd.organization_handle DESC;
```

## Output
- `key_vault_secrets.csv` - List of unique secret UUIDs extracted from the database

## Latest Execution History

**2026/02/02**
- No duplicate secret_uuids found
- Extracted **1,221 secrets** into key_vault_secrets.csv
- Active secrets: **1,219** (when compared with AWS Key Vault)

## Key Tables
- `configuration_value` - Stores configuration values with secret references
- `configuration_mount` - Links configurations to components
- `component_data` - Contains component and organization information
