# Choreo Rudder DB - Secret References Extraction

## Overview
Extracts key vault secret references from the Choreo Rudder database by querying both secrets and config_maps tables for vault IDs.

## Scripts
- `extract_rudder_db_secret_refs.py` - Primary extraction script
- `extract_rudder_db_secret_refs_backup.py` - Backup version

## SQL Query

```sql
SELECT 
    vault_id,
    name,
    'secrets' as source_table,
    created_at
FROM secrets
WHERE vault_id IS NOT NULL AND organization_id = 'f5aad5f4-4cac-40df-b0ed-e0c3ca8ae985'
UNION ALL
SELECT 
    vault_id,
    name,
    'config_maps' as source_table,
    created_at
FROM config_maps
WHERE vault_id IS NOT NULL AND organization_id = 'f5aad5f4-4cac-40df-b0ed-e0c3ca8ae985'
ORDER BY created_at DESC;
```

## Output
- `key_vault_secrets.csv` - List of unique vault IDs extracted from the database
- `key_vault_secrets_with_names.csv` - Extended version including secret names

## Latest Execution History

**2026/02/02**
- Extracted **692 unique vault IDs** into key_vault_secrets.csv
- Active secrets: **656** (when compared with AWS Key Vault)
- **Note**: Duplicate vault_id values found across secrets and config_maps tables

### Duplicate vault_id Values Found:
pure-visitor-integration-377426398 -> 3 times
opas-g2-scheduled-task-3865857953 -> 3 times
mediation-history-classics-and-514186435 -> 3 times
activemq-viewer-818706314 -> 3 times
mediation-pure-id-resolver-945581776 -> 3 times
mediation-sits-integration-api-1455967074 -> 3 times
scpreport-2351674411 -> 3 times
mediation-social-political-sci-1898524381 -> 3 times
mediation-estates-api-proxy-2052929379 -> 3 times
idm-integration-scheduler-4077181971 -> 3 times
wtribe-scheduled-task-3722025393 -> 3 times
pure-finance-projects-sch-3848849260 -> 3 times
pure-finance-awards-sched-2494837849 -> 3 times
mediation-physics-and-astronom-1229417050 -> 3 times
mediation-informatics-api-pr-a-732704381 -> 3 times
mediation-geo-sciences-api-pr--854153573 -> 3 times
eopasscheduledtask-3752852819 -> 3 times
careerhub-task-scheduler-95265999 -> 3 times
careerhubintegration-4149937593 -> 3 times
mediation-stutalkincomingapipr-3459593691 -> 3 times
atom-feed-scheduled-tasks-835723694 -> 3 times
archibus-work-requests-sc-1983915944 -> 3 times
mediation-card-microservice-ap-409343302 -> 3 times
payroll-codes-cheduled-task-2480559677 -> 2 times
mediation-exam-timetabling-api-3551406136 -> 3 times
archibus-stock-inventory-afm-s-828182580 -> 2 times
archibus-stock-inventory-sched-2270187455 -> 2 times
mediation-course-timetabling-a-3332878243 -> 3 times
mediation-worktribe-api-proxy-4066319408 -> 3 times
saffron-task-scheduler-941617927 -> 3 times
mediation-saffron-ftp-proxy-ap-3132485838 -> 3 times
archibus-ar-lease-schedul-34327540 -> 3 times
pure-impacts-scheduled-ta-1982172989 -> 3 times
pure-impacts-delete-task-671972826 -> 3 times
mediation-accounts-payables-ap-2373615178 -> 3 times
mediation-alma-api-proxy-1606810509 -> 3 times
mediation-estates-api-proxy-3422759928 -> 3 times
alma-scheduled-task-3309089931 -> 3 times
kinetics-scheduled-task-1720258325 -> 3 times
mediation-idm-156759324 -> 3 times
mediation-room-display-api-530515123 -> 3 times
mediation-inohub-api-2899078118 -> 3 times
mediation-dvdtkx-1759884326 -> 2 times
mediation-zttsyh-410790265 -> 2 times
mediation-fmmqev-1225520545 -> 3 times
mediation-qwlvrx-2288625824 -> 3 times
mediation-myowlo-2481818128 -> 3 times
mediation-nnkbbq-1808521313 -> 3 times
mediation-xpneqw-1319095223 -> 2 times
mediation-nnkbbq-851980542 -> 3 times
Extracted 844 secrets into key_vault_secrets.csv

2026/02/02
Valid vault_ids extracted : 692
Rows skipped (empty vault_id): 152
No duplicate vault_id values found.

