import csv
import os
from pathlib import Path

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

def detect_stale_secrets():
    """
    Detect stale secrets that exist in AWS Key Vault but not in any DB folders.
    """
    # Get the base directory (process_secrets folder)
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    
    # Path to AWS Key Vault secrets
    aws_csv_path = base_dir / 'aws_key_vault' / 'key_vault_secrets.csv'
    
    # Paths to DB folder secrets
    db_folders = [
        'choreo_app_db',
        'choreo_cloud_manager_db',
        'choreo_configuration_service_db',
        'choreo_rudder_db'
    ]
    
    print("=" * 80)
    print("Starting Stale Secrets Detection")
    print("=" * 80)
    print()
    
    # Read AWS Key Vault secrets
    print(f"Reading AWS Key Vault secrets from: {aws_csv_path}")
    aws_secrets = read_secrets_from_csv(aws_csv_path)
    print(f"Total AWS Key Vault secrets: {len(aws_secrets)}")
    print()
    
    # Read all DB folder secrets and combine them
    all_db_secrets = set()
    db_secrets_by_folder = {}
    print("Reading secrets from DB folders:")
    for folder in db_folders:
        db_csv_path = base_dir / folder / 'key_vault_secrets.csv'
        print(f"  - {folder}")
        db_secrets = read_secrets_from_csv(db_csv_path)
        db_secrets_by_folder[folder] = db_secrets
        all_db_secrets.update(db_secrets)
    
    print()
    print(f"Total unique secrets across all DB folders: {len(all_db_secrets)}")
    print()
    
    # Find stale secrets (in AWS but not in any DB)
    stale_secrets = aws_secrets - all_db_secrets
    
    print("=" * 80)
    print(f"Detection Complete: Found {len(stale_secrets)} stale secrets")
    print("=" * 80)
    print()
    
    # Write stale secrets to CSV
    output_path = script_dir / 'stale_secrets.csv'
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['key_vault_secret_name'])
        for secret in sorted(stale_secrets):
            writer.writerow([secret])
    
    print(f"Stale secrets saved to: {output_path}")
    print()
    
    # Print summary statistics
    print("Summary:")
    print(f"  AWS Key Vault secrets: {len(aws_secrets)}")
    print(f"  DB folder secrets: {len(all_db_secrets)}")
    print(f"  Stale secrets: {len(stale_secrets)}")
    print(f"  Active secrets: {len(aws_secrets & all_db_secrets)}")
    print()
    
    # Print active secret count for each DB folder
    print("Active secrets by DB folder:")
    for folder in db_folders:
        db_secrets = db_secrets_by_folder[folder]
        active_count = len(aws_secrets & db_secrets)
        print(f"  {folder}: {active_count} active secrets")
    print()
    
    # Print first 10 stale secrets as examples
    if stale_secrets:
        print("Sample stale secrets (first 10):")
        for i, secret in enumerate(sorted(stale_secrets)[:10], 1):
            print(f"  {i}. {secret}")
        if len(stale_secrets) > 10:
            print(f"  ... and {len(stale_secrets) - 10} more")
    
    return stale_secrets

if __name__ == '__main__':
    stale_secrets = detect_stale_secrets()
