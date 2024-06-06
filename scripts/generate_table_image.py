import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.table import Table

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

def wrap_text(text, width):
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) + len(current_line) > width:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
        else:
            current_line.append(word)
            current_length += len(word)
    if current_line:
        lines.append(" ".join(current_line))
    return "\n".join(lines)

def save_table_as_image(df, file_path, cell_width=30, cell_height=0.25):
    fig, ax = plt.subplots(figsize=(12, len(df) * cell_height + 1))
    ax.axis('tight')
    ax.axis('off')

    table = Table(ax, bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    n_rows, n_cols = df.shape
    width_ratios = [1.5, 3]  # Adjust these ratios to change column widths
    for (i, j), val in np.ndenumerate(df.values):
        wrapped_text = wrap_text(val, width=cell_width if j == 1 else cell_width)
        table.add_cell(i, j, width_ratios[j], cell_height, text=wrapped_text, loc='center', facecolor='white')

    # Add headers
    for j, col in enumerate(df.columns):
        table.add_cell(-1, j, width_ratios[j], cell_height, text=col, loc='center', facecolor='lightgrey')

    ax.add_table(table)
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
