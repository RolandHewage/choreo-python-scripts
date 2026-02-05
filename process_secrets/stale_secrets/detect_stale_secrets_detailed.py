import csv
import os
from pathlib import Path
from collections import defaultdict

def read_secrets_from_csv(csv_path):
    """Read secret names from a CSV file and return as a set."""
    secrets = set()
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                secret_name = row.get('key_vault_secret_name', '').strip()
                if secret_name:
                    secrets.add(secret_name)
        print(f"Loaded {len(secrets)} secrets from {csv_path}")
    except FileNotFoundError:
        print(f"Warning: File not found - {csv_path}")
    except Exception as e:
        print(f"Error reading {csv_path}: {e}")
    return secrets

def read_full_audit_csv(csv_path):
    """Read the full audit CSV and organize by UUID (SecretName is the UUID)."""
    secrets_by_uuid = defaultdict(list)
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                uuid = row.get('SecretName', '').strip()
                if uuid:
                    # Store the full row data
                    secrets_by_uuid[uuid].append({
                        'SecretName': uuid,
                        'LastAccessedDate': row.get('LastAccessedDate', ''),
                        'LastChangedDate': row.get('LastChangedDate', ''),
                        'Tags': row.get('Tags', ''),
                        'VersionId': row.get('VersionId', ''),
                        'VersionStages': row.get('VersionStages', ''),
                        'VersionCreatedDate': row.get('VersionCreatedDate', '')
                    })
        
        print(f"Loaded {len(secrets_by_uuid)} unique UUIDs from full audit CSV")
    except FileNotFoundError:
        print(f"Error: File not found - {csv_path}")
    except Exception as e:
        print(f"Error reading full audit CSV: {e}")
    
    return secrets_by_uuid

def detect_stale_secrets_detailed():
    """
    Detect stale secrets with detailed information from secrets_full_audit.csv.
    """
    # Get the base directory (process_secrets folder)
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    
    # Path to full audit CSV
    full_audit_csv_path = base_dir / 'aws_key_vault' / 'secrets_full_audit.csv'
    
    # Path to AWS Key Vault secrets (UUIDs)
    aws_csv_path = base_dir / 'aws_key_vault' / 'key_vault_secrets.csv'
    
    # Paths to DB folder secrets
    db_folders = [
        'choreo_app_db',
        'choreo_cloud_manager_db',
        'choreo_configuration_service_db',
        'choreo_rudder_db'
    ]
    
    print("=" * 80)
    print("Starting Detailed Stale Secrets Detection")
    print("=" * 80)
    print()
    
    # Read full audit data
    print(f"Reading full audit data from: {full_audit_csv_path}")
    secrets_by_uuid = read_full_audit_csv(full_audit_csv_path)
    print()
    
    # Read AWS Key Vault secrets (UUIDs)
    print(f"Reading AWS Key Vault UUIDs from: {aws_csv_path}")
    aws_secrets = read_secrets_from_csv(aws_csv_path)
    print(f"Total AWS Key Vault UUIDs: {len(aws_secrets)}")
    print()
    
    # Read all DB folder secrets and combine them
    all_db_secrets = set()
    print("Reading secrets from DB folders:")
    for folder in db_folders:
        db_csv_path = base_dir / folder / 'key_vault_secrets.csv'
        print(f"  - {folder}")
        db_secrets = read_secrets_from_csv(db_csv_path)
        all_db_secrets.update(db_secrets)
    
    print()
    print(f"Total unique secrets across all DB folders: {len(all_db_secrets)}")
    print()
    
    # Find stale UUIDs (in AWS but not in any DB)
    stale_uuids = aws_secrets - all_db_secrets
    
    print("=" * 80)
    print(f"Detection Complete: Found {len(stale_uuids)} stale secrets")
    print("=" * 80)
    print()
    
    # Prepare detailed stale secrets data
    detailed_stale_secrets = []
    uuids_with_audit_data = 0
    uuids_without_audit_data = 0
    
    for uuid in stale_uuids:
        if uuid in secrets_by_uuid:
            uuids_with_audit_data += 1
            # Get all versions for this UUID
            versions = secrets_by_uuid[uuid]
            # Add each version as a separate row
            for version in versions:
                detailed_stale_secrets.append({
                    'SecretName': version['SecretName'],
                    'LastAccessedDate': version['LastAccessedDate'],
                    'LastChangedDate': version['LastChangedDate'],
                    'Tags': version['Tags'],
                    'VersionId': version['VersionId'],
                    'VersionStages': version['VersionStages'],
                    'VersionCreatedDate': version['VersionCreatedDate']
                })
        else:
            uuids_without_audit_data += 1
            # UUID not found in audit data - add with minimal info
            detailed_stale_secrets.append({
                'SecretName': uuid,
                'LastAccessedDate': 'N/A',
                'LastChangedDate': 'N/A',
                'Tags': 'N/A',
                'VersionId': 'N/A',
                'VersionStages': 'N/A',
                'VersionCreatedDate': 'N/A'
            })
    
    # Write detailed stale secrets to CSV
    output_path = script_dir / 'stale_secrets_detailed.csv'
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['SecretName', 'LastAccessedDate', 'LastChangedDate', 
                     'Tags', 'VersionId', 'VersionStages', 'VersionCreatedDate']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        # Sort by SecretName for consistency
        detailed_stale_secrets.sort(key=lambda x: x['SecretName'])
        writer.writerows(detailed_stale_secrets)
    
    print(f"Detailed stale secrets saved to: {output_path}")
    print()
    
    # Print summary statistics
    print("Summary:")
    print(f"  Total stale UUIDs: {len(stale_uuids)}")
    print(f"  UUIDs with audit data: {uuids_with_audit_data}")
    print(f"  UUIDs without audit data: {uuids_without_audit_data}")
    print(f"  Total rows in output (including all versions): {len(detailed_stale_secrets)}")
    print()
    
    # Print first 5 stale secrets as examples with details
    if detailed_stale_secrets:
        print("Sample stale secrets (first 5):")
        for i, secret in enumerate(detailed_stale_secrets[:5], 1):
            print(f"\n  {i}. Secret Name (UUID): {secret['SecretName']}")
            print(f"     Last Accessed: {secret['LastAccessedDate']}")
            print(f"     Last Changed: {secret['LastChangedDate']}")
            print(f"     Version Stage: {secret['VersionStages']}")
        
        if len(detailed_stale_secrets) > 5:
            print(f"\n  ... and {len(detailed_stale_secrets) - 5} more rows")

if __name__ == '__main__':
    detailed_stale_secrets = detect_stale_secrets_detailed()
