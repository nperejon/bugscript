import json


def print_as_json(node):
    return json.dumps(node)

def print_ast(node, indent=""):
    if isinstance(node, dict):
        print(f"{indent}{node.get('type', 'Unknown')}")
        for key, value in node.items():
            if key != 'type':
                print(f"{indent}  {key}:")
                print_ast(value, indent + "    ")
    elif isinstance(node, list):
        for item in node:
            print_ast(item, indent + "  ")
    else:
        print(f"{indent}{node}")