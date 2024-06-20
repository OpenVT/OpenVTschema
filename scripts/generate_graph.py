import json
import os
from graphviz import Digraph

def load_instance(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_graph(instance):
    dot = Digraph(comment=instance['name'])

    # Add objects
    for obj in instance['objects']:
        obj_label = f"{obj['name']}\nAttributes: {', '.join(obj['attributes'])}"
        dot.node(obj['object_id'], obj_label, shape='ellipse')

        # Add processes
        for proc_id in obj['processes']:
            proc = next((p for p in instance['processes'] if p['process_id'] == proc_id), None)
            if proc:
                proc_label = f"{proc['name']}\n{proc['description']}"
                dot.node(proc['process_id'], proc_label, shape='box')
                dot.edge(obj['object_id'], proc['process_id'], label="uses")

        # Add boundary conditions
        for bc_id in obj['boundary_conditions']:
            bc = next((bc for bc in instance['boundaries']['pde_boundary_conditions'] if bc['bc_id'] == bc_id), None)
            if bc:
                bc_label = f"{bc['type']} BC\nValue: {bc['value']}"
                dot.node(bc['bc_id'], bc_label, shape='diamond')
                dot.edge(obj['object_id'], bc['bc_id'], label="adheres to")
            else:
                bc = next((bc for bc in instance['boundaries']['geometric_constraints'] if bc['gc_id'] == bc_id), None)
                if bc:
                    bc_label = f"{bc['type']} GC\nDims: {', '.join(bc['dimensions'])}"
                    dot.node(bc['gc_id'], bc_label, shape='diamond')
                    dot.edge(obj['object_id'], bc['gc_id'], label="adheres to")

    # Add containment relationships
    for containment in instance['containment']:
        dot.edge(containment['outer_object_id'], containment['inner_object_id'], label="contains")

    return dot

def save_graph(dot, file_path):
    dot.render(file_path, format='png')

def main():
    instance_file = '../simulator_schemas/compucell3d.json'  # Path to your CompuCell3D instance JSON file
    output_file = '../docs/compucell3d_graph'

    instance = load_instance(instance_file)
    dot = create_graph(instance)
    save_graph(dot, output_file)

if __name__ == "__main__":
    main()
