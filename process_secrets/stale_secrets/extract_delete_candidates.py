import csv

input_file = "stale_secrets_detailed.csv"
output_file = "delete_candidates.txt"

secret_names = []
seen = set()

with open(input_file, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = (row.get("SecretName") or "").strip()
        if name and name not in seen:
            secret_names.append(name)
            seen.add(name)

with open(output_file, "w") as f:
    for name in secret_names:
        f.write(name + "\n")

print(f"Extracted {len(secret_names)} unique secret names into {output_file}")
