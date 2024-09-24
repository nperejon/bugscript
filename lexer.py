import re

class BugScriptLexicalAnalyzer:
    def __init__(self, content: str):
        self.content = content
        self.result = content
        self.tokenize_content()

    def tokenize_content(self) -> None:
        self.remove_comments()
        self.remove_empty_lines()
        self.replace_key_words()
        self.replace_symbols_and_characters()
        self.replace_numbers()
        self.replace_identifiers()
        self.spacing_tokens()

    def remove_comments(self) -> None:
        self.result = re.sub(r'#.*', '', self.result)

    def remove_empty_lines(self) -> None:
        self.result = re.sub(r'\n+', '\n', self.result)

    def replace_symbols_and_characters(self) -> None:
        regex_and_sub_list = [
            (r'$$', r' OPEN_PARENTHESIS '),
            (r'$$', r' CLOSE_PARENTHESIS '),
            (r'$$', r' OPEN_BRACKET '),
            (r'$$', r' CLOSE_BRACKET '),
            (r'>', r' GREATER_THAN '),
            (r'<', r' LESS_THAN '),
            (r'=', r' EQUAL '),
            (r'\+', r' ADD_OPERATOR '),
            (r'-', r' SUB_OPERATOR '),
            (r',', r' COMMA '),
            (r':', r' COLON '),
            (r'\n', r' BREAK_LINE ')
        ]
        for (regex, sub) in regex_and_sub_list:
            self.result = re.sub(regex, sub, self.result)

    def spacing_tokens(self) -> None:
        self.result = ' '.join(self.result.split())

    def replace_numbers(self) -> None:
        self.result = re.sub(r'\b(\d+)\b', r'NUMBER \1', self.result)

    def replace_key_words(self) -> None:
        keywords = {
            'cryInt': 'KW_INT',
            'cryString': 'KW_STRING',
            'cryBool': 'KW_BOOL',
            'inBug': 'KW_INPUT',
            'outBug': 'KW_OUTPUT',
            'minusBug': 'KW_SUBTRACTION',
            'moreBug': 'KW_ADDITION',
            'bugCheck': 'KW_IF',
            'endBugCheck': 'KW_ELSE',
            'goAway': 'KW_WHILE',
            'flyAway': 'KW_BREAK',
            'true': 'KW_TRUE',
            'false': 'KW_FALSE'
        }

        for keyword, token in keywords.items():
            self.result = re.sub(r'\b' + keyword + r'\b', token, self.result)

    def replace_identifiers(self) -> None:
        self.result = re.sub(r'\b(?!KW_INT\b|KW_STRING\b|KW_BOOL\b|KW_INPUT\b|KW_OUTPUT\b|KW_SUBTRACTION\b|KW_ADDITION\b|KW_IF\b|KW_ELSE\b|KW_WHILE\b|KW_BREAK\b|KW_TRUE\b|KW_FALSE\b|NUMBER\b|OPEN_PARENTHESIS\b|CLOSE_PARENTHESIS\b|OPEN_BRACKET\b|CLOSE_BRACKET\b|GREATER_THAN\b|LESS_THAN\b|EQUAL\b|ADD_OPERATOR\b|SUB_OPERATOR\b|COMMA\b|COLON\b|BREAK_LINE\b)[a-zA-Z_][a-zA-Z0-9_]*\b', r'IDENT \g<0>', self.result)