import csv
import re
from pathlib import Path
from uuid import UUID

def is_type1_uuid(uuid_str):
    """
    Check if a UUID is type 1 (time-based UUID).
    Type 1 UUIDs have the version bits set to 0001 in the third group.
    The version is indicated by the first hexadecimal digit of the third group.
    """
    try:
        # Parse the UUID
        uuid_obj = UUID(uuid_str)
        
        # Check if it's a version 1 UUID
        # Version 1 UUIDs have version field = 1
        return uuid_obj.version == 1
    except (ValueError, AttributeError):
        # If parsing fails, use pattern matching as fallback
        # Type 1 UUIDs have '1' as the first character of the 3rd group
        pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-1[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(pattern, uuid_str.lower()))

def filter_type1_uuids():
    """
    Filter out type 1 UUIDs from stale secrets and generate final delete candidates list.
    """
    script_dir = Path(__file__).parent
    
    # Input file
    stale_secrets_csv = script_dir / 'stale_secrets.csv'
    
    # Output file
    delete_candidates_list_txt = script_dir / 'delete_candidates_list.txt'
    
    print("=" * 80)
    print("Filtering Type 1 UUIDs from Stale Secrets")
    print("=" * 80)
    print()
    
    # Read stale secrets (simple list)
    print(f"Reading stale secrets from: {stale_secrets_csv}")
    stale_uuids = []
    try:
        with open(stale_secrets_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                uuid = row.get('key_vault_secret_name', '').strip()
                if uuid:
                    stale_uuids.append(uuid)
        print(f"Loaded {len(stale_uuids)} stale UUIDs")
    except FileNotFoundError:
        print(f"Error: File not found - {stale_secrets_csv}")
        return
    
    # Classify UUIDs
    print()
    print("Classifying UUIDs by type...")
    type1_uuids = []
    non_type1_uuids = []
    
    for uuid in stale_uuids:
        if is_type1_uuid(uuid):
            type1_uuids.append(uuid)
        else:
            non_type1_uuids.append(uuid)
    
    print(f"  Type 1 UUIDs (time-based): {len(type1_uuids)}")
    print(f"  Non-Type 1 UUIDs: {len(non_type1_uuids)}")
    print()
    
    # Write delete candidates as plain text (one UUID per line, no comments)
    print(f"Writing delete candidates to: {delete_candidates_list_txt}")
    with open(delete_candidates_list_txt, 'w', encoding='utf-8') as file:
        for uuid in sorted(non_type1_uuids):
            file.write(f"{uuid}\n")
    print(f"  ✓ Saved {len(non_type1_uuids)} delete candidates (one UUID per line)")
    print()
    
    # Summary
    print("=" * 80)
    print("Filtering Complete!")
    print("=" * 80)
    print()
    print("Summary:")
    print(f"  Total stale secrets: {len(stale_uuids)}")
    print(f"  Type 1 UUIDs (excluded): {len(type1_uuids)}")
    print(f"  Final delete candidates: {len(non_type1_uuids)}")
    print(f"  Reduction: {len(type1_uuids)} secrets ({len(type1_uuids)/len(stale_uuids)*100:.1f}%)")
    print()
    
    # Show all Type 1 UUIDs
    if type1_uuids:
        print("=" * 80)
        print(f"Type 1 UUIDs Excluded ({len(type1_uuids)} total)")
        print("=" * 80)
        for i, uuid in enumerate(sorted(type1_uuids), 1):
            print(f"{i:3d}. {uuid}")
        print()
    
    print(f"Output File: {delete_candidates_list_txt.name}")
    print()
    
    return non_type1_uuids, type1_uuids

if __name__ == '__main__':
    delete_candidates, excluded = filter_type1_uuids()
