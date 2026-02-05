import csv
from collections import Counter
import re

input_file = "38516-8.log"
output_file = "key_vault_secrets.csv"

# UUID regex (strict)
UUID_REGEX = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)

secrets = []
skipped_empty_vault_ids = 0

with open(input_file, "r") as f:
    for line in f:
        raw_line = line.rstrip()

        # Skip headers, separators, footers
        if (
            not raw_line.strip()
            or raw_line.startswith("vault_id")
            or raw_line.startswith("-")
            or raw_line.startswith("(")
        ):
            continue

        parts = raw_line.split()

        # If vault_id column is empty, the first token won't be a UUID
        candidate = parts[0]

        if UUID_REGEX.match(candidate):
            secrets.append(candidate)
        else:
            skipped_empty_vault_ids += 1

# Write CSV
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["key_vault_secret_name"])
    for s in secrets:
        writer.writerow([s])

# Duplicate detection
counter = Counter(secrets)
duplicates = {k: v for k, v in counter.items() if v > 1}

# Reporting
print("Vault ID extraction summary")
print("----------------------------")
print(f"Valid vault_ids extracted : {len(secrets)}")
print(f"Rows skipped (empty vault_id): {skipped_empty_vault_ids}")

if duplicates:
    print("\nDuplicate vault_id values found:")
    for vault_id, count in duplicates.items():
        print(f"{vault_id} -> {count} times")
else:
    print("\nNo duplicate vault_id values found.")

print(f"\nCSV written to: {output_file}")
