import json
import jsonschema
from jsonschema import validate
import sys

def load_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

def main():
    try:
        ontology_path = "pathwise_ontology.json"
        schema_path = "schema.json"

        # Load files
        data = load_json(ontology_path)
        schema = load_json(schema_path)

        # Validate
        validate(instance=data, schema=schema)
        print("✅ JSON is valid and conforms to the schema.")

    except jsonschema.exceptions.ValidationError as err:
        print("❌ Validation error:")
        print(err.message)
        sys.exit(1)
    except Exception as e:
        print("❌ Unexpected error:")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
