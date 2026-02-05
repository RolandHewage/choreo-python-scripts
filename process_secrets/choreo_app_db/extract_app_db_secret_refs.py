import csv
from collections import Counter

input_file = "38516-3.log"
output_file = "key_vault_secrets.csv"

secrets = []

with open(input_file, "r") as f:
    for line in f:
        line = line.strip()

        # Skip headers, separators, and empty lines
        if (
            not line
            or line.startswith("organization_handle")
            or line.startswith("-")
            or line.startswith("(")
        ):
            continue

        # Split by whitespace (fixed-width table)
        parts = line.split()

        # secret_uuid is the 3rd column
        if len(parts) >= 3:
            secrets.append(parts[2])

# Write CSV
with open(output_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["key_vault_secret_name"])
    for s in secrets:
        writer.writerow([s])

# Detect duplicates
counter = Counter(secrets)
duplicates = {k: v for k, v in counter.items() if v > 1}

# Print duplicates
if duplicates:
    print("Duplicate secret_uuids found:")
    for secret, count in duplicates.items():
        print(f"{secret} -> {count} times")
else:
    print("No duplicate secret_uuids found.")

print(f"\nExtracted {len(secrets)} secrets into {output_file}")
