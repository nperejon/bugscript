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

if __name__ == '__main__':
    file_path_to_extract = "teste.bug"
    file_path_to_write_result = "result.txt"
    
    file_manager = FileManager()
    content = file_manager.get_content_file(file_path_to_extract)

    lexical_analyzer = BugScriptLexicalAnalyzer(content)
    tokens = lexical_analyzer.result.split()

    # Debug: Print tokens for tracing
    print("Tokens:", tokens)

    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("AST:", ast)
    except Exception as e:
        print(f"Unexpected error: {e}")

    file_manager.write_result_in_file(file_path_to_write_result, lexical_analyzer.result)