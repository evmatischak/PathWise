import json
import sys
from collections import Counter

def extract_ids(ontology):
    ids = []
    for category in ontology.get("categories", []):
        for term in category.get("terms", []):
            if "id" in term:
                ids.append(term["id"])
    return ids

def main(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        ontology = json.load(f)

    ids = extract_ids(ontology)
    id_counts = Counter(ids)
    duplicates = {id_: count for id_, count in id_counts.items() if count > 1}

    if duplicates:
        print("❌ Duplicate IDs found:")
        for dup_id, count in duplicates.items():
            print(f"  - {dup_id} (appears {count} times)")
        sys.exit(1)
    else:
        print("✅ All IDs are unique.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_unique_ids.py pathwise_ontology.json")
        sys.exit(2)
    main(sys.argv[1])
