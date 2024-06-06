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


def generate_table(instances):
    table = "| Name | Description |\n"
    table += "| ---- | ----------- |\n"
    for instance in instances:
        name = instance.get("name", "N/A")
        description = instance.get("description", "N/A")
        table += f"| {name} | {description} |\n"
    return table


def update_readme(readme_path, table):
    with open(readme_path, 'r') as file:
        readme_content = file.read()

    start_marker = "<!-- START INSTANCES TABLE -->"
    end_marker = "<!-- END INSTANCES TABLE -->"

    start_index = readme_content.find(start_marker) + len(start_marker)
    end_index = readme_content.find(end_marker)

    new_readme_content = (
        readme_content[:start_index]
        + "\n" + table + "\n"
        + readme_content[end_index:]
    )

    with open(readme_path, 'w') as file:
        file.write(new_readme_content)


def main():
    instances_directory = "instances"
    readme_path = "README.md"

    instances = load_instances(instances_directory)
    table = generate_table(instances)
    update_readme(readme_path, table)


if __name__ == "__main__":
    main()
