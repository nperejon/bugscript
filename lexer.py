import re

class BugScriptLexicalAnalyzer:
    def __init__(self, content: str):
        self.content = content
        self.tokens = []
        self.tokenize_content()

    def tokenize_content(self) -> None:
        self.remove_comments()
        self.tokenize()

    def remove_comments(self) -> None:
        self.content = re.sub(r'#.*', '', self.content)

    def tokenize(self) -> None:
        patterns = [
            ('KW_INT', r'\bcryInt\b'),
            ('KW_FLOAT', r'\bcryFloat\b'),
            ('KW_BOOL', r'\bcryBool\b'),
            ('KW_STRING', r'\bcryString\b'),
            ('KW_WHILE', r'\bgoAway\b'),
            ('KW_IF', r'\bbugCheck\b'),
            ('KW_ELSE', r'\bendBugCheck\b'),
            ('KW_BREAK', r'\bflyAway\b'),
            ('KW_TRUE', r'\btrue\b'),
            ('KW_FALSE', r'\bfalse\b'),
            ('KW_OUTPUT', r'\boutBug\b'),
            ('KW_ADDITION', r'\bmoreBug\b'),
            ('KW_SUBTRACTION', r'\bminusBug\b'),
            ('KW_MULTIPLY', r'\btimesBug\b'),
            ('KW_DIVISION', r'\bdivideBug\b'),
            ('IDENT', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('DECIMAL', r'\b\d+\.\d+\b'),
            ('NUMBER', r'\b\d+\b'),
            ('LOGICAL_EQUAL', r'=='),
            ('LOGICAL_NEQUAL', r'!='),
            ('EQUAL', r'='),
            ('LESS_THAN', r'<'),
            ('GREATER_THAN', r'>'),
            ('OPEN_PAREN', r'\('),
            ('CLOSE_PAREN', r'\)'),
            ('OPEN_BRACKET', r'\{'),
            ('CLOSE_BRACKET', r'\}'),
            ('COMMA', r','),
            ('COLON', r':'),
            ('TEXT', r'\"([^\\\"]|\\.)*\"|\'([^\\\']|\\.)*\''),
            ('NEWLINE', r'\n'),
            ('WHITESPACE', r'\s+'),
            ('LOGICAL_AND', r'&&'),
            ('LOGICAL_OR', r'\|\|'),
            ('LOGICAL_NOT', r'!'),
        ]

        regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns)
        for match in re.finditer(regex, self.content):
            token_type = match.lastgroup
            token_value = match.group()
            if token_type != 'WHITESPACE':
                self.tokens.append((token_type, token_value))

    def get_tokens(self):
        return self.tokens