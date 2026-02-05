### Extract key vault secret references from choreo_configuration_service_db

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

Execution History

2026/02/02
No duplicate value_ref entries found.
Extracted 1491 secrets into key_vault_secrets.csv
