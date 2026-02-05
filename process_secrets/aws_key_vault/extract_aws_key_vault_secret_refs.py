import csv
import re
from collections import Counter

input_file = "secrets_full_audit.csv"
valid_output_file = "key_vault_secrets.csv"
invalid_output_file = "non_uuid_secret_names.csv"

# Strict UUID regex
UUID_REGEX = re.compile(
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}$"
)

valid_secrets = []
invalid_secrets = []

total_rows = 0
skipped_non_current = 0

with open(input_file, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        total_rows += 1

        # Only AWSCURRENT versions
        if row["VersionStages"] != "AWSCURRENT":
            skipped_non_current += 1
            continue

        secret_name = row["SecretName"]

        if UUID_REGEX.match(secret_name):
            valid_secrets.append(secret_name)
        else:
            invalid_secrets.append({
                "SecretName": secret_name,
                "VersionId": row["VersionId"],
                "VersionStages": row["VersionStages"]
            })

# Write valid UUID SecretNames
with open(valid_output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["key_vault_secret_name"])
    for s in valid_secrets:
        writer.writerow([s])

# Write non-UUID SecretNames
with open(invalid_output_file, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["SecretName", "VersionId", "VersionStages"]
    )
    writer.writeheader()
    for row in invalid_secrets:
        writer.writerow(row)

# Duplicate detection (UUID SecretNames only)
counter = Counter(valid_secrets)
duplicates = {k: v for k, v in counter.items() if v > 1}

# Reporting
print("AWS Secrets (AWSCURRENT) – SecretName UUID Validation")
print("----------------------------------------------------")
print(f"Total rows processed          : {total_rows}")
print(f"Skipped non-AWSCURRENT rows   : {skipped_non_current}")
print(f"Valid UUID SecretNames        : {len(valid_secrets)}")
print(f"Non-UUID SecretNames detected : {len(invalid_secrets)}")

if duplicates:
    print("\nDuplicate UUID SecretNames found:")
    for secret, count in duplicates.items():
        print(f"{secret} -> {count} times")
else:
    print("\nNo duplicate UUID SecretNames found.")

print(f"\nValid UUID CSV   : {valid_output_file}")
print(f"Non-UUID CSV     : {invalid_output_file}")
