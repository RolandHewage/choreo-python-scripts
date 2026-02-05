#!/bin/bash

# --- CONFIGURATION ---
REGION="eu-west-2"
OUTPUT_FILE="secrets_full_audit.csv"
# ---------------------

# 1. Create Header
# We are combining Secret Metadata (Cols 1-4) with Version Metadata (Cols 5-7)
echo "SecretName,LastAccessedDate,LastChangedDate,Tags,VersionId,VersionStages,VersionCreatedDate" > "$OUTPUT_FILE"

echo "Starting full audit scan in $REGION..."
echo "This may take some time depending on the number of secrets..."

# 2. Get the full list of secrets (containing the metadata)
# We output raw JSON so we can iterate object-by-object safely
SECRETS_LIST_JSON=$(aws secretsmanager list-secrets --region "$REGION" --output json)

# 3. Loop through every secret object
# 'jq -c .SecretList[]' prints each secret as a single-line JSON string
echo "$SECRETS_LIST_JSON" | jq -c '.SecretList[]' | while read -r secret_record; do

    # --- Extract Secret-Level Metadata ---
    
    # 1. Name
    SECRET_NAME=$(echo "$secret_record" | jq -r '.Name')
    
    # 2. Last Accessed (Handle nulls)
    LAST_ACCESSED=$(echo "$secret_record" | jq -r '.LastAccessedDate // "Never"')
    
    # 3. Last Changed
    LAST_CHANGED=$(echo "$secret_record" | jq -r '.LastChangedDate // "N/A"')
    
    # 4. Tags (Convert Array to "Key=Value; Key2=Value2" string)
    # We use 'map' to format, 'join' to combine, and '// empty' if no tags exist
    TAGS_FORMATTED=$(echo "$secret_record" | jq -r '(.Tags // []) | map("\(.Key)=\(.Value)") | join("; ")')

    echo "Scanning: $SECRET_NAME"

    # --- Get Versions for this Secret ---
    
    # We pass the outer variables ($TAGS_FORMATTED, etc) into the inner jq command using --arg
    aws secretsmanager list-secret-version-ids \
        --secret-id "$SECRET_NAME" \
        --region "$REGION" \
        --output json | \
    jq -r \
        --arg name "$SECRET_NAME" \
        --arg access "$LAST_ACCESSED" \
        --arg changed "$LAST_CHANGED" \
        --arg tags "$TAGS_FORMATTED" \
        '.Versions[] | [$name, $access, $changed, $tags, .VersionId, (.VersionStages | join(";")), .CreatedDate] | @csv' >> "$OUTPUT_FILE"

done

echo "------------------------------------------------"
echo "Scan Complete. Results saved to $OUTPUT_FILE"
