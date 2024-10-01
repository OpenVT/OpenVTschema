"""
Script to validate object and process instances
"""

import json
import os
import jsonschema
from jsonschema import validate

# Load schemas from the 'schemas' directory
with open('schemas/object_schema.json', 'r') as obj_schema_file:
    object_schema = json.load(obj_schema_file)

with open('schemas/process_schema.json', 'r') as proc_schema_file:
    process_schema = json.load(proc_schema_file)

# Function to validate and save objects, with overwrite option
def validate_and_save_object(object_instance, object_dir='objects', overwrite=False):
    try:
        # Validate the object instance against the schema
        validate(instance=object_instance, schema=object_schema)
        print("Object is valid.")

        # Ensure the objects directory exists
        if not os.path.exists(object_dir):
            os.makedirs(object_dir)

        # Check if an object with the same ID already exists
        object_id = object_instance['id']
        filepath = os.path.join(object_dir, f"{object_id}.json")
        if os.path.exists(filepath) and not overwrite:
            print(f"Error: An object with ID '{object_id}' already exists. Use overwrite=True to replace it.")
            return

        # Save (or overwrite) the object instance as a JSON file
        with open(filepath, 'w') as f:
            json.dump(object_instance, f, indent=4)
        print(f"Object saved at: {filepath}")

    except jsonschema.exceptions.ValidationError as e:
        print(f"Object validation failed: {e}")

# Function to validate and save processes, with overwrite option
def validate_and_save_process(process_instance, process_dir='processes', overwrite=False):
    try:
        # Validate the process instance against the schema
        validate(instance=process_instance, schema=process_schema)
        print("Process is valid.")

        # Ensure the processes directory exists
        if not os.path.exists(process_dir):
            os.makedirs(process_dir)

        # Check if a process with the same ID already exists
        process_id = process_instance['id']
        filepath = os.path.join(process_dir, f"{process_id}.json")
        if os.path.exists(filepath) and not overwrite:
            print(f"Error: A process with ID '{process_id}' already exists. Use overwrite=True to replace it.")
            return

        # Save (or overwrite) the process instance as a JSON file
        with open(filepath, 'w') as f:
            json.dump(process_instance, f, indent=4)
        print(f"Process saved at: {filepath}")

    except jsonschema.exceptions.ValidationError as e:
        print(f"Process validation failed: {e}")

# function to validate all instances in the 'objects' and 'processes' directories
def validate_all_instances():
    print("Validating all object and process instances...")

    # Validate all objects in the 'objects' directory
    object_dir = 'objects'
    if os.path.exists(object_dir):
        for filename in os.listdir(object_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(object_dir, filename)
                with open(filepath, 'r') as f:
                    object_instance = json.load(f)
                    try:
                        validate(instance=object_instance, schema=object_schema)
                        print(f"Object {object_instance['id']} is valid.")
                    except jsonschema.exceptions.ValidationError as e:
                        print(f"Object {object_instance['id']} validation failed: {e}")

    # Validate all processes in the 'processes' directory
    process_dir = 'processes'
    if os.path.exists(process_dir):
        for filename in os.listdir(process_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(process_dir, filename)
                with open(filepath, 'r') as f:
                    process_instance = json.load(f)
                    try:
                        validate(instance=process_instance, schema=process_schema)
                        print(f"Process {process_instance['id']} is valid.")
                    except jsonschema.exceptions.ValidationError as e:
                        print(f"Process {process_instance['id']} validation failed: {e}")

    print("Validation completed.")



# Example usage
def example():
    # Example object instance
    object_instance = {
      "id": "obj_001",
      "name": "Cell",
      "type": "BiologicalCell",
      "attributes": {
        "mass": 50,
        "volume": 100
      },
      "boundary_conditions": {
        "temperature": {
            "type": "fixed",
            "value": 37.0,
            "behavior": "constant"
        }
      },
      "contained_object_types": []
    }

    # Example process instance
    process_instance = {
        "id": "proc_001",
        "name": "Cell Growth",
        "type": "growth_process",
        "attributes": {
            "temperature": 37,
            "pressure": 1.0
        },
        "participating_objects": ["Cell"],
        "dynamics": {
            "type": "growth",
            "rate": 0.02
        },
    }

    # Validate and save the example object and process
    validate_and_save_object(object_instance, overwrite=True)
    validate_and_save_process(process_instance, overwrite=True)


if __name__ == "__main__":
    example()
    validate_all_instances()
