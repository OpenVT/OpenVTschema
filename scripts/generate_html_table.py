import json
import os
import pandas as pd

def load_instances(directory):
    instances = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                instance = json.load(file)
                instance['schema_link'] = filepath
                instances.append(instance)
    return instances

def generate_table(instances):
    data = []
    for instance in instances:
        name = instance.get("name", "N/A")
        description = instance.get("description", "N/A")
        website = instance.get("website", "N/A")
        schema_link = instance.get("schema_link", "N/A")
        data.append([name, description, website, schema_link])
    return pd.DataFrame(data, columns=["Name", "Description", "Website", "Schema"])

def save_table_as_html(df, file_path):
    if df.empty:
        print("No data to display.")
        return

    # Make website and schema links clickable
    df['Website'] = df['Website'].apply(lambda x: f'<a href="{x}">{x}</a>')
    df['Schema'] = df['Schema'].apply(lambda x: f'<a href="{x}">Link</a>')

    # Create HTML table
    html_table = df.to_html(escape=False, index=False)

    # Define HTML template for better styling
    html_template = f"""
    <html>
    <head>
    <style>
        table, th, td {{
            border: 1px solid black;
            border-collapse: collapse;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: black;
            color: white;
        }}
    </style>
    </head>
    <body>
    <h1>Simulators</h1>
    {html_table}
    </body>
    </html>
    """

    # Save HTML to a file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(html_template)

def main():
    instances_directory = "instances"
    output_path = "docs/instances_table.html"

    instances = load_instances(instances_directory)
    df = generate_table(instances)
    save_table_as_html(df, output_path)

if __name__ == "__main__":
    main()
