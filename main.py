from source.code_generator import CodeGenerator
from source.file_manager import FileManager
from source.lexer import BugScriptLexicalAnalyzer
from source.output import print_as_json, print_ast
from source.parser import Parser
from source.semantic import SemanticAnalyzer
from source.semantic_error import SemanticError
import subprocess

if __name__ == '__main__':
    file_path_to_extract = "tests/teste.bug"
    file_path_to_write_result = "outputs/result.txt"
    file_output_python_path = "outputs/result.py"
    
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

    tokens_json = print_as_json(tokens)
    print("\n" + "JSON TOKENS:\n" + tokens_json + "\n")

    # Debug: Print tokens for tracing
    print("Tokens:")
    for i, token in enumerate(tokens):
        print(f"{i}: {token[0]} - {token[1]}")

    parser = Parser(tokens)
    try:
        ast = parser.parse()
        ast_json = print_as_json(ast)
        print("\n" + "AST TOKENS:\n" + ast_json)
        print("\nAbstract Syntax Tree:")
        print_ast(ast)

        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)
        print("\nSemantic analysis completed successfully.")

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

    print("\nExecution Result:\n")

    subprocess.run(["python", file_output_python_path]) 
