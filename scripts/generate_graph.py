import json
import os
import argparse
from graphviz import Digraph

def load_instance(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_graph(instance):
    print(f'Creating graph for {instance["name"]}')
    dot = Digraph(comment=instance['name'])

    # Add objects
    for obj in instance['objects']:
        obj_label = f"{obj['name']}\nAttributes: {', '.join(obj['attributes'])}"
        dot.node(obj['object_id'], obj_label, shape='ellipse')

        # Add processes
        for proc_id in obj.get('processes', []):
            proc = next((p for p in instance['processes'] if p['process_id'] == proc_id), None)
            if proc:
                proc_label = f"{proc['name']}\n{proc['description']}"
                dot.node(proc['process_id'], proc_label, shape='box')
                dot.edge(obj['object_id'], proc['process_id'], label="uses")

        # Add boundary conditions
        for bc_id in obj.get('boundary_conditions', []):
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
    for containment in instance.get('containment', []):
        dot.edge(containment['outer_object_id'], containment['inner_object_id'], label="contains")

    return dot

def save_graph(dot, file_path):
    dot.render(file_path, format='png')

def main():
    parser = argparse.ArgumentParser(description="Generate graphs for simulator instances.")
    parser.add_argument(
        'simulator',
        type=str,
        help='The name of the simulator schema JSON file (without extension), or "all" to generate graphs for all simulators.')
    args = parser.parse_args()

    instances_directory = 'simulator_schemas'
    output_directory = 'docs/simulator_graphs'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if args.simulator.lower() == 'all':
        print(f"Generating graphs for all simulators in {instances_directory}")
        for filename in os.listdir(instances_directory):
            if filename.endswith(".json"):
                instance_file = os.path.join(instances_directory, filename)
                instance = load_instance(instance_file)
                dot = create_graph(instance)
                output_file = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_graph")
                save_graph(dot, output_file)
    else:
        simulator = args.simulator
        if '.json' not in args.simulator:
            simulator = f"{simulator}.json"
        instance_file = os.path.join(instances_directory, f"{simulator}")
        if os.path.exists(instance_file):
            instance = load_instance(instance_file)
            dot = create_graph(instance)
            output_file = os.path.join(output_directory, f"{args.simulator}_graph")
            save_graph(dot, output_file)
        else:
            print(f"No instance found for simulator: {args.simulator}")


if __name__ == "__main__":
    main()
