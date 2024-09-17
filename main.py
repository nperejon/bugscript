from core.file_manager import FileManager
from lexical_analyzer.main import PythonLexicalAnalyzer
from json import loads, dumps

file_path_to_extract = "code-simplified.bs"
file_path_to_write_result = "result.txt"

file_manager = FileManager()
language_definitions = file_manager.get_content_file('./core/language_definitions.json');
dict_language_definitions = loads(language_definitions)

content = file_manager.get_content_file(file_path_to_extract)

lexicalAnalyzer = PythonLexicalAnalyzer(content, dict_language_definitions)

tokens = lexicalAnalyzer.get_token_list()
for token in tokens:
    print(f"{token.type}: {token.content}")

# file_manager.write_result_in_file(file_path_to_write_result, tokens_string)
# print(lexicalAnalyzer.result)