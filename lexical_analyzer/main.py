import re

from enum import Enum

class TokenType(Enum):
    keyword = 1
    logical_operator = 2
    aritmetical_operator = 3
    simbols = 4
    text = 5
    condition_operator = 6


class Token:
    content: str
    type: TokenType

    def __init__(self, content : str, type:TokenType):
        self.content = content,
        self.type = type


class PythonLexicalAnalyzer:
    result : str
    result_list : list[Token]

    variables_tokens : list[str] = ['cryInt', 'cryString', 'cryBool']
    condition_tokens : list[str] = ['bugCheck', 'endBugCheck', 'goAway', 'flyAway']

    keywords_tokens : list = variables_tokens + condition_tokens

    logical_operator_tokens : list = ['<', '>']

    aritmetical_tokens = ['*']

    simbols : list[str] = ['=', ';', '(', ')', '{', '}']

    def __init__(self, content : str, language_definitions:dict = []):
        self.result = content
        self.language_definitions = language_definitions
        self.result_list = []

        # Prepare Data
        self.remove_comments()
        self.remove_break_lines()

        # Analyze Data
        self.tokenize_content()

    def get_token_list(self) -> list[Token]:
        return self.result_list


    def remove_comments(self) -> None:
        self.result = re.sub(r'\/\/.*\n', '', self.result)
        print(self.result)


    def remove_break_lines(self) -> None:
        self.result = re.sub(r'\n', ' ', self.result)
        self.result = re.sub(r'\t', '', self.result)


    def tokenize_content(self) -> None:
        def add_new_token(content:str, type:TokenType):
            self.result_list.append(Token(content.strip(), type))

        text = ""

        # for char in self.result:
            
        #     # KeyWord Tokens
        #     if text in self.keywords_tokens:
        #         print(1, ' ', text)
        #         add_new_token(text, TokenType.keyword)
        #         text = ''
            
        #     # Aritmetical Tokens
        #     if text in self.aritmetical_tokens:
        #         print(2, ' ', text)
        #         add_new_token(text, TokenType.aritmetical_operator)
        #         text = ''

        #     # Logical Tokens
        #     if text in self.logical_operator_tokens:
        #         print(3, ' ', text)
        #         add_new_token(text, TokenType.logical_operator)
        #         text = ''

        #     # Simbols
        #     if text in self.simbols:
        #         print(4, ' ', text)
        #         add_new_token(text, TokenType.simbols)
        #         text = ''

        #     # Text (Value or)
        #     if char == " ":
        #         print(5, ' ', text)
        #         if text != '':
        #             add_new_token(text, TokenType.text)
        #             text = ''
        #         else:
        #             text += char
        #         continue

        #     text += char

        self.result = " ".join(self.result.split())
        next_is_simbol = False
        for char in self.result:
            # KeyWord Tokens
            if text in self.keywords_tokens:
                add_new_token(text, TokenType.keyword)
                text = ''
            
            # Aritmetical Tokens
            if text in self.aritmetical_tokens:
                add_new_token(text, TokenType.aritmetical_operator)
                text = ''

            # Logical Tokens
            if text in self.logical_operator_tokens:
                add_new_token(text, TokenType.logical_operator)
                text = ''

            # Simbols
            if char in self.simbols:
                if text != "":
                    next_is_simbol = True
                    add_new_token(text, TokenType.text)
                    text = ''

            if next_is_simbol:
                next_is_simbol = False
                add_new_token(text, TokenType.simbols)
                text = ''

            # Text (Value or)
            if char == " ":
                if text != "":
                    add_new_token(text, TokenType.text)
                    text = ""
                    continue
            text += char
            


class PythonLexicalAnalyzer2:
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

"""
if __name__ == '__main__':
    file_path_to_extract = "code-simplified.py"
    file_path_to_write_result = "result.txt"
    
    file_manager = FileManager()
    content = file_manager.get_content_file(file_path_to_extract)

    lexicalAnalyzer = PythonLexicalAnalyzer(content)
    
    file_manager.write_result_in_file(file_path_to_write_result, lexicalAnalyzer.result)
    print(lexicalAnalyzer.result)
"""