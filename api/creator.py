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
        # Initialize the object instance with defaults based on the schema
        self.schema = object_schema
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

    def add_attribute(self, **kwargs):
        """Add attributes dynamically based on schema."""
        for key, value in kwargs.items():
            if key in self.schema['properties']['attributes']['additionalProperties']['oneOf']:
                self.object_instance["attributes"][key] = value
            else:
                print(f"Invalid attribute: {key} not allowed in schema.")

    def add_boundary_condition(self, var, condition):
        """Add boundary condition dynamically."""
        self.object_instance["boundary_conditions"][var] = condition

    def add_contained_object(self, contained_obj_type):
        self.object_instance["contained_object_types"].append(contained_obj_type)

    def validate(self):
        """Check the instance for missing fields and validate against the schema."""
        missing_fields = []
        for key in self.schema['required']:
            if self.object_instance.get(key) is None:
                missing_fields.append(key)

        if missing_fields:
            print(f"Missing required fields: {missing_fields}")
            return False
        try:
            validate(instance=self.object_instance, schema=self.schema)
            print("Object is valid.")
            return True
        except jsonschema.exceptions.ValidationError as e:
            # Detailed error message
            error_message = f"Validation failed at {list(e.path)}: {e.message}"
            print(error_message)
            return False

    def save(self, object_dir='objects', overwrite=False):
        """Save the validated object to a file."""
        if not self.validate():
            print("Cannot save object. Validation failed.")
            return
        object_id = self.object_instance['id']
        filepath = os.path.join(object_dir, f"{object_id}.json")
        if os.path.exists(filepath) and not overwrite:
            print(f"Error: An object with ID '{object_id}' already exists. Use overwrite=True to replace it.")
            return
        with open(filepath, 'w') as f:
            json.dump(self.object_instance, f, indent=4)
        print(f"Object saved at: {filepath}")


# Helper class for creating processes
class ProcessCreator:
    def __init__(self):
        # Initialize the process instance with defaults based on the schema
        self.schema = process_schema
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

    def add_attribute(self, **kwargs):
        """Add attributes dynamically based on schema."""
        for key, value in kwargs.items():
            if key in self.schema['properties']['attributes']['additionalProperties']['oneOf']:
                self.process_instance["attributes"][key] = value
            else:
                print(f"Invalid attribute: {key} not allowed in schema.")

    def add_participating_object(self, obj_name):
        self.process_instance["participating_objects"].append(obj_name)

    def set_dynamics(self, dynamics_type, rate):
        self.process_instance["dynamics"] = {"type": dynamics_type, "rate": rate}

    def add_event(self, event_name, trigger):
        self.process_instance["events"].append({"name": event_name, "trigger": trigger})

    def validate(self):
        """Check the instance for missing fields and validate against the schema."""
        missing_fields = []
        for key in self.schema['required']:
            if self.process_instance.get(key) is None:
                missing_fields.append(key)

        if missing_fields:
            print(f"Missing required fields: {missing_fields}")
            return False
        try:
            validate(instance=self.process_instance, schema=self.schema)
            print("Process is valid.")
            return True
        except jsonschema.exceptions.ValidationError as e:
            # Detailed error message
            error_message = f"Validation failed at {list(e.path)}: {e.message}"
            print(error_message)
            return False

    def save(self, process_dir='processes', overwrite=False):
        """Save the validated process to a file."""
        if not self.validate():
            print("Cannot save process. Validation failed.")
            return
        process_id = self.process_instance['id']
        filepath = os.path.join(process_dir, f"{process_id}.json")
        if os.path.exists(filepath) and not overwrite:
            print(f"Error: A process with ID '{process_id}' already exists. Use overwrite=True to replace it.")
            return
        with open(filepath, 'w') as f:
            json.dump(self.process_instance, f, indent=4)
        print(f"Process saved at: {filepath}")


# Example usage of the API
def example():
    # Create an object using the API
    obj_creator = ObjectCreator()
    obj_creator.set_id("obj_003")
    obj_creator.set_name("Heart Cell")
    obj_creator.set_type("CardiacCell")
    obj_creator.add_attribute(mass=100, volume=200)
    obj_creator.add_boundary_condition("pressure", {"type": "dynamic", "value": 120, "behavior": "periodic"})
    obj_creator.save(overwrite=True)

    # Create a process using the API
    proc_creator = ProcessCreator()
    proc_creator.set_id("proc_003")
    proc_creator.set_name("Blood Flow")
    proc_creator.set_type("circulation_process")
    proc_creator.add_attribute(temperature=37, velocity=2.0)
    proc_creator.set_dynamics("flow", 0.05)
    proc_creator.add_event("valve_open", "pressure_exceeds_threshold")
    proc_creator.save(overwrite=True)

if __name__ == "__main__":
    example()
