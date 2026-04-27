import csv
from collections import Counter

input_file = "config_service_secrets.csv"
output_file = "key_vault_secrets.csv"

secrets = []

with open(input_file, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        secret = (row.get("value_ref") or "").strip()
        if secret:
            secrets.append(secret)

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
