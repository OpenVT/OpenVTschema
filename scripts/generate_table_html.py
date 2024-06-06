import json
import os

def load_instances(directory):
    instances = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                instances.append(json.load(file))
    return instances

def generate_html(instances):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simulators</title>
    </head>
    <body>
        <h1>Simulators</h1>
        <table border="1">
            <tr>
                <th>Name</th>
                <th>Description</th>
            </tr>
    """

    for instance in instances:
        name = instance.get("name", "N/A")
        description = instance.get("description", "N/A")
        html_content += f"""
            <tr>
                <td>{name}</td>
                <td>{description}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """
    return html_content

def save_html(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    instances_directory = "instances"
    html_path = "instances.html"

    instances = load_instances(instances_directory)
    html_content = generate_html(instances)
    save_html(html_path, html_content)

if __name__ == "__main__":
    main()
