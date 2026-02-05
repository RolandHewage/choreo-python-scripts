import csv
from collections import Counter

input_file = "38516-6.log"
output_file = "key_vault_secrets.csv"

secrets = []

with open(input_file, "r") as f:
    for line in f:
        line = line.strip()

        # Skip headers, separators, footers, empty lines
        if (
            not line
            or line.startswith("value_ref")
            or line.startswith("-")
            or line.startswith("(")
        ):
            continue

        secrets.append(line)

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
    print("Duplicate value_ref entries found:")
    for secret, count in duplicates.items():
        print(f"{secret} -> {count} times")
else:
    print("No duplicate value_ref entries found.")

print(f"\nExtracted {len(secrets)} secrets into {output_file}")
