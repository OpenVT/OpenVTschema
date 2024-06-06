import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from textwrap import wrap

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
        website = instance.get("website", "N/A")
        data.append([name, description, website])
    return pd.DataFrame(data, columns=["Name", "Description", "Website"])

def wrap_text(text, width):
    return "\n".join(wrap(text, width))

def save_table_as_image(df, file_path):
    fig, ax = plt.subplots(figsize=(14, len(df) * 0.5 + 2))
    ax.axis('tight')
    ax.axis('off')

    cell_text = []
    for row in df.values:
        wrapped_row = [
            row[0],  # Name
            wrap_text(row[1], 40),  # Description
            row[2]  # Website
        ]
        cell_text.append(wrapped_row)

    table = ax.table(cellText=cell_text, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    for key, cell in table.get_celld().items():
        cell.set_edgecolor('grey')
        if key[0] == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('black')

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
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
