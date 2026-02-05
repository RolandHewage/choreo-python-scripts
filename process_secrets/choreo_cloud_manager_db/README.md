### Extract key vault secret references from choreo_cloud_manager_db

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

Execution History

2026/02/02
No duplicate secret_name values found.
Extracted 19488 secrets into key_vault_secrets.csv
