import json
import os
import matplotlib.pyplot as plt
import pandas as pd

def load_instances(directory):
    instances = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                instances.append(json.load(file))
    return instances

def generate_table(instances):
    data = []
    for instance in instances:
        name = instance.get("name", "N/A")
        description = instance.get("description", "N/A")
        data.append([name, description])
    return pd.DataFrame(data, columns=["Name", "Description"])

def save_table_as_image(df, file_path):
    fig, ax = plt.subplots(figsize=(8, len(df) * 0.5 + 1))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    plt.savefig(file_path, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)

def main():
    instances_directory = "instances"
    output_path = "docs/instances_table.png"

    instances = load_instances(instances_directory)
    df = generate_table(instances)
    save_table_as_image(df, output_path)

if __name__ == "__main__":
    main()
