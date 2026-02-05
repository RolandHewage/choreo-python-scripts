import csv
from pathlib import Path
from datetime import datetime

def parse_date(date_str):
    """Parse date string and return datetime object for sorting. Handle 'Never' and 'N/A' cases."""
    if not date_str or date_str.strip().upper() in ['NEVER', 'N/A', '']:
        # Return a very old date for 'Never' or 'N/A' so they appear at the bottom when sorted descending
        return datetime(1900, 1, 1)
    
    try:
        # Parse ISO format dates and remove timezone info for comparison
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        # Return naive datetime (without timezone) for consistent comparison
        return dt.replace(tzinfo=None)
    except Exception:
        # If parsing fails, return old date
        return datetime(1900, 1, 1)

def sort_stale_secrets():
    """
    Sort stale_secrets_detailed.csv by different date fields and create separate output files.
    """
    script_dir = Path(__file__).parent
    input_file = script_dir / 'stale_secrets_detailed.csv'
    
    print("=" * 80)
    print("Sorting Stale Secrets by Date Fields")
    print("=" * 80)
    print()
    
    # Read the input CSV
    print(f"Reading from: {input_file}")
    secrets = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                secrets.append(row)
        
        print(f"Loaded {len(secrets)} secret records")
        print()
    except FileNotFoundError:
        print(f"Error: File not found - {input_file}")
        print("Please run detect_stale_secrets_detailed.py first to generate the input file.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    if not secrets:
        print("No secrets found in the input file.")
        return
    
    # Define the sort configurations
    sort_configs = [
        {
            'field': 'LastAccessedDate',
            'output_file': 'stale_secrets_by_last_accessed.csv',
            'description': 'Last Accessed Date'
        },
        {
            'field': 'LastChangedDate',
            'output_file': 'stale_secrets_by_last_changed.csv',
            'description': 'Last Changed Date'
        },
        {
            'field': 'VersionCreatedDate',
            'output_file': 'stale_secrets_by_version_created.csv',
            'description': 'Version Created Date'
        }
    ]
    
    # Sort and save for each configuration
    for config in sort_configs:
        field = config['field']
        output_file = script_dir / config['output_file']
        description = config['description']
        
        print(f"Sorting by {description} (descending)...")
        
        # Sort by the date field in descending order (most recent first)
        sorted_secrets = sorted(
            secrets,
            key=lambda x: parse_date(x.get(field, '')),
            reverse=True
        )
        
        # Write to output file
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['SecretName', 'LastAccessedDate', 'LastChangedDate', 
                         'Tags', 'VersionId', 'VersionStages', 'VersionCreatedDate']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sorted_secrets)
        
        print(f"  ✓ Saved to: {output_file}")
        
        # Show top 3 entries
        print(f"  Top 3 entries by {description}:")
        for i, secret in enumerate(sorted_secrets[:3], 1):
            date_value = secret.get(field, 'N/A')
            secret_name = secret.get('SecretName', 'N/A')
            print(f"    {i}. {secret_name[:40]}... - {date_value}")
        print()
    
    print("=" * 80)
    print("Sorting Complete!")
    print("=" * 80)
    print()
    print("Output files created:")
    for config in sort_configs:
        print(f"  - {config['output_file']} (sorted by {config['description']})")

if __name__ == '__main__':
    sort_stale_secrets()
