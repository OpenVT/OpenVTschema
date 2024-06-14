import json
import os
import pandas as pd

def load_instances(directory):
    instances = []
    # base_url = "https://raw.githubusercontent.com/OpenVT/OpenVTschema/main/"
    base_url = "https://raw.githubusercontent.com/rheiland/OpenVTschema/main/"
    # for filename in os.listdir(directory):
    # artistoo.json		compucell3d.json	netlogo.json		simucell3d.json
    # biocellion.json		hal.json		physicell.json		tissue_forge.json
    # chaste.json		morpheus.json		polyhoop.json
    for filename in ["compucell3d.json", "physicell.json", "chaste.json", "morpheus.json", "tissue_forge.json", "biocellion.json", "artistoo.json", "simucell3d.json", "hal.json", "netlogo.json", "polyhoop.json"]:
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                instance = json.load(file)
                # Construct the correct URL for the schema link
                instance['schema_link'] = base_url + os.path.join(directory, filename).replace("\\", "/")
                instances.append(instance)
    return instances

def generate_table(instances):
    data = []
    for instance in instances:
        name = instance.get("name", "N/A")
        description = instance.get("description", "N/A")
        website = instance.get("website", "N/A")
        # schema_link = instance.get("schema_link", "N/A")
        # data.append([name, description, website, schema_link])
        data.append([name, description, website])
    # return pd.DataFrame(data, columns=["Name", "Description", "Website", "Schema"])
    return pd.DataFrame(data, columns=["Name", "Description", "Website"])

def save_table_as_html(df, file_path):
    if df.empty:
        print("No data to display.")
        return

    # Make website and schema links clickable
    # df['Website'] = df['Website'].apply(lambda x: f'<a href="{x}">{x}</a>')
    df['Website'] = df['Website'].apply(lambda x: f'<a href="{x}">link</a>')
    # df['Schema'] = df['Schema'].apply(lambda x: f'<a href="{x}">Link</a>')

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
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}
        th {{
            background-color: black;
            color: white;
        }}
    </style>
    </head>
    <body>
    <h1>Multicellular Frameworks</h1>
    {html_table}
    </body>
    </html>
    """

    # Save HTML to a file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(html_template)

def main():
    instances_directory = "simulator_schemas"
    output_path = "docs/instances_table.html"

    instances = load_instances(instances_directory)
    df = generate_table(instances)
    save_table_as_html(df, output_path)
    print("--> ",output_path)

if __name__ == "__main__":
    main()
