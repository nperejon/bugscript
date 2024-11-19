import subprocess
from source.parser import Parser
from source.code_generator import CodeGenerator
from source.file_manager import FileManager
from source.lexer import BugScriptLexicalAnalyzer
from source.semantic import SemanticAnalyzer
from source.semantic_error import SemanticError


def execute_file(file_manager:FileManager, folder:str, file_name:str):
    file_path_to_write_result = f"outputs/{file_name}_result.txt"
    file_output_python_path = f"outputs/{file_name}_result.txt"

    try:
        content = file_manager.get_content_file(folder + '/' + file_name)
    except FileNotFoundError:
        print(f"File not found: {folder}/{file_name}")
    except Exception as e:
        print(f"Error reading file: {e}")

    lexical_analyzer = BugScriptLexicalAnalyzer(content)
    tokens = lexical_analyzer.get_tokens()
    tokens.append(('EOF', ''))

    parser = Parser(tokens)
    try:
        ast = parser.parse()
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)

    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except SemanticError as e:
        print(f"Semantic Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()

    formatted_tokens = "\n".join([f"{token[0]} - {token[1]}" for token in tokens])
   
    formatted_tokens = formatted_tokens.replace("\nNEWLINE - ", "")

    formatted_tokens = formatted_tokens.replace("\n\n", "\n")
    file_manager.write_result_in_file(file_path_to_write_result, formatted_tokens)
    
    codeGenerator = CodeGenerator(formatted_tokens)
    python_content = codeGenerator.generate()

    file_manager.write_result_in_file(file_output_python_path, python_content)
    subprocess.run(["python", file_output_python_path]) 