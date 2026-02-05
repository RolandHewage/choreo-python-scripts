### Extract key vault secret references from choreo_app_db

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

Execution History

2026/02/02
No duplicate secret_uuids found.
Extracted 1221 secrets into key_vault_secrets.csv
