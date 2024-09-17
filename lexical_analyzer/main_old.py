import re

from core.file_manager import FileManager

class PythonLexicalAnalyzer:
    result : str
    
    def __init__(self, content : str,):
        self.content = content
        self.result = content
        self.tokenize_content()

    def tokenize_content(self) -> None:
        self.remove_comments()
        self.remove_empty_lines()
        self.replace_identifiers()
        self.replace_key_words()
        self.replace_numbers()
        self.replace_simbols_and_characters()
        self.spacing_tokens()

    def remove_comments(self) -> None:
        self.result = re.sub(r'#.*', '', self.result)

    def remove_empty_lines(self) -> None:
        while re.search(r'\n\n', self.result) is not None:
            self.result = re.sub(r'\n\n', '\n', self.result)

    def replace_simbols_and_characters(self) -> None:
        regex_and_sub_list = [
            (r'    ', r' TAB '),
            (r'\:',   r' COLON '),
            (r'\(',   r' OPEN_PARENTHESIS '),
            (r'\)',   r' CLOSE_PARENTHESIS '),
            (r'>',    r' GREATER_THAN '),
            (r'<',    r' LESS_THAN '),
            (r' = ',  r' EQUAL '),
            (r'\+',   r' ADD_OPERATOR '),
            (r'\[',   r' OPEN_BRACKET '),
            (r'\]',   r' CLOSE_BRACKET '),
            (r'\,', r' COMMA '),
            (r'\n',   r' BREAK_LINE ')
        ]
        for (regex, sub) in regex_and_sub_list:
            self.result = re.sub(regex, sub, self.result)

    def spacing_tokens(self) -> None:
        self.result = self.result.split()
        self.result = "\n".join(self.result)

    def replace_numbers(self) -> None:
        self.result = re.sub(r'(\d+)', r'NUMBER=\1 ', self.result)

    def replace_key_words(self) -> None:
        self.result = re.sub(r'\b(if|else|for|while|in|True|False)\b', r'KW_\1', self.result)

    def replace_identifiers(self) -> None:
        self.result = re.sub(r'(\b(?!if\b|else\b|for\b|while\b|in\b|True\b|False\b)[a-zA-Z_][a-zA-Z0-9_]*\b)', r'IDENT_\1 ', self.result)
        
if __name__ == '__main__':
    file_path_to_extract = "teste.py"
    file_path_to_write_result = "result.txt"
    
    file_manager = FileManager()
    content = file_manager.get_content_file(file_path_to_extract)

    lexicalAnalyzer = PythonLexicalAnalyzer(content)
    
    file_manager.write_result_in_file(file_path_to_write_result, lexicalAnalyzer.result)
    print(lexicalAnalyzer.result)