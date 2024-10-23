from lexer import BugScriptLexicalAnalyzer
from parser import Parser

class FileManager:
    def get_content_file(self, file_path_to_extract) -> str:
        with open(file_path_to_extract, 'r', encoding="utf-8") as file:
            result = file.read()
        return result

    def write_result_in_file(self, file_path_to_write_result: str, content: str) -> None:
        with open(file_path_to_write_result, 'w+', encoding="utf-8") as file:
            file.write(content)

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

if __name__ == '__main__':
    file_path_to_extract = "teste.bug"
    file_path_to_write_result = "result.txt"
    
    file_manager = FileManager()
    try:
        content = file_manager.get_content_file(file_path_to_extract)
    except FileNotFoundError:
        print(f"File not found: {file_path_to_extract}")
    except Exception as e:
        print(f"Error reading file: {e}")

    lexical_analyzer = BugScriptLexicalAnalyzer(content)
    tokens = lexical_analyzer.get_tokens()
    tokens.append(('EOF', ''))  # Add EOF token

    # Debug: Print tokens for tracing
    print("Tokens:")
    for i, token in enumerate(tokens):
        print(f"{i}: {token[0]} - {token[1]}")

    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("\nAbstract Syntax Tree:")
        print_ast(ast)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

    formatted_tokens = "\n".join([f"{token[0]} - {token[1]}" for token in tokens])
    file_manager.write_result_in_file(file_path_to_write_result, formatted_tokens)