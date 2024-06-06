import json
import jsonschema
import sys
import os

def validate_instance(instance_file, schema_file):
    with open(schema_file, 'r') as schema_f:
        schema = json.load(schema_f)

    with open(instance_file, 'r') as instance_f:
        instance = json.load(instance_f)

    try:
        jsonschema.validate(instance, schema)
        print(f"{instance_file} is valid.")
    except jsonschema.exceptions.ValidationError as e:
        print(f"{instance_file} is invalid: {e.message}")


def main():
    if len(sys.argv) != 3:
        print("Usage: validate-instance <instance_file> <schema_file>")
        sys.exit(1)

    instance_file = sys.argv[1]
    schema_file = sys.argv[2]

    validate_instance(instance_file, schema_file)


if __name__ == "__main__":
    main()
