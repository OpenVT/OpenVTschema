import json
import os
import jsonschema
from jsonschema import validate


def load_schema(schema_file):
    with open(schema_file, 'r') as file:
        return json.load(file)


def validate_instance(instance_file, schema):
    with open(instance_file, 'r') as file:
        instance = json.load(file)
        validate(instance=instance, schema=schema)


def load_simulator_schemas(directory):
    schemas = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            # schema_name = filename.replace(".json", "")
            schema_file = os.path.join(directory, filename)
            simulator_schema = load_schema(schema_file)
            simulator_name = simulator_schema['name']
            schemas[simulator_name] = simulator_schema
    return schemas


def main():
    global_schema = load_schema('global_schema.json')
    simulator_instance_directory = 'simulator_schemas'
    simulator_schemas = load_simulator_schemas(f'{simulator_instance_directory}/')

    for filename in os.listdir(simulator_instance_directory):
        if filename.endswith(".json"):
            instance_file = os.path.join(simulator_instance_directory, filename)
            validate_instance(instance_file, global_schema)

    model_instance_directory = 'model_schemas'
    for filename in os.listdir(model_instance_directory):
        if filename.endswith(".json"):
            instance_file = os.path.join(model_instance_directory, filename)
            with open(instance_file, 'r') as file:
                instance = json.load(file)
                simulator = instance['properties']['simulator']
                if simulator and simulator in simulator_schemas:
                    validate_instance(instance_file, simulator_schemas[simulator])


if __name__ == "__main__":
    main()
