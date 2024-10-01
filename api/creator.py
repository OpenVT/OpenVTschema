import json
import os
import jsonschema
from jsonschema import validate

# Load schemas from the 'schemas' directory
with open('schemas/object_schema.json', 'r') as obj_schema_file:
    object_schema = json.load(obj_schema_file)

with open('schemas/process_schema.json', 'r') as proc_schema_file:
    process_schema = json.load(proc_schema_file)


# Helper class for creating objects
class ObjectCreator:
    def __init__(self):
        self.object_instance = {
            "id": None,
            "name": None,
            "type": None,
            "attributes": {},
            "boundary_conditions": {},
            "contained_object_types": []
        }

    def set_id(self, obj_id):
        self.object_instance["id"] = obj_id

    def set_name(self, name):
        self.object_instance["name"] = name

    def set_type(self, obj_type):
        self.object_instance["type"] = obj_type

    def add_attribute(self, key, value):
        self.object_instance["attributes"][key] = value

    def add_boundary_condition(self, var, condition):
        self.object_instance["boundary_conditions"][var] = condition

    def add_contained_object(self, contained_obj_type):
        self.object_instance["contained_object_types"].append(contained_obj_type)

    def get_instance(self):
        return self.object_instance


# Helper class for creating processes
class ProcessCreator:
    def __init__(self):
        self.process_instance = {
            "id": None,
            "name": None,
            "type": None,
            "attributes": {},
            "participating_objects": [],
            "dynamics": None,
            "events": []
        }

    def set_id(self, process_id):
        self.process_instance["id"] = process_id

    def set_name(self, name):
        self.process_instance["name"] = name

    def set_type(self, process_type):
        self.process_instance["type"] = process_type

    def add_attribute(self, key, value):
        self.process_instance["attributes"][key] = value

    def add_participating_object(self, obj_name):
        self.process_instance["participating_objects"].append(obj_name)

    def set_dynamics(self, dynamics_type, rate):
        self.process_instance["dynamics"] = {"type": dynamics_type, "rate": rate}

    def add_event(self, event_name, trigger):
        self.process_instance["events"].append({"name": event_name, "trigger": trigger})

    def get_instance(self):
        return self.process_instance


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


# Example usage of the API
def example():
    # Create an object using the API
    obj_creator = ObjectCreator()
    obj_creator.set_id("obj_002")
    obj_creator.set_name("Neuron Cell")
    obj_creator.set_type("NeuralCell")
    obj_creator.add_attribute("mass", 30)
    obj_creator.add_boundary_condition("membrane_potential",
                                       {"type": "dynamic", "value": -70, "behavior": "oscillating"})
    object_instance = obj_creator.get_instance()

    # Create a process using the API
    proc_creator = ProcessCreator()
    proc_creator.set_id("proc_002")
    proc_creator.set_name("Action Potential")
    proc_creator.set_type("electrical_process")
    proc_creator.add_attribute("temperature", 37)
    proc_creator.set_dynamics("spike", 1.0)
    proc_creator.add_event("threshold_reached", "membrane_potential_exceeds")
    process_instance = proc_creator.get_instance()

    # Validate and save object and process
    validate_and_save_object(object_instance, overwrite=True)
    validate_and_save_process(process_instance, overwrite=True)


if __name__ == "__main__":
    example()
